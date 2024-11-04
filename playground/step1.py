from moviepy.editor import VideoFileClip

# Function to convert timestamp "MM:SS" to seconds
def convert_timestamp_to_seconds(timestamp):
    try:
        minutes, seconds = map(int, timestamp.split(":"))
        return minutes * 60 + seconds
    except ValueError:
        print(f"Error: Invalid timestamp format '{timestamp}'. Expected format is MM:SS.")
        return None

# Function to read timestamp ranges from a file in "start-end" format
def read_timestamp_ranges_from_file(file_path):
    timestamp_ranges = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Split the line into start and end timestamps
            range_parts = line.strip().split("-")
            if len(range_parts) == 2:
                start, end = range_parts
                timestamp_ranges.append((start, end))
            else:
                print(f"Error: Invalid range format '{line.strip()}'. Expected format is start-end.")
    return timestamp_ranges

# Function to split video based on the timestamp ranges
def split_video_based_on_ranges(video_file, timestamp_ranges, output_prefix="output_clip"):
    for i, (start, end) in enumerate(timestamp_ranges):
        # Convert start and end timestamps to seconds
        start_time = convert_timestamp_to_seconds(start)
        end_time = convert_timestamp_to_seconds(end)

        # Ensure start_time and end_time are valid
        if start_time is not None and end_time is not None and end_time > start_time:
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
txt_file = "timestamps.txt"  # Path to your text file with timestamp ranges
input_video = "vid.mp4"  # Path to your video file

# Read timestamp ranges from file and split video based on them
timestamp_ranges = read_timestamp_ranges_from_file(txt_file)
split_video_based_on_ranges(input_video, timestamp_ranges)
