import vnw_crawler
import vl24_crawler
import topcv_crawler
import time 

body = {
    "userId": 0,
    "query": "",
    "filter": [],
    "ranges": [],
    "order": [],
    "hitsPerPage": 50,
    "page": 0,
}

start = time.time()
api = 'https://ms.vietnamworks.com/job-search/v1.0/search'
print("Crawl vnw ...")
vnw_crawler.crawl(api,body,0,50) 
end = time.time()
print("==================================================================")
print("Processing time: ",end-start)
print("==================================================================")

start = time.time()
print("Crawl topcv ...")
topcv_crawler.crawl(0,5)
end = time.time()
print("==================================================================")
print("Processing time: ",end-start)
print("==================================================================")

start = time.time()
print("Crawl vl24 ...")
vl24_crawler.crawl(0,5)
end = time.time()
print("==================================================================")
print("Processing time: ",end-start)
print("==================================================================")


