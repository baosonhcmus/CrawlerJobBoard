import insert
from bs4 import BeautifulSoup

from datetime import datetime
import requests
import pandas as pd
import time
import re

def crawl(start,max_iteration):
  page = start
  print("Crawling ...")
  while True:
      print("\t Page {:}".format(page))
      if (page < max_iteration) :
          url = "https://vieclam24h.vn/tim-kiem-viec-lam-nhanh?page=" + str(page)
          headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

          r = requests.get(url,headers=headers)
          soup = BeautifulSoup(r.text,'html.parser')

          tags_with_href = soup.find_all(href=True)

          link_jobs=[]
          # Print tag names and href values
          for tag in tags_with_href:
              link = tag.get('href')
              if (bool(re.search(r"id\d*.html",link))) :
                  link = "https://vieclam24h.vn" + link
                  link_jobs.append(link)
                  #print("href value:", link)

          for link in link_jobs:
              try :
                  match = re.search(r"id\d*",link)
                  if match :
                      jobid = match.group()
                  else:
                      jobid=""
                  res = requests.get(link,headers=headers)
                  soup =  BeautifulSoup(res.text,'html.parser')
                  #
                  content_divs_1 = soup.find('div', class_='md:ml-7 w-full')
                  lines =[]
                  for div in content_divs_1:
                      lines.append(div.get_text(strip=True, separator=' '))
                  company_name = lines[0]
                  position = lines[1]
                  location = lines[3].split(":")[-1]
                  line = lines[4].split(" ")
                  created_on =  line[7] +" "+ line[8]
                  view = line[-1]
                  content_divs_2 = soup.find('div', class_='mt-3 space-y-1')
                  lines =[]
                  for div in content_divs_2:
                      lines.append(div.get_text(strip=True, separator=' '))
                  company_size = lines[-1].split(":")[-1]  
                  content_divs_3 = soup.find('a', class_='jsx-d84db6a84feb175e')
                  lines =[]
                  for div in content_divs_3:
                      lines.append(div.get_text(strip=True, separator=' '))
                  group_job_function = lines[0]
                  #print(group_job_function)

                  content_divs_4 = soup.find_all('div', class_="ml-3")
                  for div in content_divs_4:
                      text = div.get_text(strip=True, separator=' ')
                      salary_substr="Mức lương : "
                      job_level_substr= 'Cấp bậc '
                      if salary_substr in text:
                          salary = re.sub(re.escape(salary_substr),'',text)
                      if job_level_substr in text:
                          job_level = re.sub(re.escape(job_level_substr),'',text)
                  
                  #company id 
                  tags_with_href = soup.find_all(href=True)
                  for tag in tags_with_href:
                      link = tag.get('href')
                      if (bool(re.search(r"-ntd[\w\d]+.html",link))) :
                          match = re.search(r"ntd[\w\d]+",link)
                          if match :
                              company_id = match.group()
                          else:
                              company_id=""
                  #min max salary
                  match = re.findall(r'\b\d+\b',salary)
                  salaries = [int(num) for num in match]
                  salary_max = max(salaries)
                  salary_min = min(salaries)
                  
                  data = {
                      "job_id" : jobid,
                      "job_title" : position,
                      "company_id" : company_id,
                      "company_name" : company_name,
                      "company_size" : company_size,
                      "location" : location,
                      "job_function" : group_job_function,
                      "group_job_function" : group_job_function,
                      "created_on" : created_on,
                      "salary_max" : salary_max,
                      "salary_min" :salary_min,
                      "salary_estimate" : salary,
                      "job_level" : job_level,
                      "application" : None,
                      "view" : view,
                      "job_board" : "vl24"
                  }

                  insert.insert_data(data)
                
                  #print(data)
                  #print("-----------------")
                  time.sleep(2)
              except :
                  print("\t Fail to crawl link ",link)
                  time.sleep(2)
          page+=1
      else:
          break