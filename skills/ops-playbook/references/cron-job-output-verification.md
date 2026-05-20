# Cron Job Output Verification

> **Pattern for verifying cron job completion and detecting new vs. continuing state changes.**

After a cron job runs (especially ones that write data and push to git), don't trust just the script's exit code or natural-language summary. Verify through actual side effects.

## Verification Sequence

### 1. Confirm the commit was created

```bash
git log -5
```

Look for the expected commit message (e.g., `oc-companies daily check: 2026-05-17`). If the most recent commit doesn't match today's date, the script never completed its push.

### 2. Confirm the push went through

```bash
git status
# → "Your branch is up to date with 'origin/main'."
```

If the branch is behind or ahead of origin, the push either failed or there are uncommitted changes. A clean working tree + up-to-date status = push succeeded.

### 3. Check what actually changed

```bash
git diff HEAD~1 --stat
```

This shows how many files were modified. For a script that updates N profiles, you should see roughly N files changed. Zero changes with a "success" exit code = the script may have hallucinated its results.

### 4. Determine "new finds" vs "carries" (stateful cron jobs)

When a cron job tracks "found" vs "not found" state per entity, compare the current result against yesterday's:

```bash
# Check if a company had roles yesterday too (carry) or only today (new)
git show HEAD~1:path/to/entity.md | grep -i "marketing role"
```

**Interpretation:**
- Same roles found today as yesterday → **continuing** (not newsworthy unless there's a count change)
- Different roles found today → **changed** (new role type appeared, or a role vanished)
- No roles found yesterday, roles found today → **new find** (interesting!)
- Roles found yesterday, none today → **expired** (role closed)

### 5. Verify profile updates directly

The most authoritative check: read the profile file that was supposedly updated and confirm its `Last Checked` date is today:

```bash
grep "Last Checked" path/to/profile.md
# → Should show today's date
```

## Common Pitfalls

**Truncated output:** Large script output (>50KB) gets cut by the terminal tool. If the push confirmation line is missing from the visible output, use the git-based checks above instead — they're more reliable.

**Exit code 1 on success:** Some scripts exit non-zero because a sub-process (e.g., a single company's page fetch) failed, even though the overall job completed and pushed successfully. Don't treat exit code as authoritative — check actual side effects.

**Script ran but nothing changed:** If the script processed all entities but found no state changes, it still should produce a commit with updated `Last Checked` timestamps. If even those didn't change, the script may not have run at all.
