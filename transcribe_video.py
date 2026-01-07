
import argparse
import os
import tempfile
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import whisper

def extract_audio(video_path, audio_path):
    """Extracts audio from a video file and saves it as an MP3."""
    print(f"Extracting audio from {video_path}...")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    print(f"Audio extracted and saved to {audio_path}")

def chunk_audio(audio_path, chunk_folder, chunk_size_mb=10):
    """Chunks an audio file into smaller pieces of a given size."""
    print(f"Chunking audio file: {audio_path}")
    audio = AudioSegment.from_mp3(audio_path)
    chunk_length_ms = (chunk_size_mb * 1024 * 1024) / (audio.frame_rate * audio.frame_width * audio.channels) * 1000
    
    # After some testing, the above calculation is not accurate, so we will use a more direct way
    # A 128 kbps MP3 file is approximately 1 MB per minute.
    # So, 10MB is approximately 10 minutes or 600,000 ms.
    chunk_length_ms = 10 * 60 * 1000 # 10 minutes
    
    chunks = []
    for i, chunk in enumerate(audio[::chunk_length_ms]):
        chunk_path = os.path.join(chunk_folder, f"chunk_{i}.mp3")
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)
        print(f"Exported chunk: {chunk_path}")
    return chunks

def transcribe_chunks(chunks, model):
    """Transcribes a list of audio chunks."""
    transcripts = []
    for chunk_path in chunks:
        print(f"Transcribing {chunk_path}...")
        result = model.transcribe(chunk_path)
        transcripts.append(result["text"])
        print(f"Finished transcribing {chunk_path}")
    return transcripts

def main():
    """Main function to transcribe a video file."""
    parser = argparse.ArgumentParser(description="Transcribe a video file using OpenAI Whisper.")
    parser.add_argument("video_path", help="Path to the video file.")
    args = parser.parse_args()

    if not os.path.exists(args.video_path):
        print(f"Error: Video file not found at {args.video_path}")
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        audio_path = os.path.join(temp_dir, "extracted_audio.mp3")
        
        try:
            # 1. Extract audio
            extract_audio(args.video_path, audio_path)
            
            # 2. Chunk audio
            chunk_folder = os.path.join(temp_dir, "chunks")
            os.makedirs(chunk_folder, exist_ok=True)
            chunks = chunk_audio(audio_path, chunk_folder)
            
            # 3. Transcribe chunks
            print("Loading Whisper model...")
            model = whisper.load_model("base")
            print("Whisper model loaded.")
            
            transcripts = transcribe_chunks(chunks, model)
            
            # 4. Combine transcripts
            full_transcript = " ".join(transcripts)
            
            print("\n--- Full Transcript ---")
            print(full_transcript)
            
            # 5. Save transcript to a file
            transcript_filename = os.path.splitext(os.path.basename(args.video_path))[0] + ".txt"
            with open(transcript_filename, "w") as f:
                f.write(full_transcript)
            print(f"\nTranscript saved to {transcript_filename}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
