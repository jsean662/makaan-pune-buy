import scrapy
#from scrapy import log
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.selector import Selector
from makaan.items import MakaanItem
from scrapy.loader import ItemLoader
import unicodedata
import json
import datetime
from datetime import datetime as dt
import re

class PuneSpider(scrapy.Spider):
    name = "puneBuy"
    allowed_domains = ["https://www.makaan.com/"]

    start_urls = ['https://www.makaan.com/listings?sortBy=date-desc&listingType=buy&pageType=CITY_URLS&cityName=Pune&cityId=21&templateId=MAKAAN_CITY_LISTING_BUY&page=%s' % page for page in xrange(1,891)]
  
    def parse(self, response):
        item = MakaanItem()
        hxs = Selector(response)
        a = hxs.xpath("//div[@class='cardholder']")
        
        for i in a:
            qua4 = 5
            detail = i.xpath('div[@class="cardWrapper"]/script/text()').extract_first()
            data = json.loads(detail)

#Initialization to defult value

            item['carpet_area'] = '0'
            item['updated_date'] = '0'
            item['management_by_landlord'] = 'None' 
            item['areacode'] = '0'
            item['mobile_lister'] = '0'
            item['google_place_id'] = 'None'
            item['age'] = '0'
            item['address'] = 'None' 
            item['price_on_req'] = 'FALSE' 
            item['sublocality'] = 'None' 
            item['config_type'] = 'None' 
            item['platform'] = 'None'  
            item['city'] = 'None'  
            item['listing_date'] = '0'  
            item['txn_type'] = 'None'  
            item['property_type'] = 'None'  
            item['Building_name'] = 'None'  
            item['lat'] = '0'  
            item['longt'] = '0'  
            item['locality'] = 'None'  
            item['Status'] = 'None'  
            item['listing_by'] = 'None'
            item['name_lister'] = 'None'  
            item['Selling_price'] = '0'  
            item['Monthly_Rent'] = '0'  
            item['details'] = 'None'  
            item['data_id'] = 'None'  
            item['Possession'] = '0'  
            item['Launch_date'] = '0'
            item['price_per_sqft'] = '0'  
            item['Bua_sqft'] = '0'  
            item['quality1'] = '0'
            item['quality2'] = '0'
            item['quality3'] = '0'
            item['quality4'] = '0'
                     
#Scrapimg of data

            item['property_type'] = data['propertyType']
            if item['property_type'] == '':
                qua1 -= 1
            
            item['platform'] = 'makaan'
            
            item['data_id'] = data['id']
            
            item['name_lister'] = data['sellerName']
            if item['name_lister'] == '':
                item['name_lister'] = 'None'
                qua3 -= 1

            item['lat'] = data['latitude']
            if item['lat'] == '':
                item['lat'] = '0'
                qua4 -= 1

            item['longt'] = data['longitude']
            if item['longt'] == '':
                item['longt'] = '0'
                qua4 -= 1

            item['locality'] = data['localityName']

            item['city'] = data['cityName']

            item['Building_name'] = data['fullName']
            if item['Building_name'] == '':
                item['Building_name'] = 'None'
                qua4 -= 1

            item['config_type'] = data['bedrooms']+'BHK'

            item['txn_type'] = data['listingCategory']
            
            if 'Primary' in item['txn_type']:
                item['txn_type'] = 'Sale'

            if item['txn_type'] == 'Sale' or item['txn_type'] == 'Resale':
                item['Selling_price'] = data['price']
                item['Monthly_Rent'] = '0'

            if 'Rental' in item['txn_type']:
                item['Monthly_Rent'] = data['price']
                item['Selling_price'] = '0'

            if item['Selling_price'] == '0' and item['Monthly_Rent'] == '0':
                item['price_on_req'] = 'TRUE'
                qua4 -= 1
            else:
                item['price_on_req'] = 'FALSE'

            item['Status'] = data['projectStatus']
            if item['Status'] == '':
                item['Status'] = 'None'
           
            if (not data['verificationDate'] == ''):
                dat = int(data['verificationDate'])/1000
                item['listing_date'] = datetime.datetime.utcfromtimestamp(dat).strftime('%m/%d/%Y %H:%M:%S')
                item['updated_date'] = item['listing_date']
            else:
                item['listing_date'] = dt.now().strftime('%m/%d/%Y %H:%M:%S')
                item['updated_date'] = item['listing_date']

            if 'ale' in item['txn_type']:
                prc_pr_sf = i.xpath('div[@class="cardWrapper"]/div[@class="cardLayout clearfix"]/div[@class="infoWrap"]/div[@class="headInfo"]/div[@class="priceWrap"]/div[@class="price-rate-col"]/div[@class="rate"]/span[@class="val"]/text()').extract_first()
                item['price_per_sqft'] = re.findall('[0-9]+',prc_pr_sf)
                item['price_per_sqft'] = ''.join(item['price_per_sqft'])
            else:
                item['price_per_sqft'] = '0'

            sqf = i.xpath('.//span[@class="size"]/text()').extract_first()
            try:
                item['Bua_sqft'] = re.findall('[0-9]+',sqf)
                item['Bua_sqft'] = ''.join(item['Bua_sqft'])
            except:
                item['Bua_sqft'] = '0'
                qua4 -= 1

            if 'onstruction' in item['Status']:
                try:
                    date = i.xpath('div[@class="cardWrapper"]/div[@class="cardLayout clearfix"]/div[@class="infoWrap"]/div[@class="highlight-points"]/div[@class="dcol poss"]/div[1]/text()').extract_first()
                    item['Possession'] = dt.strftime(dt.strptime(date,'%b %Y'),'%m/%d/%Y %H:%M:%S')
                    item['age'] = '0'
                except:
                    print date
            elif 'ale' in item['txn_type']:
                item['age'] = i.xpath('div[@class="cardWrapper"]/div[@class="cardLayout clearfix"]/div[@class="infoWrap"]/div[@class="highlight-points"]/div[@class="dcol poss"]/div[@class="val ''"]/text()').extract_first()

            if ((not item['age'] == '') or (not item['age'] == 'None')):
                item['age'] = '0'   
                
            
#Quality calculations
            if (((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['price_per_sqft'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None') and (not item['lat']=='0'))):
                item['quality4'] = 1
            elif (((not item['price_per_sqft'] == '0') and (not item['Building_name']=='None') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['lat']=='0')) or ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['lat']=='0')) or ((not item['Selling_price'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None')) or ((not item['Monthly_Rent'] == '0') and (not item['Bua_sqft']=='0') and (not item['Building_name']=='None'))):
                item['quality4'] = 0.5
            else:
                item['quality4'] = 0

            if ((not item['mobile_lister'] == 'None') or (not item['listing_by'] == 'None') or (not item['name_lister'] == 'None')):
                item['quality3'] = 1
            else:
                item['quality3'] = 0              

            if ((not item['Launch_date'] == '0') or (not item['Possession'] == '0')):
                item['quality2'] = 1
            else:
                item['quality2'] = 0

            if ((not item['Building_name'] == 'None') and (not item['listing_date'] == '0') and (not item['txn_type'] == 'None') and (not item['property_type'] == 'None') and ((not item['Selling_price'] == '0') or (not item['Monthly_Rent'] == '0'))):
                item['quality1'] = 1
            else:
                item['quality1'] = 0

            yield item
