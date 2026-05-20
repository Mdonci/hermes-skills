# Long-Running Process Diagnosis

## The Scenario

A cron-launched job appears to be running but is past its expected finish time. Is it hung? Slow? Failed silently?

**Wrong answer:** Assume it's dead and kill it.
**Right answer:** Instrument the process first, then decide.

---

## Diagnostic Sequence

### Step 1: Confirm Process Is Alive

```bash
ps aux | grep <process_name> | grep -v grep
ps -p <PID> -o pid,etime,stat,cmd
```

- `Ss` (sleeping) + elapsed time increasing = alive
- `Z` (zombie) = dead, reap with parent
- ` Sl` (interruptible sleep with elapsed time) = actively computing

### Step 2: Find the Real PID

If you see a bash parent process, find children:

```bash
pstree -p <PID>
# or
ps --ppid <PID> -o pid,etime,stat,cmd
```

The bash script wraps Python; the Python process is where the work happens.

### Step 3: Check CPU and Thread Count

```bash
ps -p <PID> -o pid,pcpu,pmem,rss,etime,stat,wchan
cat /proc/<PID>/status | grep -E "Threads|State|VmPeak|VmRSS"
ls /proc/<PID>/task/ | wc -l
```

Key signals:
- `wchan: futex_wait_queue` = normal multi-threaded sleep between batches (NOT a deadlock)
- High `%CPU` (90%+) = actively computing
- `VmRSS` stable + `Threads: N` stable = not leaking memory

### Step 4: Check System-Level Resource Contention

```bash
vmstat 1 3        # CPU: us/sy/id — is the box under load?
iostat -x 1 2     # I/O: is disk saturated?
```

- `id 0` with high `us` = CPU-bound (normal for ML inference)
- High `iowait` = disk bottleneck

### Step 5: Check for Blocking I/O or Network

```bash
ls -la /proc/<PID>/fd/ 2>/dev/null | grep -v "^total"
cat /proc/<PID>/cmdline 2>/dev/null | tr '\0' ' '
```

Look for:
- Open files pointing to large files being read
- Pipes (`pipe:[...]`) — normal for subprocess communication
- Sockets to external services (HuggingFace, S3, etc.)

### Step 6: Check Application Logs

HuggingFace model downloads write to:
```
/root/.cache/huggingface/xet/logs/xet_YYYYMMDDTHHMMSS+0000_<PID>.log
```

This log shows:
- S3 range requests (`s3::get_range`, status 206)
- File reconstruction progress (`File reconstruction completed successfully`)
- Download concurrency adjustments

**If the log is actively writing** → the process is downloading model files, not hung.

### Step 7: Check File Output (Partial Progress)

Some jobs write output incrementally. Check timestamps:

```bash
ls -la /root/transcripts/*.txt 2>/dev/null | tail -10
stat /root/transcripts/chunks_full/chunk_000.wav | grep Modify
```

If output files are being written, the job is making progress.

---

## Common "Appears Stuck" Patterns

### Pattern 1: Downloading Model Files
- **Symptom:** Process alive, low CPU, log shows S3 requests
- **Cause:** First run downloads model to `~/.cache/huggingface/`
- **Fix:** Wait — this is one-time, then subsequent runs are fast

### Pattern 2: Multi-threaded Sleep Between Batches
- **Symptom:** `futex_wait_queue` in wchan, high CPU
- **Cause:** Normal — threads sleep waiting for next inference batch
- **Fix:** Not a problem — process is working

### Pattern 3: I/O Bottleneck on Large File Read
- **Symptom:** High RSS, low CPU, disk `bi` elevated
- **Cause:** Reading large audio/video files from disk
- **Fix:** Not a problem — normal for media processing

### Pattern 4: Cron Job LLM Fabricating Success
- **Symptom:** Log or response says "completed" but no output files written
- **Cause:** LLM in cron prompt hallucinated success instead of reporting failure
- **Fix:** Verify actual side effects — file timestamps, DB row counts, exit codes

---

## Faster Whisper Timing Reference (VPS, CPU-only)

| Model | Compute Type | Time/chunk (110MB, ~22min audio) |
|-------|-------------|----------------------------------|
| tiny | int8 | ~2-3 min |
| small | int8 | ~4-6 min |
| **medium** | **int8** | **~7-10 min** |
| large | int8 | ~15-20 min |

17 chunks × medium int8 ≈ **120-170 min total** (not 51-85 min as initially estimated)

**Key variables:** Audio complexity, number of speakers, background music, CPU contention from other processes.

---

## When to Kill

- `ps` shows process gone (completed or crashed)
- `ps` shows zombie (`Z`) — parent not reaping
- Log shows uncaught exception + stack trace
- CPU at 0% AND no I/O AND log not advancing → likely dead but pipe open

**Do NOT kill** just because it's past the estimated time — investigate first.