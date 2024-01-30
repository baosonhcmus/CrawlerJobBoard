from datetime import datetime
import requests
import pandas as pd
import time
import insert


def data_processing_vnw(df_job):
    columns = ['jobId','jobTitle','createdOn','salaryMax','salaryMin','companyId','companyName','companySize','workingLocations','jobLevelVI','prettySalary','jobFunction','numOfApplications']
    df = df_job[columns]
    columns_name = ['job_id', 'job_title','company_id', 'company_name', 'company_size',
                'location', 'job_function','group_job_function', 'created_on',
                'salary_max','salary_min', 'salary_estimate','job_level','application', 'view','job_board']
    data = pd.DataFrame(columns=columns_name)
    #Dữ liệu dạng số
    data['job_id'] = df['jobId'].astype(int)
    data['company_id'] = df['companyId'].astype(int)
    data['application'] = df['numOfApplications'].astype(int)
    #Dữ liệu cần trích xuất
    data['location'] = df['workingLocations'].apply(lambda x: x[0]['cityNameVI'])
    data['job_function'] = df['jobFunction'].apply(lambda x: x['children'][0]['nameVI'])
    data['group_job_function'] = df['jobFunction'].apply(lambda x: x['parentNameVI'])
    #Dữ liệu không cần xử lý
    data[['job_title','created_on','salary_max','salary_min','salary_estimate','company_name','company_size','job_level']]=df[['jobTitle','createdOn','salaryMax','salaryMin','prettySalary','companyName','companySize','jobLevelVI']]
    data['view'] = None
    data['job_board']= 'vnw'  
    
    values = data.to_dict(orient='records')

    return values

def crawl(api,body,start,max_iteration):
  page = start
  r = requests.post(api, json=body)
  metadata = r.json()
  data = metadata['data']
  columns_name = list(data[0].keys())
  print('Crawling ...')
  while True:
    if page < max_iteration :
      body['page'] = page
      print('\tPage {:}'.format(page))
      try:
        df = pd.DataFrame(columns=columns_name)
        r = requests.post(api, json=body)
        metadata = r.json()
        data = metadata['data']
        for jobinfo in data:
            if int(jobinfo['jobId']) not in list(map(int, df['jobId'])) :
                df = df._append(jobinfo,ignore_index=True)
        values = data_processing_vnw(df)
        insert.insert_data(values)
        page +=1
        time.sleep(2)
      except Exception as e:
        print(f"Error: {e}")
        print('Failed to crawl page {:} !!!'.format(page))
        page +=1
    else :
      break