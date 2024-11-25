import os
import requests
from urllib.parse import urlparse

# Function to download the file and save it in the desired folder structure
def download_file(url, base_dir, cookie):
    try:
        # Prepare the headers with the cookie
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        
        # Include the authentication cookie
        cookies = {
            '_vercel_jwt': cookie  # Replace with the actual cookie name and value
        }
        
        # Send a GET request to download the file with the authentication cookie
        response = requests.get(url, headers=headers, cookies=cookies)
        response.raise_for_status()  # Check if the request was successful

        # Parse the URL to get the file name and path
        parsed_url = urlparse(url)
        # Remove 'http://' or 'https://' and split path components
        path_parts = parsed_url.path.strip('/').split('/')

        # Create folder structure based on URL path
        file_path = os.path.join(base_dir, *path_parts[:-1])  # All parts except last for directories
        file_name = path_parts[-1]  # The last part is the file name

        # Make the directories if they don't exist
        os.makedirs(file_path, exist_ok=True)

        # Save the content to the file
        file_full_path = os.path.join(file_path, file_name)
        with open(file_full_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Downloaded: {file_full_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Function to read URLs from a .txt file and download them
def download_files_from_txt(txt_file, base_dir, cookie):
    with open(txt_file, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()  # Remove any leading/trailing spaces or newlines
            if url:
                download_file(url, base_dir, cookie)

if __name__ == "__main__":
    # Path to your .txt file containing the URLs
    txt_file = 'urls.txt'
    # Base directory where the files will be saved
    base_dir = 'downloaded_files'

    # The authentication cookie value (replace this with your actual cookie value)
    cookie_value = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI4SXZUNldhYmR2NXFCRTluRm5zTnlDRTQiLCJpYXQiOjE3MzI1MjQwMTgsIm93bmVySWQiOiJ0ZWFtX3drVjR1MkVqYld4WTZkUWM2RG82SkNKciIsImF1ZCI6ImVuZ2xpc2gtZmxvdy1zdG9yYWdlLWVvNWlodjAzNy1maW5zLXByb2plY3RzLWE1ZTZmMGE2LnZlcmNlbC5hcHAiLCJ1c2VybmFtZSI6ImZpbnN0YXJzMSIsInN1YiI6InNzby1wcm90ZWN0aW9uIn0.oNO0LLhAsFzobxe7z6HzhgUFy1a7lVSA-jrcRZbADzg'

    # Start downloading the files with the cookie for authentication
    download_files_from_txt(txt_file, base_dir, cookie_value)
