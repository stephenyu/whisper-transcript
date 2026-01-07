
import argparse
import os
import tempfile
from pydub import AudioSegment
from moviepy import VideoFileClip
import whisper
import shutil

def extract_audio(video_path, audio_path):
    """Extracts audio from a video file and saves it as an MP3."""
    print(f"Extracting audio from {video_path}...")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, codec='mp3')
    print(f"Audio extracted and saved to {audio_path}")

def chunk_audio(audio_path, chunk_folder, chunk_size_mb=10):
    """Chunks an audio file into smaller pieces of a given size."""
    print(f"Chunking audio file: {audio_path}")
    
    file_extension = os.path.splitext(audio_path)[1].lower()
    if file_extension == '.mp3':
        audio = AudioSegment.from_mp3(audio_path)
    elif file_extension == '.m4a':
        audio = AudioSegment.from_file(audio_path, "m4a")
    else:
        # Attempt to load with ffmpeg for other formats
        audio = AudioSegment.from_file(audio_path)

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
    """Main function to transcribe a video or audio file."""
    parser = argparse.ArgumentParser(description="Transcribe a video or audio file using OpenAI Whisper.")
    parser.add_argument("input_path", help="Path to the video or audio file (mp4, mov, avi, mp3, m4a).")
    args = parser.parse_args()

    if not os.path.exists(args.input_path):
        print(f"Error: File not found at {args.input_path}")
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        
        try:
            file_extension = os.path.splitext(args.input_path)[1].lower()
            temp_audio_path = os.path.join(temp_dir, "source_audio" + file_extension)

            if file_extension in ['.mp4', '.mov', '.avi']:
                # 1. Extract audio from video
                audio_path_for_chunking = os.path.join(temp_dir, "extracted_audio.mp3")
                extract_audio(args.input_path, audio_path_for_chunking)
            elif file_extension == '.mp3':
                # Copy mp3 to temp dir to work with it
                print(f"Copying {args.input_path} to temporary directory...")
                shutil.copy(args.input_path, temp_audio_path)
                audio_path_for_chunking = temp_audio_path
            elif file_extension == '.m4a':
                # Convert m4a to mp3 in temp dir
                print(f"Converting {args.input_path} to MP3...")
                audio_path_for_chunking = os.path.join(temp_dir, "converted_audio.mp3")
                audio = AudioSegment.from_file(args.input_path, "m4a")
                audio.export(audio_path_for_chunking, format="mp3")
                print(f"Converted and saved to {audio_path_for_chunking}")
            else:
                print(f"Error: Unsupported file type '{file_extension}'. Please use a video (mp4, mov, avi) or audio (mp3, m4a) file.")
                return

            # 2. Chunk audio
            chunk_folder = os.path.join(temp_dir, "chunks")
            os.makedirs(chunk_folder, exist_ok=True)
            chunks = chunk_audio(audio_path_for_chunking, chunk_folder)
            
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
            transcript_filename = os.path.splitext(os.path.basename(args.input_path))[0] + ".txt"
            with open(transcript_filename, "w") as f:
                f.write(full_transcript)
            print(f"\nTranscript saved to {transcript_filename}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
