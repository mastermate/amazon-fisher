'''
Created on 23 Jan 2018

@author: bestg
'''
import unittest
import scraper


class CategoryScraperTest(unittest.TestCase):


    def test_build_category_url(self):
        url = scraper.build_category_url('ref=dp_bc_1', ['node=68'])
        print(url)

    def test_scrape_products_from_category(self):
        urls = scraper.scrape_products_from_category('ref=dp_bc_1', ['node=68'])
        print(urls)
        
    def test_reviews_from_category(self):
        reviews = scraper.reviews_from_category('ref=dp_bc_1', ['node=68'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()