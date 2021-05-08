import scrapy
import json

class Spider(scrapy.Spider):
    name='medium_scrapper'
    handle_httpstatus_list = [401,400]
    
    autothrottle_enabled=True
    def start_requests(self):
        
        start_urls = ['https://www.medium.com/search/posts?q=Data%20Science']
        
        for url in start_urls:
            yield scrapy.Request(url,method='GET',callback=self.parse)
    
    def parse(self,response):
              
        response_data=response.text
        response_split=response_data.split("ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken")
       
        response_data=response_split[1]
        filename="medium.txt"

        # writeTofile(filename,response_data)
        
        file = open(filename, "a")
        file.write(response_data)

        # with open(filename,'w') as infile:
        #     data=json.load(infile)
        # #Check if there is a next tag in json data
        # if 'paging' in data['payload']:
        #     data=data['payload']['paging']
        #     if 'next' in data:
        #         #Make a post request
        #         print("In Paging, Next Loop")
        #         data=data['next']
        #         formdata={
        #                 'ignoredIds':data['ignoredIds'],
        #                 'page':data['page'],
        #                 'pageSize':data['pageSize']
        #                 }               

        #         yield scrapy.Request('https://www.medium.com/search/posts?q=Data%20Science',method='POST',body=json.dumps(formdata),headers=header,cookies=cookie,callback=self.parse)