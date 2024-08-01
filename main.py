import os
import json
import os
import sys
import requests
import shutil
# from pydub import AudioSegment

key = "sk_714da4661a8595a92693df2fb45be06c5ba73d30626c390e"

voices = {
    # "American": {
    #     "Male": "", # Bill - Health Nutrition Videos
    #     "Female": "" # Brittney Hart - Social Media Voice - Fun, Youthful & Informative
    # },
    "British": {
        "Male": "", # Johnny Kid  - Serious
        "Female": "" # Ana
    },
    # "Canadian": {
    #     "Male": "", # Haseeb - Canadian Narration
    #     "Female": "" # Danielle - Canadian Narrator
    # },
    # "Australian": {
    #     "Male": "", # Will - Young Australian Male
    #     "Female": "" # Maya - Young Australian Female
    # },
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

def scan_directory(directory):
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")
            if f == 'lesson.json':
                lesson_path = os.path.join(root, f)
                print(f"{sub_indent}Opening {lesson_path}")
                with open(lesson_path, 'r') as lesson_file:
                    try:
                        lesson_data = json.load(lesson_file)
                        if 'lesson' in lesson_data and isinstance(lesson_data['lesson'], list):
                            for index, lesson_item in enumerate(lesson_data['lesson']):
                                print(f"{sub_indent} Lesson {index + 1}:")
                                # print(json.dumps(lesson_item, indent=4))

                                 # Create a folder for each lesson
                                conv_folder_name = str(index + 1)
                                conv_folder_path = os.path.join(root, conv_folder_name)
                                lesson_path = os.path.join(conv_folder_path, f"{index + 1}.mp3")
                                brit_male_path = os.path.join(conv_folder_path, "British", "Male")
                                brit_female_path = os.path.join(conv_folder_path, "British", "Female")
                                if not os.path.exists(conv_folder_path):
                                    # os.makedirs(conv_folder_path)
                                    os.makedirs(brit_male_path)
                                    os.makedirs(brit_female_path)
                                    print(f"{sub_indent}    Created folder: {conv_folder_path}")
                                
                                if 'conversation' in lesson_item and isinstance(lesson_item['conversation'], list):
                                    for conv_index, conversation in enumerate(lesson_item['conversation']):
                                        print(json.dumps(conversation['text'], indent=4))
                                        print(lesson_path)

                                        voice1 = voices['British']['Male']
                                        voice2 = voices['British']['Female']

                                        generate_audio(voice1, conversation['text'], brit_male_path, conv_index + 1)
                                        generate_audio(voice2, conversation['text'], brit_female_path, conv_index + 1)
                                else:
                                    print(f"{sub_indent}    No valid 'conversation' key found or it is not an array.")

                                merge_mp3_files(get_mp3_files(brit_male_path), lesson_path)

                                break
                        else:
                            print(f"{sub_indent} No valid 'lesson' key found or it is not an array.")
                    except json.JSONDecodeError as e:
                        print(f"{sub_indent} Error decoding JSON: {e}")

if __name__ == "__main__":
    base_directory = './lessons/conversational-english-lessons'
    scan_directory(base_directory)
