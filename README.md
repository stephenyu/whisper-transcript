# Video and Audio Transcriber with OpenAI Whisper

This Python script allows you to transcribe video or audio files by extracting audio, splitting it into manageable chunks, and then transcribing each chunk using OpenAI's Whisper model. Finally, it combines all transcriptions into a single text file.

## Features

-   **Handles Video and Audio**: Works with video files (mp4, mov, avi) and audio files (mp3, m4a).
-   **Audio Extraction**: Extracts audio from various video formats (supported by `ffmpeg`) to an MP3 file.
-   **Audio Conversion**: Converts M4A files to MP3 for consistent processing.
-   **Audio Chunking**: Splits the audio into 10-minute MP3 chunks to manage memory and processing for large files.
-   **Whisper Transcription**: Utilizes OpenAI's Whisper model (defaults to `medium`, configurable via CLI) to transcribe each audio chunk.
-   **Combined Transcript**: Merges all individual chunk transcriptions into a single, comprehensive text.
-   **Temporary File Management**: Automatically creates and cleans up temporary audio files and chunks.
-   **Output to File**: Saves the final transcript to a `.txt` file named after the input file.

## Prerequisites

Before running the script, ensure you have the following installed:

*   **Python 3.10+**: The project specifies Python 3.14, but should work with 3.10 and newer.
*   **uv**: A fast Python package installer and resolver.
*   **ffmpeg**: Essential for audio and video processing by `imageio-ffmpeg` and `pydub`. You can install it via your system's package manager (e.g., `brew install ffmpeg` on macOS, `sudo apt-get install ffmpeg` on Debian/Ubuntu, `choco install ffmpeg` on Windows).

## Installation

1.  **Clone the repository:**
    ```bash
    # If this is a git repository
    # git clone <repository_url>
    # cd <repository_name>
    ```

2.  **Install dependencies using `uv`:**
    ```bash
    uv pip install -e .
    ```
    This command reads the `pyproject.toml` file and installs all required packages.

## Usage

To transcribe a video or audio file, run the script using `uv`:

```bash
uv run transcript <path_to_your_file> [-model <model_size>]
```

Replace `<path_to_your_file>` with the actual path to the video or audio file you want to transcribe.

**Options:**
- `-model`, `--model`: Specify the Whisper model size. Available models are:
    - `tiny`
    - `base`
    - `small`
    - `medium` (default)
    - `large`
    - (English-only variants are also supported: `tiny.en`, `base.en`, etc.)

Larger models offer better accuracy but require more computational resources and VRAM.

**Supported Formats:**
- Video: `.mp4`, `.mov`, `.avi`
- Audio: `.mp3`, `.m4a`

**Examples:**

```bash
# Transcribe a video file using the default 'medium' model
uv run transcript videos/my_conference_talk.mp4

# Transcribe an audio file using the 'tiny' model for faster results
uv run transcript audio/podcast_episode.mp3 -model tiny
```

The script will print progress updates to the console. Once finished, a text file (e.g., `my_conference_talk.txt` or `podcast_episode.txt`) containing the full transcription will be created in the same directory where you ran the script.

## Customization

-   **Chunk Size**: The audio is chunked into approximately 10-minute segments. While the `chunk_audio` function has a `chunk_size_mb` parameter, the current implementation hardcodes a 10-minute duration. You can adjust the `chunk_length_ms` variable in the `chunk_audio` function in `transcribe_video.py` if you need different chunking behavior.
