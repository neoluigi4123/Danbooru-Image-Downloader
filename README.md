# Gelbooru-Image-Downloader
A client made in python that use the gelbooru apy to download image with specified tag

![screencap](https://github.com/user-attachments/assets/69a499f8-79a4-469e-948d-b640e80da0ff)

# How it work

 - ## - Tags -
You write your tags in the first text box, tags should not contain any '_', and must be comma separated ', '. The tags ALSO must be on gelbooru too, a typo and/or the tags doesn't exist won't work.

 - ## - API Key / User ID -
To use the software, you must have an account on gelbooru and then get your key, see the next section about getting the API Key / User ID.

 - ## - Custom Directory -
You can use any directory you want by checking the "use Custom Directory" button, then you can paste any directory or browse them with the "Browse" button.

 - ## - Download an precise amount of image -
If unchecked, you'll download every image that can be found with the tag you put, otherwise, To Download the right amount of image needed, you can check "Limit Max Images" then input any number.

 - ## - Clean Up -
The clean up function can take an high amount of time based on how many image you want to download. It will check for every image their content, and if it detect multiple one's it will delete them (multiple "exact" image, if an image is the same as an other one, but with text bubble or something it will cound as an another one).

 - ## - Open Directory After Download -
You just need to check it if you want to automaticly open the folder with the downloaded images at the end of the download.

 - ## - Fast Download -
Because gelbooru cannot send 100 images at speed of light, there is some delay to ensure that the data is correctly downloaded and the server doesn't block the process. You can use "Fast Download" to download an smaller amount of image faster (500-1000) but will be less accurate and is more likely to crash.


