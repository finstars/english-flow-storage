import os
import sys
import requests
import shutil
from pydub import AudioSegment

key = "sk_714da4661a8595a92693df2fb45be06c5ba73d30626c390e"

voices = {
    "American": {
        "Male": "", # Bill - Health Nutrition Videos
        "Female": "" # Brittney Hart - Social Media Voice - Fun, Youthful & Informative
    },
    "British": {
        "Male": "", # Johnny Kid  - Serious
        "Female": "" # Ana
    },
    "Canadian": {
        "Male": "", # Haseeb - Canadian Narration
        "Female": "" # Danielle - Canadian Narrator
    },
    "Australian": {
        "Male": "", # Will - Young Australian Male
        "Female": "" # Maya - Young Australian Female
    },
}

def generate_audio(voice, text, path, file_number):
    text = text.strip()

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": key,
    }

    data = {
        "text": f"  {text}  ",
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
        },
    }

    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    response = requests.post(url, json=data, headers=headers, stream=True)
    if response.status_code == 200:
        with open(f"{path}/{file_number}.mp3", 'wb') as writer:
            for chunk in response.iter_content(chunk_size=8192):
                writer.write(chunk)
        print(f"{text}.mp3 downloaded successfully!")
    else:
        print(f"Error downloading {text}.mp3", response.status_code,
              response.text)
        sys.exit(1)

def get_mp3_files(directory):
    # Get a list of all files in the directory ending with .mp3
    files = [
        os.path.join(directory, file) for file in os.listdir(directory)
        if file.endswith('.mp3')
    ]
    # Sort the files alphabetically
    files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))

    return files

def merge_mp3_files(file_list, output_file, silence_duration_ms=500):
    # Create an empty AudioSegment
    combined = AudioSegment.empty()

    # Generate silence
    silence = AudioSegment.silent(duration=silence_duration_ms)

    # Iterate through the list of files
    for file in file_list:
        # Load the audio file
        audio = AudioSegment.from_mp3(file)

        # Append the audio file to the combined audio with silence in between
        combined += audio + silence

    # Export the combined audio
    combined.export(output_file, format="mp3")

# process_script('./script.txt')

input_files = get_mp3_files("./script")
merge_mp3_files(input_files, "./script.mp3")

# process_script('./lesson.txt')

# input_files = get_mp3_files("./lesson")
# merge_mp3_files(input_files, "./lesson.mp3")
