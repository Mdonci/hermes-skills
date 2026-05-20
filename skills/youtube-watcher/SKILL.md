---
name: youtube-watcher
description: Fetch and read transcripts from YouTube videos. Use when you need to summarize a video, answer questions about or extract information from its content.
author: michael gathara
version: 1.1.0
triggers:
  - "watch youtube"
  - "summarize video"
  - "video transcript"
  - "youtube summary"
  - "analyze video"
  - "what does the video say"
  - "video content"
  - "get transcript"
  - "transcript this video"
---

# YouTube Watcher

Fetch transcripts from YouTube videos to enable summarization, QA, and content extraction.

## Setup

- Python package `youtube-transcript-api` must be installed in the Hermes venv:
  `uv pip install youtube-transcript-api --python /usr/local/lib/hermes-agent/venv/bin/python3`
- Works with videos that have closed captions (CC), auto-generated subtitles, or transcripts in any language
- If a video has no subtitles at all, the script exits with an error

## Usage

### Get Transcript

```bash
python3 {baseDir}/scripts/get_transcript.py "<YouTube URL>"
```

**What it does:**
1. Extracts the video ID from the URL
2. Calls `youtube-transcript-api` to list available transcripts (priority: English manual > English auto > any manual > any auto)
3. Fetches transcript entries and formats them into clean paragraphs
4. Prints to stdout

**Output:** Plain English (or whatever language the video has). No timestamps, no VTT markup.

### Example Workflow

1. Get the transcript:
   `python3 {baseDir}/scripts/get_transcript.py "<YouTube URL>"`
2. Read the full output
3. Summarize, answer questions, or extract key information for the user

## Notes

- **Language handling:** Script prioritizes English. If no English transcript exists, it falls back to whatever language the video has — English-speaking users will receive the raw foreign-language transcript and should summarize/translate it themselves
- **No transcript available:** Exit code 1 with message "No transcript found for this video"
- **Transcripts disabled:** Exit code 1 with message "Transcripts are disabled for this video"
- **Transcription quality:** Auto-generated captions may contain errors; manually created captions are more accurate
- **youtube-transcript-api** does NOT require a JS runtime or browser — it uses YouTube's internal transcript API, making it more reliable than `yt-dlp` for caption retrieval
