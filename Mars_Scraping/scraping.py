# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# 10.5.3
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Set news title and paragraph varaibles
    news_title, news_paragraph = mars_news(browser)

    # Create a data dictionary
    # Run all scraping functions and store results in dictonary
    data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "last_modified": dt.datetime.now(),
            "hemisphere_images": hemisphere_images(browser)
    }

    # Stop webdriver
    browser.quit()
    return data

# 10.5.2
def mars_news(browser):

   # Visit the mars nasa news site
   url = 'https://redplanetscience.com/'
   browser.visit(url)

   # Optional delay for loading the page
   browser.is_element_present_by_css('div.list_text', wait_time=1)

   # Convert the browser html to a soup object and then quit the browser
   html = browser.html
   news_soup = soup(html, 'html.parser')

# 10.5.2
def mars_news(browser):

    # Visit the mars nasa news site
    url= 'https://redplanetscience.com/'
    browser.visit(url)

    #optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #add a try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent elemtn to find the first 'a' tag and save it as a 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Add a try/except for error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return(img_url)


# ## Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstraps
    return df.to_html()

# ## Hemisphere
def hemisphere_images():

    # Visit URL
    url = 'https://marshemispheres.com'
    browser.visit(url)
    
    hemisphere_image_urls = []

    for hemispheres in range(4):
        # Click through each link
        browser.links.find_by_partial_text('Hemisphere')[hemispheres].click()
    
        # Parse
        html = browser.html
        hemisphere_soup = soup(html, 'html.parser')
    
        # Scrape
        title = hemisphere_soup.find('h2', class_='title').text
        img_url = hemisphere_soup.find('li').a.get('href')
    
        # Dictionary
        hemisphere_content = {}
        hemisphere_content['title']=title
        hemisphere_content['img_url']= f'https://marshemispheres.com/{img_url}'
    
        # Append into list
        hemisphere_image_urls.append(hemisphere_content)
        browser.back()

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())