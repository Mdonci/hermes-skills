#!/usr/bin/env python3
"""
Fetch YouTube video transcript using youtube-transcript-api.
Usage: python3 get_transcript.py "<YouTube URL>"
"""

import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    NotTranslatable,
)


def extract_video_id(url: str) -> str:
    """Extract video ID from a YouTube URL."""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'^([0-9A-Za-z_-]{11})$',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def clean_transcript_text(entries: list) -> str:
    """
    Convert transcript entries into clean paragraphs.
    Handles both dict-style entries (from fetch()) and attribute-style
    entries (FetchedTranscriptSnippet from youtube-transcript-api >= 0.6).
    """
    texts = []
    for entry in entries:
        # Support both dict-like and attribute-based entry objects
        if isinstance(entry, dict):
            text = entry.get('text', '')
        else:
            text = getattr(entry, 'text', '')

        text = text.strip()
        if not text:
            continue
        # Skip music symbol placeholders
        if text.count('[') > 3 or text.count('♪') > 5:
            continue
        texts.append(text)

    if not texts:
        return ''

    full = ' '.join(texts)

    # Split into sentences and regroup into paragraphs
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÚJÖV])', full)

    paragraphs = []
    current = []
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        current.append(sent)
        if len(current) >= 5 or len(' '.join(current)) > 600:
            paragraphs.append(' '.join(current))
            current = []
    if current:
        paragraphs.append(' '.join(current))

    return '\n\n'.join(paragraphs)


def fetch_any_transcript(video_id: str):
    """
    Try to get a transcript for a video. Returns (entries, language_code).
    Priority: English manual > English auto > any manual > any auto.
    """
    api = YouTubeTranscriptApi()

    # Priority order for languages
    lang_priority = ['en', 'en-US', 'en-GB']

    # First try to find a manually-created transcript
    try:
        tl = api.list(video_id)
        try:
            t = tl.find_transcript(lang_priority)
            return t.fetch(), t.language_code
        except NoTranscriptFound:
            pass

        # Try any manually-created transcript
        for t in tl:
            if not t.is_generated:
                return t.fetch(), t.language_code

        # Try any auto-generated transcript
        for t in tl:
            if t.is_generated:
                return t.fetch(), t.language_code

    except Exception:
        pass

    raise NoTranscriptFound(video_id)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 get_transcript.py <YouTube URL>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]

    try:
        video_id = extract_video_id(url)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        entries, lang = fetch_any_transcript(video_id)
        transcript = clean_transcript_text(entries)

    except TranscriptsDisabled:
        print("Error: Transcripts are disabled for this video.", file=sys.stderr)
        sys.exit(1)
    except NoTranscriptFound:
        print(
            "Error: No transcript found for this video. "
            "The video may not have captions or auto-generated subtitles.",
            file=sys.stderr,
        )
        sys.exit(1)
    except VideoUnavailable:
        print("Error: Video is unavailable or private.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error fetching transcript: {e}", file=sys.stderr)
        sys.exit(1)

    if not transcript.strip():
        print("Error: Transcript was empty.", file=sys.stderr)
        sys.exit(1)

    print(transcript)


if __name__ == '__main__':
    main()
