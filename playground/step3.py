import os
import whisper

# Function to transcribe the audio from an mp4 file to text using Whisper
def transcribe_audio_to_text(mp4_file, output_txt_file, model):
    try:
        print(f"Transcribing {mp4_file}...")
        # Use Whisper to transcribe the audio
        result = model.transcribe(mp4_file)
        text = result['text']
        
        # Write the transcription to the txt file
        with open(output_txt_file, 'w') as txt_file:
            txt_file.write(text)
        print(f"Transcription for {mp4_file} saved to {output_txt_file}.")
    except Exception as e:
        print(f"Error transcribing {mp4_file}: {e}")

# Main function to go through each mp4 file and transcribe it
def transcribe_all_clips(directory):
    # Load the Whisper model (you can use "base", "small", "medium", "large")
    model = whisper.load_model("base")

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.startswith("output_clip_") and filename.endswith(".mp4"):
            mp4_file = os.path.join(directory, filename)
            output_txt_file = os.path.join(directory, f"{filename.replace('.mp4', '')}.txt")
            
            # Transcribe the audio to text
            transcribe_audio_to_text(mp4_file, output_txt_file, model)

# Example usage
if __name__ == "__main__":
    # Directory where the output_clip_*.mp4 files are stored
    directory = "."
    
    # Transcribe all clips in the directory
    transcribe_all_clips(directory)
