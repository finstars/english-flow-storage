import os

def remove_txt_files():
    # Get the current directory
    current_dir = os.getcwd()

    # Loop through all files in the directory
    for filename in os.listdir(current_dir):
        # Check if the file ends with .txt but is not script.txt
        if filename.endswith('.txt') and filename != 'script.txt':
            file_path = os.path.join(current_dir, filename)
            try:
                # Remove the file
                os.remove(file_path)
                print(f"Removed: {filename}")
            except Exception as e:
                print(f"Error removing {filename}: {e}")

if __name__ == "__main__":
    remove_txt_files()
