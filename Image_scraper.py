from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os


#This function reaches out the google images page, selects individual thumbnails, gets the image urls.
def fetch_image_url(search_string:str, wd:webdriver, max_images:int, delay:int = 2):
    
    """fetch_imaage_url function takes in 4 arguments - search_string, wd, max_images, delay(default = 1), gives
    back array of image_urls"""
    
    try:
        #This function helps us to scroll down the webpage (using java script)
        def scroll_down(wd):
            try:
                wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(delay)
            except Exception as e:
                return f"We have encountered an error in scroll_down method - {e}"   
        
        #We are providing the initialization link for image search
        url = "https://www.google.com/search?q={q}&hl=EN&tbm=isch&sxsrf=AJOqlzUBdXVGTsXec_zUwh4v9XfwZIX3kw%3A1674384479113&source=hp&biw=1536&bih=760&ei=XxTNY57GAceA2roPtq6j0AY&iflsig=AK50M_UAAAAAY80ib9GjOu2ESDfw8QjQScavTpzaX4Dt&ved=0ahUKEwje8duggNv8AhVHgFYBHTbXCGoQ4dUDCAc&uact=5&oq=voilet&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BwgjEOoCECc6BAgjECc6CwgAEIAEELEDEIMBOggIABCxAxCDAVDoDViaFWC3GWgBcAB4AIABUogBuQOSAQE2mAEAoAEBqgELZ3dzLXdpei1pbWewAQo&sclient=img"
        wd.get(url.format(q=search_string))

        #image urls are defined as set so as to eliminate identical image urls
        image_urls = set()
        image_count = 0
        search_start = 0
        while image_count <= max_images:
            scroll_down(wd)

            #selecting thumbnails
            thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")
            no_of_thumbnails = len(thumbnails)

            print(f'Found : {no_of_thumbnails} results, extracting image links')

            #selecting image urls from thumbnails    
            for img in thumbnails[search_start:no_of_thumbnails]:
                try:
                    img.click()
                    time.sleep(delay)
                except Exception:
                    continue

                #filtering other elements apart from image links    
                actual_images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
                for images in actual_images:
                    if images.get_attribute('src') and 'http' in images.get_attribute('src'):
                        image_urls.add(images.get_attribute('src'))
                    
                image_count = len(image_urls)

                if len(image_urls) > max_images:
                    print(f'Found {len(image_urls)} results, waiting to get downloaded...')
                    break
        
        return image_urls
    
    except Exception as e:
        return f'We have encountered an issue in fetch_image_url method- {e} '


#This function downloads individual images saves in local system
def save_image(path:str, url:str, count:int):
    """save_image function takes in path, url, count and helps in saving images after downloading"""
    try:
        image_content = requests.get(url).content
    except Exception as e:
        print(f'ERROR - couldnt download image from url {url}')
    
    try:
        f = open(os.path.join(path, "IMG-"+str(count)+".jpg"), "wb")
        f.write(image_content)
        f.close()
        print(f'SUCCESS - We have saved the image from url - {url} at {f}')
    except Exception as e:
        print(f'ERROR - We have encountered error while saving image from url - {url}')


#This function calls both fetch_image_url function and save_image function helps creating folder and final scraping
def search_and_download(search_string:str, number_of_images:int, driver_path:str, target_path:str = "./images"):
    
    """search_and_download function takes in search_string, number_of_images, driver_path and target_path(default)
    and performs the final taks of scrapping all images into a folder named per search_string"""
    try:
        target_folder = os.path.join(target_path, '_'.join(search_string.lower().split(' ')))

        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        
        with webdriver.Chrome(executable_path=driver_path) as wd:
            links = fetch_image_url(search_string=search_string,wd=wd, max_images=(number_of_images-1))
        
        count = 0
        for link in links:
            save_image(target_folder, link, count)
            count += 1
    
    except Exception as e:
        return f"We have encountered an error at search_and_download function - {e}"


###EXECUTION###
#provide the path where chromedriver is located
DRIVER_PATH = "C:\\Users\\ptbka\\Web scraping- Google Image scraping\\chromedriver.exe"
#provide the string to be searched
search = "POKEMON"
search_and_download(search_string=search, number_of_images=50, driver_path=DRIVER_PATH)
