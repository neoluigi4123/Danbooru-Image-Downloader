import os
import asyncio
import aiohttp
import hashlib
from tkinter import Tk, Label, Entry, Button, filedialog, BooleanVar, StringVar, IntVar, messagebox
from tkinter import DISABLED, NORMAL
from tkinter import ttk
from pygelbooru import Gelbooru
import threading
import subprocess

# Global event to stop download
stop_event = threading.Event()

# Function to read API key and user ID from token.txt file
def load_token():
    if os.path.exists('token.txt'):
        with open('token.txt', 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                api_key_var.set(lines[0].strip())
                user_id_var.set(lines[1].strip())

# Function to save API key and user ID to token.txt file
def save_token(api_key, user_id):
    with open('token.txt', 'w') as file:
        file.write(f"{api_key}\n{user_id}")

async def download_image(session, url, save_path, retry_limit=3): 
    retries = 0
    while retries < retry_limit:
        if stop_event.is_set():
            process_var.set("Download stopped.")
            return None
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    # Extract the content type from the response headers
                    content_type = response.headers.get('Content-Type', '')
                    
                    # Determine the correct file extension based on the content type
                    if 'image/jpeg' in content_type:
                        extension = '.jpg'
                    elif 'image/png' in content_type:
                        extension = '.png'
                    elif 'image/gif' in content_type:
                        extension = '.gif'
                    elif 'video/mp4' in content_type:
                        extension = '.mp4'
                    else:
                        extension = os.path.splitext(url)[-1]  # Use the URL's extension as a fallback

                    # Update the save path with the correct extension
                    save_path = os.path.splitext(save_path)[0] + extension

                    with open(save_path, 'wb') as f:
                        f.write(await response.read())
                    return save_path
                else:
                    process_var.set(f"Failed to download {url} with status code {response.status}")
        except (aiohttp.ClientOSError, aiohttp.ClientConnectionError) as e:
            retries += 1
            process_var.set(f"Error downloading {url}: {e}. Retrying ({retries}/{retry_limit})...")
            await asyncio.sleep(2)
        except Exception as e:
            process_var.set(f"Unexpected error: {e}")
            break
    process_var.set(f"Failed to download {url} after {retry_limit} attempts.")
    return None

async def get_gelbooru_images(tags, api_key, user_id, page=0, limit=100): 
    gelbooru = Gelbooru(api_key, user_id)
    
    try:
        results = await gelbooru.search_posts(tags=tags, page=page, limit=limit)
    except Exception as e:
        process_var.set(f"Error fetching images: {e}")
        return []

    if not results:
        process_var.set(f"No results found for tags: {', '.join(tags)}.")
        return []

    image_urls = [post.file_url for post in results]
    return image_urls

async def download_images(tags, save_dir, api_key, user_id):
    limit_per_batch = 100 
    os.makedirs(save_dir, exist_ok=True)

    batch = 0
    total_downloaded = 0
    max_images = max_images_var.get() if max_images_checkbox_var.get() else float('inf')

    async with aiohttp.ClientSession() as session:
        while not stop_event.is_set() and total_downloaded < max_images:
            process_var.set(f"Fetching images from batch {batch + 1}...")
            images = await get_gelbooru_images(tags, api_key, user_id, page=batch, limit=min(limit_per_batch, max_images - total_downloaded))

            if not images or stop_event.is_set():
                process_var.set("No more images found or download stopped.")
                break

            tasks = []
            for idx, img_url in enumerate(images):
                if stop_event.is_set() or total_downloaded >= max_images:
                    break

                # Extract the original file extension from the URL
                file_extension = os.path.splitext(img_url)[-1]
                save_path = os.path.join(save_dir, f"image_batch{batch + 1}_{idx + 1}{file_extension}")

                tasks.append(download_image(session, img_url, save_path))
                total_downloaded += 1
            
            await asyncio.gather(*tasks)

            process_var.set(f"Downloaded {total_downloaded} images from batch {batch + 1} to {save_dir}")
            batch += 1
            await asyncio.sleep(0.3 if fast_download_var.get() else 1)

    if clean_up_var.get():
        cleanup_process(save_dir)

    if open_dir_var.get():
        open_directory(save_dir)

def calculate_hash(image_path, hash_function=hashlib.md5, block_size=65536):
    hash_obj = hash_function()
    with open(image_path, 'rb') as f:
        while chunk := f.read(block_size):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def find_duplicate_images(folder_path):
    image_hashes = {}
    duplicates = []

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webm', '.mp4')):
                image_path = os.path.join(root, file_name)
                image_hash = calculate_hash(image_path)

                if image_hash in image_hashes:
                    duplicates.append((image_hashes[image_hash], image_path))
                else:
                    image_hashes[image_hash] = image_path

    return duplicates

def check_and_remove_duplicates(folder_path):
    duplicates = find_duplicate_images(folder_path)

    if duplicates:
        process_var.set("Duplicate images found and deleted:")
        for original, duplicate in duplicates:
            process_var.set(f"Original: {original}\nDeleted Duplicate: {duplicate}\n")
            os.remove(duplicate)
    else:
        process_var.set("No duplicate images found.")

def rename_files_by_modification_time(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files_with_mtime = [(f, os.path.getmtime(os.path.join(directory, f))) for f in files]
    files_with_mtime.sort(key=lambda x: x[1])

    for i, (filename, mtime) in enumerate(files_with_mtime):
        file_extension = os.path.splitext(filename)[-1]
        new_filename = f"{i+1}{file_extension}"
        os.rename(
            os.path.join(directory, filename),
            os.path.join(directory, new_filename)
        )
        process_var.set(f"Renamed '{filename}' to '{new_filename}'")

def cleanup_process(save_dir):
    process_var.set("Checking for duplicate images, this may take some time...")
    check_and_remove_duplicates(save_dir)
    rename_files_by_modification_time(save_dir)

def format_tags(raw_tags):
    formatted_tags = [tag.strip().replace(' ', '_') for tag in raw_tags.split(',')]
    return formatted_tags

def start_download():
    stop_event.clear()
    directory = custom_dir_var.get() if use_custom_dir.get() else default_directory
    raw_tags = tag_entry.get()
    api_key = api_key_var.get()
    user_id = user_id_var.get()
    
    if not raw_tags:
        messagebox.showwarning("Input Error", "Please enter tags.")
        return

    if not api_key or not user_id:
        messagebox.showwarning("Input Error", "Please enter both API key and User ID.")
        return

    # Save the API key and User ID to token.txt
    save_token(api_key, user_id)

    tags = format_tags(raw_tags)
    save_dir = os.path.join(directory, '_'.join(tags))
    os.makedirs(save_dir, exist_ok=True)

    process_var.set("Starting download...")

    download_thread = threading.Thread(target=lambda: asyncio.run(download_images(tags, save_dir, api_key, user_id)))
    download_thread.start()

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        custom_dir_var.set(directory)

def toggle_custom_dir(*args):
    if use_custom_dir.get():
        custom_dir_entry.config(state=NORMAL)
    else:
        custom_dir_entry.config(state=DISABLED)

def stop_download():
    stop_event.set()
    process_var.set("Stopping download...")

def toggle_max_images_entry(*args):
    if max_images_checkbox_var.get():
        max_images_entry.config(state=NORMAL)
    else:
        max_images_entry.config(state=DISABLED)

def open_directory(directory):
    if os.name == 'nt':  # For Windows
        os.startfile(directory)
    elif os.name == 'posix':  # For macOS or Linux
        subprocess.Popen(['open', directory])

# Initialize the main Tkinter window
root = Tk()
root.title("Gelbooru Image Downloader")
root.config(bg="#1e1e1e")

# Define Tkinter variables
tag_var = StringVar()
api_key_var = StringVar()
user_id_var = StringVar()
custom_dir_var = StringVar()
use_custom_dir = BooleanVar()
max_images_checkbox_var = BooleanVar()
max_images_var = IntVar(value=10)
clean_up_var = BooleanVar()
open_dir_var = BooleanVar()
fast_download_var = BooleanVar()
process_var = StringVar()

# Load API key and User ID if available
load_token()

# Set default directory (current directory)
default_directory = os.getcwd()

# Create UI elements
tag_label = Label(root, text="Tags (comma separated):", bg="#1e1e1e", fg="white")
tag_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

tag_entry = Entry(root, textvariable=tag_var, width=40, bg="#333333", fg="white")
tag_entry.grid(row=0, column=1, padx=10, pady=10)

api_key_label = Label(root, text="API Key:", bg="#1e1e1e", fg="white")
api_key_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

api_key_entry = Entry(root, textvariable=api_key_var, width=40, bg="#333333", fg="white")
api_key_entry.grid(row=1, column=1, padx=10, pady=10)

user_id_label = Label(root, text="User ID:", bg="#1e1e1e", fg="white")
user_id_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

user_id_entry = Entry(root, textvariable=user_id_var, width=40, bg="#333333", fg="white")
user_id_entry.grid(row=2, column=1, padx=10, pady=10)

custom_dir_check = ttk.Checkbutton(root, text="Use Custom Directory", variable=use_custom_dir)
custom_dir_check.grid(row=3, column=0, padx=10, pady=10, sticky="e")

custom_dir_entry = Entry(root, textvariable=custom_dir_var, width=40, state=DISABLED, bg="#333333", fg="white")
custom_dir_entry.grid(row=3, column=1, padx=10, pady=10)

browse_button = Button(root, text="Browse", command=select_directory, bg="#333333", fg="white")
browse_button.grid(row=3, column=2, padx=10, pady=10)

max_images_check = ttk.Checkbutton(root, text="Limit Max Images", variable=max_images_checkbox_var)
max_images_check.grid(row=4, column=0, padx=10, pady=10, sticky="e")

max_images_entry = Entry(root, textvariable=max_images_var, width=10, state=DISABLED, bg="#333333", fg="white")
max_images_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

clean_up_check = ttk.Checkbutton(root, text="Clean Up (Remove Duplicates & Rename Files)", variable=clean_up_var)
clean_up_check.grid(row=5, column=0, padx=10, pady=10, columnspan=2)

open_dir_check = ttk.Checkbutton(root, text="Open Directory After Download", variable=open_dir_var)
open_dir_check.grid(row=6, column=0, padx=10, pady=10, columnspan=2)

fast_download_check = ttk.Checkbutton(root, text="Fast Download (Less Delay but more likely to crash)", variable=fast_download_var)
fast_download_check.grid(row=7, column=0, padx=10, pady=10, columnspan=2)

start_button = Button(root, text="Start Download", command=start_download, bg="#333333", fg="white")
start_button.grid(row=8, column=0, padx=10, pady=10, columnspan=2)

stop_button = Button(root, text="Stop Download", command=stop_download, bg="#333333", fg="white")
stop_button.grid(row=8, column=1, padx=10, pady=10, columnspan=2)

process_label = Label(root, textvariable=process_var, bg="#1e1e1e", fg="white")
process_label.grid(row=9, column=0, padx=10, pady=10, columnspan=3)

# Link variables to corresponding functions
use_custom_dir.trace_add("write", toggle_custom_dir)
max_images_checkbox_var.trace_add("write", toggle_max_images_entry)

# Run the application
root.mainloop()
