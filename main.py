import os
import json
import os
import sys
import requests
import shutil
from pydub import AudioSegment

key = ""

voices = {
    "American": {
        "Male":
        "TX3LPaxmHKxFdv7VOQHJ",  # Alternative: Bill - Health Nutrition Videos
        "Female":
        "cgSgspJ2msm6clMCkdW9"  # Alternative: Brittney Hart - Social Media Voice - Fun, Youthful & Informative
    },
    "British": {
        "Male": "CYw3kZ02Hs0563khs1Fj",  # Alternative: Johnny Kid  - Serious
        "Female": "ThT5KcBeYPX3keUQqHPh"  # Alternative: Ana
    },
    # "Canadian": {
    #     "Male": "", # Haseeb - Canadian Narration
    #     "Female": "" # Danielle - Canadian Narrator
    # },
    # "Australian": {
    #     "Male": "IKne3meq5aSn9XLyUdCD", # Will - Young Australian Male
    #     "Female": "" # Maya - Young Australian Female
    # },
    # "Irish": "bVMeCyTHy58xNoL34h3p"
}


def generate_audio(voice, text, path, filename):
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
        with open(f"{path}/{filename}.mp3", 'wb') as writer:
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


def merge_mp3_files(file_list,
                    output_file,
                    silence_duration_ms=500,
                    mute_odd_even=None):
    # Create an empty AudioSegment
    combined = AudioSegment.empty()

    # Generate silence
    silence = AudioSegment.silent(duration=silence_duration_ms)

    # Iterate through the list of files
    for index, file in enumerate(file_list):
        # Load the audio file
        audio = AudioSegment.from_mp3(file)

        # Mute the audio if it matches the specified condition
        if (mute_odd_even == 'odd'
                and index % 2 != 0) or (mute_odd_even == 'even'
                                        and index % 2 == 0):
            audio = audio - 100

        # Append the audio file to the combined audio with silence in between
        combined += audio + silence

    # Export the combined audio
    combined.export(output_file, format="mp3")


def process_normal_directory(directory):
    lesson_path = os.path.join(directory, 'lesson.json')

    with open(lesson_path, 'r') as lesson_file:
        try:
            lesson_data = json.load(lesson_file)
            if 'lesson' in lesson_data and isinstance(lesson_data['lesson'],
                                                      list):
                for index, lesson_item in enumerate(lesson_data['lesson']):
                    if index != 4:
                        continue

                    voice1 = voices['American']['Male']
                    voice2 = voices['American']['Female']
                    voice3 = voices['British']['Male']
                    voice4 = voices['British']['Female']

                    generate_audio(voice1, lesson_item['text'], directory,
                                   f"American-Male-{index + 1}")
                    generate_audio(voice2, lesson_item['text'], directory,
                                   f"American-Female-{index + 1}")
                    generate_audio(voice3, lesson_item['text'], directory,
                                   f"British-Male-{index + 1}")
                    generate_audio(voice4, lesson_item['text'], directory,
                                   f"British-Female-{index + 1}")
            else:
                print(f"No valid 'lesson' key found or it is not an array.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")


def process_conversational_directory(directory):
    lesson_path = os.path.join(directory, 'lesson.json')

    with open(lesson_path, 'r') as lesson_file:
        try:
            lesson_data = json.load(lesson_file)
            if 'lesson' in lesson_data and isinstance(lesson_data['lesson'],
                                                      list):
                for index, lesson_item in enumerate(lesson_data['lesson']):

                    # print(json.dumps(lesson_item, indent=4))

                    # Create a folder for each lesson
                    american_male_path = os.path.join(directory, "American",
                                                      "Male")
                    american_female_path = os.path.join(
                        directory, "American", "Female")

                    brit_male_path = os.path.join(directory, "British", "Male")
                    brit_female_path = os.path.join(directory, "British",
                                                    "Female")

                    os.makedirs(brit_male_path, exist_ok=True)
                    os.makedirs(brit_female_path, exist_ok=True)

                    if 'conversation' in lesson_item and isinstance(
                            lesson_item['conversation'], list):
                        for conv_index, conversation in enumerate(
                                lesson_item['conversation']):
                            print(json.dumps(conversation['text'], indent=4))
                            print(lesson_path)

                            voice1 = voices['American']['Male']
                            voice2 = voices['American']['Female']
                            voice3 = voices['British']['Male']
                            voice4 = voices['British']['Female']

                            generate_audio(voice1, conversation['text'],
                                           american_male_path, conv_index + 1)
                            generate_audio(voice2, conversation['text'],
                                           american_female_path,
                                           conv_index + 1)
                            generate_audio(voice3, conversation['text'],
                                           brit_male_path, conv_index + 1)
                            generate_audio(voice4, conversation['text'],
                                           brit_female_path, conv_index + 1)
                    else:
                        print(
                            "No valid 'conversation' key found or it is not an array."
                        )

                    # 1. Listen
                    merge_mp3_files(
                        get_mp3_files(american_male_path),
                        os.path.join(directory, f"American-Male-1.mp3"))

                    merge_mp3_files(
                        get_mp3_files(american_female_path),
                        os.path.join(directory, f"American-Female-1.mp3"))

                    merge_mp3_files(
                        get_mp3_files(brit_male_path),
                        os.path.join(directory, f"British-Male-1.mp3"))

                    merge_mp3_files(
                        get_mp3_files(brit_female_path),
                        os.path.join(directory, f"British-Female-1.mp3"))

                    # 2. Odd
                    merge_mp3_files(
                        get_mp3_files(american_male_path),
                        os.path.join(directory, f"American-Male-2.mp3"), 500,
                        'odd')

                    merge_mp3_files(
                        get_mp3_files(american_female_path),
                        os.path.join(directory, f"American-Female-2.mp3"), 500,
                        'odd')

                    merge_mp3_files(
                        get_mp3_files(brit_male_path),
                        os.path.join(directory, f"British-Male-2.mp3"), 500,
                        'odd')

                    merge_mp3_files(
                        get_mp3_files(brit_female_path),
                        os.path.join(directory, f"British-Female-2.mp3"), 500,
                        'odd')

                    # 3. Even
                    merge_mp3_files(
                        get_mp3_files(american_male_path),
                        os.path.join(directory, f"American-Male-3.mp3"), 500,
                        'even')

                    merge_mp3_files(
                        get_mp3_files(american_female_path),
                        os.path.join(directory, f"American-Female-3.mp3"), 500,
                        'even')

                    merge_mp3_files(
                        get_mp3_files(brit_male_path),
                        os.path.join(directory, f"British-Male-3.mp3"), 500,
                        'even')

                    merge_mp3_files(
                        get_mp3_files(brit_female_path),
                        os.path.join(directory, f"British-Female-3.mp3"), 500,
                        'even')

                    break
            else:
                print(f"No valid 'lesson' key found or it is not an array.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")


if __name__ == "__main__":
    base_directory = './lessons/conversational-english-lessons/teasing-mom'

    if "conversational-english-lessons" in base_directory:
        process_conversational_directory(base_directory)
    else:
        process_normal_directory(base_directory)
