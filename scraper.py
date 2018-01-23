import requests
from lxml import html  
import json

AMAZON_PRODUCT_BASE_URL = 'https://www.amazon.co.uk/dp/'
AMAZON_REVIEW_BASE_URL = 'https://www.amazon.co.uk/product-reviews/'
AMAZON_CAT_BASE_URL = 'https://www.amazon.co.uk/b/'
XPATH_ITEM_SEARCH_RESULTS = '//div[@id="search-results"]//li'
AMAZON_ASIN_SEARCH_ITEM = 'data-asin'
AMAZON_SINGLE_REVIEW_ATT = ('data-hook','review')
AMAZON_REVIEW_TITLE_ATT = ('data-hook','review-title')
AMAZON_REVIEW_BODY_ATT = ('data-hook','review-body')
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

def main():
    url = scrape_products_from_category('ref=dp_bc_1', ['node=68'])
    print(url)

def reviews_from_category(ref, categ_params):
    review_urls = scrape_products_from_category(ref, categ_params)
    for review_url in review_urls:
        reviews = scrape_reviews_from_product(review_url)
        print(reviews)

def scrape_reviews_from_product(review_url):
    ## ASIN is a 10 character code the identifies a product in Amazon
    r = requests.get(review_url, headers=HEADERS)
    content = r.text
    parsed_content = html.fromstring(content)
    xpath_expr = '//div[@{}="{}"]'.format(AMAZON_SINGLE_REVIEW_ATT[0], AMAZON_SINGLE_REVIEW_ATT[1])
    reviews = parsed_content.xpath(xpath_expr)
    review_list = []
    for review in reviews:
        title_xpath = '//span[@{}="{}"]'.format(AMAZON_REVIEW_TITLE_ATT[0], AMAZON_REVIEW_TITLE_ATT[1])
        body_xpath = '//span[@{}="{}"]'.format(AMAZON_REVIEW_BODY_ATT[0], AMAZON_REVIEW_BODY_ATT[1])
        review_title = review.xpath(title_xpath)
        title_text = review_title[0].text
        review_body = review.xpath(body_xpath)
        body_text = review_body[0].text
        entry = {'title': title_text, 'body': body_text}
        review_list.append(entry)
    return review_list

def scrape_products_from_category(ref, categ_params): 
    ## so far, ref is always present. then we need additional params
    # <div id="search-results">
    search_url = build_category_url(ref, categ_params)
    result_list = retrieve_asin_list_from_search(search_url)
    item_urls = []
    for asin in result_list:
        item_url = '{}{}'.format(AMAZON_REVIEW_BASE_URL, asin)
        item_urls.append(item_url)
    return item_urls
    
def retrieve_asin_list_from_search(search_url):
    r = requests.get(search_url, headers=HEADERS)
    content = r.text
    parsed_content = html.fromstring(content)
    ## we have the parsed html of the category
    ## we get now the search results and their asin
    search_results = parsed_content.xpath(XPATH_ITEM_SEARCH_RESULTS)
    result_list = []
    for item in search_results:
        asin = item.get(AMAZON_ASIN_SEARCH_ITEM)
        result_list.append(asin)
    return result_list

def build_category_url(ref, categ_params):
    search_url = '{}{}?'.format(AMAZON_CAT_BASE_URL,ref)
    for param in categ_params:
        search_url += param + '&'
    if (len(categ_params) > 0):
        ## remove the last '&'
        search_url = search_url[0:-1]    
    return search_url
    
    
if __name__ == "__main__":
    main()
    
