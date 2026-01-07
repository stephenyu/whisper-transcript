# Video Transcriber with OpenAI Whisper

This Python script allows you to extract audio from a video file, split it into manageable chunks, and then transcribe each chunk using OpenAI's Whisper model. Finally, it combines all transcriptions into a single text file.

## Features

-   **Audio Extraction**: Extracts audio from various video formats (supported by `moviepy`) to an MP3 file.
-   **Audio Chunking**: Splits the extracted audio into 10-minute MP3 chunks to manage memory and processing for large files.
-   **Whisper Transcription**: Utilizes the local `base` OpenAI Whisper model to transcribe each audio chunk.
-   **Combined Transcript**: Merges all individual chunk transcriptions into a single, comprehensive text.
-   **Temporary File Management**: Automatically creates and cleans up temporary audio files and chunks.
-   **Output to File**: Saves the final transcript to a `.txt` file named after the input video.

## Prerequisites

Before running the script, ensure you have the following installed:

*   **Python 3.10+**: The project specifies Python 3.14, but should work with 3.10 and newer.
*   **uv**: A fast Python package installer and resolver.
*   **ffmpeg**: Essential for audio and video processing by `moviepy` and `pydub`. You can install it via your system's package manager (e.g., `brew install ffmpeg` on macOS, `sudo apt-get install ffmpeg` on Debian/Ubuntu, `choco install ffmpeg` on Windows).

## Installation

1.  **Clone the repository (or ensure you have `transcribe_video.py` and `pyproject.toml`):**
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

To transcribe a video file, run the script from your terminal:

```bash
python transcribe_video.py <path_to_your_video_file>
```

Replace `<path_to_your_video_file>` with the actual path to the video you want to transcribe (e.g., `my_movie.mp4`, `videos/presentation.avi`).

**Example:**

```bash
python transcribe_video.py videos/my_conference_talk.mp4
```

The script will print progress updates to the console. Once finished, a text file (e.g., `my_conference_talk.txt`) containing the full transcription will be created in the same directory where you ran the script.

## OpenAI API Key

This script uses the **local `base` Whisper model** and therefore **does not require an OpenAI API key** for transcription.

If you were to use the paid OpenAI Whisper API (which is a separate service not directly used by this script's `whisper.load_model()` functionality), you would typically provide your API key by setting the `OPENAI_API_KEY` environment variable:

```bash
export OPENAI_API_KEY="YOUR_API_KEY_HERE"
```

## Customization

-   **Whisper Model**: The script currently uses the `base` Whisper model. You can change this to `tiny`, `small`, `medium`, or `large` (or their `.en` variants for English-only models) by modifying the `whisper.load_model("base")` line in `transcribe_video.py`. Larger models offer better accuracy but require more computational resources and VRAM.

    ```python
    # Example to use a larger model
    model = whisper.load_model("medium")
    ```

-   **Chunk Size**: The audio is chunked into approximately 10-minute segments. While the `chunk_audio` function has a `chunk_size_mb` parameter, the current implementation hardcodes a 10-minute duration. You can adjust the `chunk_length_ms` variable in the `chunk_audio` function in `transcribe_video.py` if you need different chunking behavior.
