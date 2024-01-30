import vnw_crawler
import vl24_crawler

body = {
    "userId": 0,
    "query": "",
    "filter": [],
    "ranges": [],
    "order": [],
    "hitsPerPage": 50,
    "page": 0,
}


api = 'https://ms.vietnamworks.com/job-search/v1.0/search'
#vnw_crawler.crawl(api,body,0,50) 

print("Crawl vl24 ...")
vl24_crawler.crawl(0,10)

