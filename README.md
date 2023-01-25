# Web-scraping-Google_Image_scraping
This is an automation project which helps us to scrape or download large quantites of Googles images on particular search, avoiding the manual work.

## Working:
There are three important functions which performs three distinct operation:
* fetch_image_url()
* save_image()
* search_and_download()

### fetch_image_url():
This function initiate the automation process. The following are the steps involved:
* takes in user's search item. 
* Using webdriver from selenium opens up chrome, loads the webpage for image search results
* Clicks on the images
* Grabs the actual image URL and returns the list of image URLs

### save_image():
This function downloads the image from the image URL and saves it in local machine

### search_and_download():
This is a link function, which links both functions fetch_image_url() and save_image(). It takes in three arguments,
* search_string - search for image which is to be scraped
* number_of_images - total number of images to be downloaded
* driver_path - Path where chrome driver is present

Now, these three arguments are applied to other two functions. search_and_download() function wraps-up the final folder with folder name same as search_string with images being scraped.
