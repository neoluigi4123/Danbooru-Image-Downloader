import os
import requests

def download_images(tag, num_images, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    url = 'https://danbooru.donmai.us/posts.json'
    images_downloaded = 0
    page = 1

    while images_downloaded < num_images:
        params = {
            'tags': tag,
            'limit': 200,  # Fetch maximum allowed per page
            'page': page
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        posts = response.json()

        # Break if no more posts are available
        if not posts:
            print("No more posts available.")
            break

        for post in posts:
            if 'file_url' in post and images_downloaded < num_images:
                image_url = post['file_url']
                image_name = os.path.basename(image_url)
                image_path = os.path.join(save_dir, image_name)

                try:
                    image_response = requests.get(image_url)
                    image_response.raise_for_status()

                    with open(image_path, 'wb') as image_file:
                        image_file.write(image_response.content)
                    images_downloaded += 1
                    print(f'Downloaded {image_name} ({images_downloaded}/{num_images})')
                except requests.RequestException as e:
                    print(f"Failed to download {image_url}: {e}")

        # Increment the page number to fetch the next set of images
        page += 1

    print(f"Downloaded {images_downloaded} images out of {num_images} requested.")

if __name__ == '__main__':
    tag = 'mario'  # Replace with your desired tag
    num_images = 500  # Replace with the number of images you want to download
    save_dir = r'E:\images'  # Replace with your desired save directory

    download_images(tag, num_images, save_dir)
