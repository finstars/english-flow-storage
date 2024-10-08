import os

# Function to rename files in the current directory
def rename_files():
    # Get the list of all files in the current directory
    files = os.listdir()

    # Loop through each file in the directory
    for file_name in files:
        # Check if the file name contains the patterns to be removed
        if "output_clip_" in file_name or "_last_frame" in file_name:
            # Generate the new file name by removing the patterns
            new_file_name = file_name.replace("output_clip_", "").replace("_last_frame", "")
            # Rename the file
            os.rename(file_name, new_file_name)
            print(f'Renamed: "{file_name}" to "{new_file_name}"')

# Run the renaming function
if __name__ == "__main__":
    rename_files()
