import os
import re

# Function to extract numbers from filenames
def extract_number_from_filename(filename):
    # Use regex to find numbers in the filename
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else None  # Return None if no number is found

# Function to merge all .txt files in the directory into one file, sorted by numbers in filenames
def merge_txt_files_by_number(directory, output_file):
    # Get all .txt files in the directory
    txt_files = [f for f in os.listdir(directory) if f.endswith(".txt")]

    # Filter and sort files by the numbers extracted from their filenames, skipping those without a number
    sorted_txt_files = sorted([f for f in txt_files if extract_number_from_filename(f) is not None], 
                              key=lambda f: extract_number_from_filename(f))

    # Open the output file in write mode
    with open(output_file, 'w') as outfile:
        # Loop through the sorted .txt files and append their contents
        for filename in sorted_txt_files:
            file_path = os.path.join(directory, filename)
            print(f"Processing {file_path}...")

            # Open each .txt file and append its contents to the output file
            with open(file_path, 'r') as infile:
                # Read and clean each line in the file, removing empty lines
                cleaned_lines = [line.strip() for line in infile if line.strip()]
                
                # Write the cleaned content to the output file without adding extra newlines
                if cleaned_lines:
                    outfile.write("\n".join(cleaned_lines) + "\n")
                
    print(f"All .txt files with numbers in their filenames have been merged into {output_file}, without empty lines.")

# Example usage
if __name__ == "__main__":
    # Directory where the .txt files are stored
    directory = "."
    
    # Output file to store the merged content
    output_file = os.path.join(directory, "script.txt")
    
    # Merge all .txt files in the directory into script.txt, sorted by numbers in filenames
    merge_txt_files_by_number(directory, output_file)
