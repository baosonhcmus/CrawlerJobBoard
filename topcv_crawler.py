from selenium.webdriver.firefox.options import Options as FirefoxOptions
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time
import re
import insert

import warnings
warnings.filterwarnings("ignore")


options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)


def run_script(driver):

    # html = driver.page_source
    # print(html)

    columns_name = ['job_id', 'job_title','company_id', 'company_name', 'company_size',
                'location', 'job_function','group_job_function', 'created_on',
                'salary_max','salary_min', 'salary_estimate','job_level','application', 'view','job_board']
    df = pd.DataFrame(columns=columns_name)

    #JOBID
    jobId_list =[]
    job_link =[]
    elements_link = driver.find_elements(By.TAG_NAME,'a')
    href_values = [element.get_attribute('href') for element in elements_link]
    for href_value in href_values:
        if (bool(re.search(r"JobSearchList_LinkDetail",str(href_value)))):
            #print(f"Link Href: {href_value}")
            job_link.append(href_value)
            match = re.search(r"\d+(?=(\.html))",href_value)
            if match :
                jobid = match.group()
            else:
                jobid=""
            jobId_list.append(jobid)
        jobId_list = list(dict.fromkeys(jobId_list))
        job_link = list(dict.fromkeys(job_link))
    numJob = len(jobId_list)
    #print(numJob)

    #JOBTITLE
    jobTitles =[]
    jobTitle_list= []
    tag_name = 'h3'
    class_name = 'title'
    elements_jobTitle = driver.find_elements(By.CSS_SELECTOR, f"{tag_name}.{class_name}")
    text_contents = [element.text for element in elements_jobTitle]
    for text_content in text_contents:
      jobTitle = text_content.split("\n")[-1]
      #print(f"Element Text: {jobTitle}")
      jobTitles.append(jobTitle)
    jobTitle_list=jobTitles[0:numJob]
    #print(len(jobTitle_list))

    #JOBCOMPANY
    company =[]
    elements = driver.find_elements(By.CLASS_NAME, "company")
    text_contents = [element.text for element in elements]
    for text_content in text_contents:
      #print(f"Element Text: {text_content}")
      company.append(text_content)
    company_list = company[0:numJob]
    #print(len(company_list))

    #SALARY
    salary =[]
    salary_min_list=[]
    salary_max_list=[]
    elements = driver.find_elements(By.CLASS_NAME,"title-salary")
    text_contents = [element.text for element in elements]
    for text_content in text_contents:
      #print(f"Element Text: {text_content}")
      salary.append(text_content)
      temp = text_content.replace(',','').replace(',','')
      match = re.findall(r'\b\d+\b',text_content)
      salaries = [int(num) for num in match]
      if (len(salaries)):
        salary_max = max(salaries)
        salary_min = min(salaries)
      else :
        salary_max = None
        salary_min = None
      salary_max_list.append(salary_max)
      salary_min_list.append(salary_min)
    salary_list = salary[0:numJob]
    salary_max_list = salary_max_list[0:numJob]
    salary_min_list = salary_min_list[0:numJob]
    #print(len(salary_list))

    #SUBMIT_DEADLINE
    submit_deadline = []
    elements = driver.find_elements(By.CLASS_NAME,"time")
    text_contents = [element.text for element in elements]
    for text_content in text_contents:
      #print(f"Element Text: {text_content}")
      num_days_ago = int(text_content.split(' ')[1])
      current_time = datetime.now()
      result_date = (current_time - timedelta(days=num_days_ago)).date()
      submit_deadline.append(str(result_date))
      #print(result_date)
    #len(submit_deadline)

    #ADDRESS + CREATEON
    line =[]
    address =[]
    createOn = []
    elements = driver.find_elements(By.CLASS_NAME,"address")
    text_contents = [element.text for element in elements]
    for text_content in text_contents:
      #print(f"Element Text: {text_content}")
      line.append(text_content)
    for i in range(0,numJob):
      address.append(line[2*i])
      times = line[2*i+1]
      minutes = 0
      hours = 0
      days = 0
      weeks = 0
      temp = times.split(" ")[2]
      num = times.split(" ")[3]
      if (temp == "phút") :
        minutes = int(num)
      if (temp == "giờ"):
        hours = int(num)
      elif (temp == "ngày") :
        days = int(num)
      elif (temp == "tuần") :
        weeks = int(num)
      current_time = datetime.now()
      result_time = current_time - timedelta(minutes=minutes,hours=hours,days=days,weeks=weeks)
      createOn.append(str(result_time))
    #print(address)
    #print(createOn)
    
    driver.close()

    company_size_list =[]
    job_level_list =[]
    job_function_list=[]

    for link in job_link:
      try:
        #print(link)
        driver = webdriver.Firefox(options=options)
        driver.get(link)
        time.sleep(5)
        #COMPANYSIZE
        elements = driver.find_elements(By.CLASS_NAME,"company-value")
        text_contents = [element.text for element in elements]
        if text_contents :
          company_size = text_contents[0]
        else :
          company_size = None
        company_size_list.append(company_size)
        #print(company_size)

        #JOBLEVEL
        elements = driver.find_elements(By.CLASS_NAME,"box-general-group-info-value")
        text_contents = [element.text for element in elements]
        if text_contents :
          job_level = text_contents[0]
        else :
          job_level = None

        elements = driver.find_elements(By.CLASS_NAME,"general-information-data")
        text_contents = [element.text for element in elements]
        for text_content in text_contents:
         job_level_substr="Cấp bậc\n"
         if job_level_substr in text_content:
            job_level = re.sub(re.escape(job_level_substr),'',text_content)
        job_level_list.append(job_level)
        #print(job_level)

        #JOBFUNCTION
        job_function = None
        elements = driver.find_elements(By.CLASS_NAME,"box-category")
        text_contents = [element.text for element in elements]
        for text_content in text_contents:
          job_function_substr="Ngành nghề\n"
          if job_function_substr in text_content:
            job_function = re.sub(re.escape(job_function_substr),'',text_content)

        elements = driver.find_elements(By.CLASS_NAME,"premium-job-related-tags__section")
        text_contents = [element.text for element in elements]
        for text_content in text_contents:
          job_function_substr="Ngành nghề\n"
          if job_function_substr in text_content:
            job_function = re.sub(re.escape(job_function_substr),'',text_content)
        if job_function :
          job_function = job_function.replace('\n',', ')
        #print(job_function)
        job_function_list.append(job_function)
        
        driver.close()

      except Exception as Eror:
        print("Eror: ",Eror)
        print("Fail crawl link ",link)
        driver.close()
    for i in range(0,numJob-1) :
      data = {
                      "job_id" : jobId_list[i],
                      "job_title" : jobTitle_list[i],
                      "company_id" : company_list[i],
                      "company_name" : company_list[i],
                      "company_size" : company_size_list[i],
                      "location" : address[i],
                      "job_function" : job_function_list[i],
                      "group_job_function" : job_function_list[i],
                      "created_on" : createOn[i],
                      "salary_max" : salary_max_list[i],
                      "salary_min" :salary_min_list[i],
                      "salary_estimate" : salary_list[i],
                      "job_level" : job_level_list[i],
                      "application" : None,
                      "view" : None,
                      "job_board" : "topcv"
                  }
      df = df._append(data,ignore_index=True)
      insert.insert_data(data)
    return df

def crawl(start,max_iteration):
    page = start
    columns_name = ['job_id', 'job_title','company_id', 'company_name', 'company_size',
                'location', 'job_function','group_job_function', 'created_on',
                'salary_max','salary_min', 'salary_estimate','job_level','application', 'view','job_board']
    data = pd.DataFrame(columns=columns_name)
    #driver = webdriver.Chrome(options=chrome_options)
    print('Crawling ...')
    while True:
      if (page < max_iteration) :
        print("\t Page {:}".format(page))
        url = "https://www.topcv.vn/tim-viec-lam-moi-nhat?page=" + str(page)
        try:
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)

            df = run_script(driver)
            #print(df)
            data = pd.concat([data,df], ignore_index=True)
            #print(data)
            page +=1

        except Exception as Eror:
          print("Eror: ",Eror)
          print("Fail crawl link ",url)
          page +=1

      else :
        return data
      


data = crawl(1,20)

driver.quit()