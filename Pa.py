from requests_html import HTMLSession
from pandas import DataFrame
import time
WAIT_TIME_IN_SECONDS = 1.5

session = HTMLSession()
dict_info = {
    'ProductName':'body > div.auto-size > div.page.grid > div.layout-fly.cf > div.main-wrap > div > div.search-list > div > div > div.product-wrap > div > h2 > a',
    'ProductProperty':'body > div.auto-size > div.page.grid > div.layout-fly.cf > div.main-wrap > div > div.search-list > div > div > div.product-wrap > div > div.product-property',
    'Description':'body > div.auto-size > div.page.grid > div.layout-fly.cf > div.main-wrap > div > div.search-list > div > div > div.product-wrap > div > div.extra-property',
    'Company':'body > div.auto-size > div.page.grid > div.layout-fly.cf > div.main-wrap > div > div.search-list > div > div > div.pro-extra > ul > li.compnay-name-li',
    'Location':'body > div.auto-size > div.page.grid > div.layout-fly.cf > div.main-wrap > div > div.search-list > div > div > div.pro-extra > ul > li:nth-child(3) > span',
    }

def auto_get_category(url = 'https://www.made-in-china.com/prod/catlist/'):
    """
    Auto Catch top category list, and urls.
    Default url link is https://www.made-in-china.com/prod/catlist/
    """
    r = session.get(url)
    cate_list = []
    for i in ['1','2','3','4','5','6']:
        sel = '#nav-' + i + ' > div.primary-classify-content > div > div > ul > li > a'
        results = r.html.find(sel)
        for j, k in enumerate(results):
            try:
                otpt = list(k.absolute_links)[0]
                cate_list.append(otpt)
            except:
                continue
    return cate_list

def info_extract(cate, r):
    """
    Output is like [(
        'Service-Catalog/Advertising',
        'Custom Printed Outdoor Advertising Folding Exhibition Tent',
        'Min. Order: 1 Set',
        'Zhejiang Dekay Tents Corporation',
        'https://dekaytents.en.made-in-china.com',
        'Zhejiang, China'),....]
    """
    otpt = []
    nums = r.html.find(dict_info['ProductName'])
    cate = cate[:-5][30:]
    for i, j in enumerate(nums):
        ProductName = r.html.find(dict_info['ProductName'])[i].text
        ProductProperty = r.html.find(dict_info['ProductProperty'])[i].text
        Company = r.html.find(dict_info['Company'])[i].text
        Link = list(r.html.find(dict_info['Company'])[i].absolute_links)[0]
        Location = r.html.find(dict_info['Location'])[i].text
        otpt.append((cate, ProductName, ProductProperty, Company, Link, Location))
    return otpt

def iter_extract(cate_list = ['https://www.made-in-china.com/Service-Catalog/Advertising.html']):
    """
    Extract information from https://www.made-in-china.com
    Input should be output from cate_list
    """
    results = []
    for cate in cate_list:
        r = session.get(cate)
        otpt = info_extract(cate=cate, r=r)
        results += otpt
        time.sleep(WAIT_TIME_IN_SECONDS)
        print('Web Extracting Data from '+ cate)       
    return results
        


if __name__ == '__main__':
    print('Made-in-China Scraper V1.0 -- Sariel Huang')
    cate_list = auto_get_category('https://www.made-in-china.com/prod/catlist/')
    results = iter_extract(cate_list=cate_list)
    DATA = DataFrame(results)
    DATA.columns = ['Category', 'ProductName', 'ProductProperty','Company','Link','Location']
    DATA.to_csv('made_in_china.csv', encoding='UTF-8', index=False)