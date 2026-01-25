# Video and Audio Transcriber with MLX Whisper

This Python script allows you to transcribe video or audio files by extracting audio, splitting it into manageable chunks, and then transcribing each chunk using MLX Whisper with Metal GPU acceleration. Finally, it combines all transcriptions into a single text file.

## Features

-   **Apple Silicon Optimized**: Uses MLX Whisper for Metal GPU acceleration on Apple Silicon Macs.
-   **Handles Video and Audio**: Works with video files (mp4, mov, avi) and audio files (mp3, m4a).
-   **Audio Extraction**: Extracts audio from various video formats (supported by `ffmpeg`) to an MP3 file.
-   **Audio Conversion**: Converts M4A files to MP3 for consistent processing.
-   **Audio Chunking**: Splits the audio into 10-minute MP3 chunks to manage memory and processing for large files.
-   **Whisper Transcription**: Utilizes MLX Whisper models from HuggingFace (defaults to `small.en`, configurable via CLI) to transcribe each audio chunk.
-   **Combined Transcript**: Merges all individual chunk transcriptions into a single, comprehensive text.
-   **Temporary File Management**: Automatically creates and cleans up temporary audio files and chunks.
-   **Output to File**: Saves the final transcript to a `.txt` file named after the input file.

## Prerequisites

Before running the script, ensure you have the following:

*   **Apple Silicon Mac**: This tool uses MLX which requires Apple Silicon (M1/M2/M3/M4).
*   **Python 3.10+**: The project specifies Python 3.14, but should work with 3.10 and newer.
*   **uv**: A fast Python package installer and resolver. (Install via https://docs.astral.sh/uv/getting-started/installation/)
*   **ffmpeg**: Essential for audio and video processing by `imageio-ffmpeg` and `pydub`. You can install it via your system's package manager (e.g., `brew install ffmpeg` on macOS).

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
    - `tiny`, `tiny.en`
    - `base`, `base.en`
    - `small`, `small.en` (default)
    - `medium`, `medium.en`
    - `large-v3`
    - `turbo`, `large-v3-turbo`
    - `distil-large-v3`

The `.en` variants are English-only models that are faster and more accurate for English content. Larger models offer better accuracy but require more computational resources and memory.

**Supported Formats:**
- Video: `.mp4`, `.mov`, `.avi`
- Audio: `.mp3`, `.m4a`

**Examples:**

```bash
# Transcribe a video file using the default 'small.en' model
uv run transcript videos/my_conference_talk.mp4

# Transcribe an audio file using the 'tiny' model for faster results
uv run transcript audio/podcast_episode.mp3 -model tiny

# Transcribe using the turbo model
uv run transcript audio/interview.m4a -model turbo
```

The script will print progress updates to the console. On first run with a model, it will download the model from HuggingFace. Once finished, a text file (e.g., `my_conference_talk.txt` or `podcast_episode.txt`) containing the full transcription will be created in the same directory where you ran the script.

## Customization

-   **Chunk Size**: The audio is chunked into approximately 10-minute segments. While the `chunk_audio` function has a `chunk_size_mb` parameter, the current implementation hardcodes a 10-minute duration. You can adjust the `chunk_length_ms` variable in the `chunk_audio` function in `transcribe_video.py` if you need different chunking behavior.
