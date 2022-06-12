from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception ("Unable to fetch page " + url)
    doc = BeautifulSoup(response.text,'html.parser')
    return doc


# Defining functions to parse fields from the doc

def get_restaurant_names(doc):
    selector = 'grey res_name font-20 bold inline-block'
    name_tags = doc.find_all('h3',class_=selector)
    return [tag.text.strip() for tag in name_tags]

def get_restaurant_locations(doc):
    selector = 'margin-t-5 res_loc'
    location_tags = doc.find_all('h3',class_=selector)
    return [tag.text.strip() for tag in location_tags]

def get_costs_for_2(doc):
    selector = 'padding-l-10 grey cost_for_two'
    cost_tags = doc.find_all('span',class_=selector)
    for cost_tag in cost_tags:
        if cost_tag:
            cost = cost_tag.string
        else:
            cost = "Price Not Available"
        
    return [tag.text.strip()[:-7] for tag in cost_tags]

def get_restaurant_cusisines(doc):
    selector = 'grey padding-l-10 res_cuisine'
    cusisine_tags = doc.find_all('div',class_=selector)
    return [tag.text.strip() for tag in cusisine_tags]

def get_restaurant_ratings(doc):
    selector = 'critic'
    rating_tags = doc.find_all('span',class_=selector)
    return [tag.text.strip() for tag in rating_tags]

def get_restaurant_restaurant_images(doc):
    selector = 'radius-4 res_name lazy'
    img_tags = doc.find_all('img',class_=selector)
    return [tag['src'] for tag in img_tags]

def get_restaurant_restaurant_pages(doc):
    base_url = "https://www.eazydiner.com/"
    selector = 'btn btn-primary height-40 block bold padding-10 font-14 apxor_click'
    page_tags = doc.find_all('a',class_=selector)
    return [base_url + tag['href'] for tag in page_tags]

# Defining function that will process the request from start to end

def get_restaurants():

    i = 1
    all_restaurant_names = []
    all_restaurant_locations = []
    all_costs_for_2 = []
    all_cusisines = []
    all_ratings = []
    all_restaurant_images = []
    all_restaurant_pages = []
    
    base_url = 'https://www.eazydiner.com/restaurants?location=delhi-ncr&pax=2&total=281&page='
    
    page_count = input("Enter then number of pages you want to scrape: ")
    page_count = int(page_count)

    # Initilising the loop

    while True:
        
        if i > page_count:
            break
    
        page_url = base_url + str(i)
        
        # Fetching the page from the url
        doc = get_page(page_url)

        # Parsing data from the page            
        restaurant_names = get_restaurant_names(doc)

        # Adding condition to break the loop if page has no restaurants
        if len(restaurant_names) < 1:
            print("Stoping at page {}, No more data to scrape".format(i-1))
            break

        restaurant_locations = get_restaurant_locations(doc)
            
        costs_for_2 = get_costs_for_2(doc)
            
        cusisines = get_restaurant_cusisines(doc)
            
        ratings = get_restaurant_ratings(doc)
            
        restaurant_images = get_restaurant_restaurant_images(doc)
            
        restaurant_pages = get_restaurant_restaurant_pages(doc)

        all_restaurant_names = all_restaurant_names + restaurant_names
        all_restaurant_locations = all_restaurant_locations + restaurant_locations
        all_costs_for_2 = all_costs_for_2 + costs_for_2
        all_cusisines = all_cusisines + cusisines
        all_ratings = all_ratings + ratings
        all_restaurant_images = all_restaurant_images + restaurant_images
        all_restaurant_pages = all_restaurant_pages + restaurant_pages
            
        restaurant_data = {
            'restaurant_name':all_restaurant_names,
            'restaurant_location':all_restaurant_locations,
            'cost_for_2':all_costs_for_2,
            'cusisine':all_cusisines,
            'rating':all_ratings,
            'restaurant_img': all_restaurant_images,
            'restaurant_page':all_restaurant_pages
            }

        i = i + 1
    return restaurant_data,print("Task Completed")

def get_restaurant_csv():
    output = get_restaurants()
    df = pd.DataFrame(output[0])
    comment = output[1]
    return df.to_csv('restaurants.csv', index=None),comment

if __name__ == '__main__':
    get_restaurant_csv()