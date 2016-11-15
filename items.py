# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class MakaanItem(scrapy.Item):
    carpet_area = Field()
    updated_date = Field() 
    management_by_landlord = Field()
    areacode = Field()
    mobile_lister = Field()
    google_place_id = Field()
    #immediate_possession = Field()
    age = Field()
    address = Field()
    price_on_req = Field()
    sublocality = Field()
    config_type = Field()
    platform = Field()
    city = Field()
    listing_date = Field()
    txn_type = Field()
    property_type = Field()
    building_name = Field()
    lat = Field()
    longt = Field()
    locality = Field()
    #sqft = Field()
    status = Field()
    listing_by = Field() 
    name_lister = Field()
    selling_price = Field()
    monthly_rent = Field()
    details = Field()
    data_id = Field()
    possession = Field()
    launch_date = Field()
    price_per_sqft = Field()
    bua_sqft = Field()
    quality1 = Field()
    quality2 = Field()
    quality3 = Field()
    quality4 = Field()
    