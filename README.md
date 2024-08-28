# Gelbooru Image Downloader

A Python client that uses the Gelbooru API to download images with specified tags.

![screencap](https://github.com/user-attachments/assets/69a499f8-79a4-469e-948d-b640e80da0ff)

## How to install it

You must verify your api key and user id from gelbooru [here](https://github.com/neoluigi4123/Gelbooru-Image-Downloader/edit/main/README.md#how-to-setup-your-gelbooru-api-key-and-user-id).

and once its done, just download the zip file, run the install.bat then you're good to go

## How It Works

### Tags
Enter your tags in the first text box. Tags should not contain any underscores (_) and must be comma-separated. The tags must also exist on Gelbooru; any typo or non-existent tag won't work.

### API Key / User ID
To use the software, you must have an account on Gelbooru and then get your API key and user ID. The script saves your API key and user ID the first time you use it, so don't worry about losing them—the app takes care of everything.

To get them, check [How to set up your Gelbooru API key and user ID](https://github.com/neoluigi4123/Gelbooru-Image-Downloader/edit/main/README.md#how-to-setup-your-gelbooru-api-key-and-user-id).

### Custom Directory
You can use any directory you want by checking the "Use Custom Directory" button, then either paste any directory or browse for one with the "Browse" button. The app will automatically use `C:/Users/pc/Pictures/tag` if you don't specify a custom one.

### Download a Specific Number of Images
If unchecked, you'll download every image that can be found with the tags you entered. To download a specific number of images, you can check "Limit Max Images" and then input the desired number.

### Clean Up
The cleanup function can take a significant amount of time based on how many images you want to download. It will check each image's content, and if it detects duplicates, it will delete them. (Note: it only detects exact duplicates. If an image is the same as another but with a text bubble or minor differences, it will count as a different one.)

### Open Directory After Download
Check this option if you want to automatically open the folder with the downloaded images at the end of the download.

### Fast Download
Because Gelbooru cannot send 100 images at the speed of light, there is some delay to ensure that the data is correctly downloaded and the server doesn't block the process. You can use "Fast Download" to download a smaller amount of images faster (500-1000), but this will be less accurate and is more likely to crash.

## How to Set Up Your Gelbooru API Key and User ID

### Create the Gelbooru Account
If you don't already have an account, go to [this link](https://gelbooru.com/index.php?page=account&s=reg) to create one (don't forget to read their TOS that no one reads anyway: [TOS](https://gelbooru.com/tos.php)).

### Get Your API Key / User ID
Once your account is created, go to [this URL](https://gelbooru.com/index.php?page=account&s=options) to see your settings, which contain your API key and user ID. Scroll all the way down, and you'll see them.

![image](https://github.com/user-attachments/assets/90a09294-fded-4016-9a03-daffc88c1f25)

Just grab them and paste them into the app, and you're good to go!

![image](https://github.com/user-attachments/assets/26d6d5b7-7578-4224-9c37-5977b3251922)

The script saves your API key and user ID the first time you use it, so don't worry about losing them—the app takes care of everything.
