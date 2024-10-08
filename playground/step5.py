import os

# Get the current working directory
current_directory = os.getcwd()

# Loop through all files in the current directory
for filename in os.listdir(current_directory):
    # Check if the file contains "output_clip_" or "_last_frame"
    if "clip_" in filename or "_last_frame" in filename:
        # Remove "output_clip_" and "_last_frame" from the filename
        new_filename = filename.replace("clip_", "").replace("_last_frame", "")
        
        # Get the full paths for renaming
        old_filepath = os.path.join(current_directory, filename)
        new_filepath = os.path.join(current_directory, new_filename)
        
        # Rename the file
        os.rename(old_filepath, new_filepath)
        print(f'Renamed: "{filename}" to "{new_filename}"')

print("Renaming complete.")
