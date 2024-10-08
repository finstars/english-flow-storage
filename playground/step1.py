from moviepy.editor import VideoFileClip

# Function to convert timestamp "MM:SS" to seconds
def convert_timestamp_to_seconds(timestamp):
    try:
        minutes, seconds = map(int, timestamp.split(":"))
        return minutes * 60 + seconds
    except ValueError:
        print(f"Error: Invalid timestamp format '{timestamp}'. Expected format is MM:SS.")
        return None

# Function to read timestamps from a file
def read_timestamps_from_file(file_path):
    timestamps = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            timestamps.append(line.strip())  # Strip to remove any newlines or spaces
    return timestamps

# Function to split video based on the timestamps using VideoFileClip
def split_video_based_on_timestamps(video_file, timestamps, output_prefix="output_clip"):
    # Convert all timestamps to seconds
    timestamps_in_seconds = [convert_timestamp_to_seconds(ts) for ts in timestamps]

    # Filter out any None values (in case of invalid timestamps)
    timestamps_in_seconds = [ts for ts in timestamps_in_seconds if ts is not None]

    # Loop through timestamps and create subclips
    for i in range(len(timestamps_in_seconds) - 1):
        start_time = timestamps_in_seconds[i]
        end_time = timestamps_in_seconds[i + 1]
        
        # Ensure start_time and end_time are valid
        if start_time >= 0 and end_time > start_time:
            output_clip_name = f"{output_prefix}_{i + 1}.mp4"
            print(f"Processing: start_time = {start_time}, end_time = {end_time}")

            try:
                # Use VideoFileClip to extract the subclip
                with VideoFileClip(video_file) as video:
                    subclip = video.subclip(start_time, end_time)
                    subclip.write_videofile(output_clip_name, codec="libx264")
                print(f"Generated {output_clip_name} from {start_time} to {end_time} seconds.")
            except Exception as e:
                print(f"Error generating {output_clip_name}: {e}")
        else:
            print(f"Error: Invalid times for clip {i + 1}. start_time = {start_time}, end_time = {end_time}.")

# Example usage:
txt_file = "timestamps.txt"  # Path to your text file with timestamps
input_video = "vid.mp4"  # Path to your video file

# Read timestamps from file and split video based on them
timestamps = read_timestamps_from_file(txt_file)
split_video_based_on_timestamps(input_video, timestamps)
