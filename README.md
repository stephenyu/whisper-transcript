# Video and Audio Transcriber with OpenAI Whisper

This Python script allows you to transcribe video or audio files by extracting audio, splitting it into manageable chunks, and then transcribing each chunk using OpenAI's Whisper model. Finally, it combines all transcriptions into a single text file.

## Features

-   **Handles Video and Audio**: Works with video files (mp4, mov, avi) and audio files (mp3, m4a).
-   **Audio Extraction**: Extracts audio from various video formats (supported by `moviepy`) to an MP3 file.
-   **Audio Conversion**: Converts M4A files to MP3 for consistent processing.
-   **Audio Chunking**: Splits the audio into 10-minute MP3 chunks to manage memory and processing for large files.
-   **Whisper Transcription**: Utilizes the local `base` OpenAI Whisper model to transcribe each audio chunk.
-   **Combined Transcript**: Merges all individual chunk transcriptions into a single, comprehensive text.
-   **Temporary File Management**: Automatically creates and cleans up temporary audio files and chunks.
-   **Output to File**: Saves the final transcript to a `.txt` file named after the input file.

## Prerequisites

Before running the script, ensure you have the following installed:

*   **Python 3.10+**: The project specifies Python 3.14, but should work with 3.10 and newer.
*   **uv**: A fast Python package installer and resolver.
*   **ffmpeg**: Essential for audio and video processing by `moviepy` and `pydub`. You can install it via your system's package manager (e.g., `brew install ffmpeg` on macOS, `sudo apt-get install ffmpeg` on Debian/Ubuntu, `choco install ffmpeg` on Windows).

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
uv run transcript <path_to_your_file>
```

Replace `<path_to_your_file>` with the actual path to the video or audio file you want to transcribe.

**Supported Formats:**
- Video: `.mp4`, `.mov`, `.avi`
- Audio: `.mp3`, `.m4a`

**Example:**

```bash
# Transcribe a video file
uv run transcript videos/my_conference_talk.mp4

# Transcribe an audio file
uv run transcript audio/podcast_episode.mp3
```

The script will print progress updates to the console. Once finished, a text file (e.g., `my_conference_talk.txt` or `podcast_episode.txt`) containing the full transcription will be created in the same directory where you ran the script.

## Customization

-   **Whisper Model**: The script currently uses the `base` Whisper model. You can change this to `tiny`, `small`, `medium`, or `large` (or their `.en` variants for English-only models) by modifying the `whisper.load_model("base")` line in `transcribe_video.py`. Larger models offer better accuracy but require more computational resources and VRAM.

    ```python
    # Example to use a larger model
    model = whisper.load_model("medium")
    ```

-   **Chunk Size**: The audio is chunked into approximately 10-minute segments. While the `chunk_audio` function has a `chunk_size_mb` parameter, the current implementation hardcodes a 10-minute duration. You can adjust the `chunk_length_ms` variable in the `chunk_audio` function in `transcribe_video.py` if you need different chunking behavior.
