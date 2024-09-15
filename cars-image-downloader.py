import requests
from bs4 import BeautifulSoup
import os

# Function to download an image from a given URL and save it to the specified folder
def download_image(url, folder_path, file_name=None):
    # If the URL does not start with 'http', add 'https:' to the beginning
    if not url.startswith('http'):
        url = 'https:' + url
    # Send a request to download the image
    response = requests.get(url)
    # If the request is successful (status code 200)
    if response.status_code == 200:
        # If no file name is provided, extract the name from the URL
        if file_name is None:
            file_name = url.split('/')[-1]
        # Define the full file path for saving the image
        file_path = os.path.join(folder_path, file_name)
        # Save the image content to the specified file
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved as {file_path}")
    else:
        print(f"Image could not be downloaded: {url}")

# Function to get the URL of the first image from a Google search query
def get_first_image_url(search_query):
    # Define the User-Agent header to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    # Replace spaces in the search query with '+' for the URL
    search_query = search_query.replace(' ', '+')
    # Construct the Google Image search URL
    url = f"https://www.google.com/search?hl=en&tbm=isch&q={search_query}"

    # Send a request to Google Image search
    response = requests.get(url, headers=headers)
    # Parse the HTML response with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all img tags on the page
    image_tags = soup.find_all('img')
    if image_tags:
        # Select the second img tag as the first one is often not the desired image
        first_image_tag = image_tags[1]  # The first img tag is usually a logo or other element
        # Extract the image URL from the src attribute
        img_url = first_image_tag['src']
        # If the URL does not start with 'http', add 'https:' to the beginning
        if not img_url.startswith('http'):
            img_url = 'https:' + img_url
        return img_url
    return None

# Main function to run the script
def main():
    # List of search queries for car models
    search_queries = [
        "Alfa Romeo145",
        "Alfa Romeo146",
        "Alfa Romeo147",
        "Toyota Starlet",
        "Toyota Supra",
        "Toyota Urban Cruiser",
        "Toyota Verso"
    ]

    # Define the folder path where images will be saved (on Desktop in 'Car_Images3' folder)
    folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Car_Images3')
    os.makedirs(folder_path, exist_ok=True)
    
    # Iterate through each search query
    for query in search_queries:
        print(f"Searching: {query}")
        # Get the first image URL for the current query
        first_image_url = get_first_image_url(query)
        
        # If an image URL is found, download the image
        if first_image_url:
            # Generate a filename based on the query (replace spaces and slashes with underscores)
            file_name = f"{query.replace(' ', '_').replace('/', '_')}.jpg"
            # Download and save the image
            download_image(first_image_url, folder_path, file_name)
        else:
            print(f"No image found for {query}.")

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
