(current version is 2.0)

## Please use the Danbooru.py as the gelbooru api doesn't seem to work correctly anymore. The latest install.bat already use it.

# Danbooru Image Downloader

A Python client that uses the Danbooru API to download images with specified tags. Can download image, video, gifs....

![image](https://github.com/user-attachments/assets/96c83b14-7a55-4e6f-9e22-5b2d9daed99c)


## How to install it

You just have to follow the instruction in the [last release](https://github.com/neoluigi4123/Gelbooru-Image-Downloader/releases/latest) then you're good to go!

However, if you want to use an older version of the software, you can go over the release tab on the right, then chose your version.. Good luck! I must say that newer version fixes issue while other may not work fine.

![image](https://github.com/user-attachments/assets/da2f524c-178d-46f3-b609-e8a65f8e25fa)


## How It Works

### Tags
Enter your tags in the first text box. Tags should not contain any underscores (_) and must be comma-separated. The tags must also exist on Gelbooru; any typo or non-existent tag won't work.

### Custom Directory
You can use any directory you want by checking the "Use Custom Directory" button, then either paste any directory or browse for one with the "Browse" button. The app will automatically use `C:/Users/pc/Pictures/tag` if you don't specify a custom one.

### Download a Specific Number of Images
If unchecked, you'll download every image that can be found with the tags you entered. To download a specific number of images, you can check "Limit Max Images" and then input the desired number.

### Open Directory After Download
Check this option if you want to automatically open the folder with the downloaded images at the end of the download.

### Fast Download
Because Gelbooru cannot send 100 images at the speed of light, there is some delay to ensure that the data is correctly downloaded and the server doesn't block the process. You can use "Fast Download" to download a smaller amount of images faster (500-1000), but this will be less accurate and is more likely to crash.

## To Do List
- Fix the tag function to download with multiple tag (50% done)
- Fix quick download
- Add the 'clean' function back to remove any duplicated images

- multiple tag downloader (download images from tag 1, while downloading images from tag 2 in another thread, etc)
