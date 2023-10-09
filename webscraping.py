from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

def log(message,path):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now() 
    timestamp = now.strftime(timestamp_format)
    with open(path,"a") as f:
        f.write(timestamp + ',' + message + '\n')
        
def webscraping(url):
    response = requests.get(url)
    html_content = response.text
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    tables = soup.find_all('table')
    list_tables = []
    
    for table in tables:
        has_rowspan = False
        rows = table.find('tbody').find_all('tr')
        list_table = []
        for row in rows:
            cell_list = []
            cells = row.find_all(['td', 'th'])
            if any(cell.has_attr('rowspan') for cell in cells):
                has_rowspan = True
            for cell in cells:
                cell_list.append(cell.text.strip('\n'))     
            list_table.append(cell_list)
        if has_rowspan:
            rank = None
            for i in list_table[1:]:
                if i[0].isdigit():
                    rank = i[0]
                else:
                    i.insert(0,rank)
        for i in list_table:
            i[1] = i[1].replace('\xa0','')
        list_tables.append(list_table)
    list_dataframe = []
    for table in list_tables:
        dataframe = pd.DataFrame(table[1:],columns=table[0])
        list_dataframe.append(dataframe)
    return list_dataframe

def load(target_file,list_dataframe,logfile):
    count = 0
    for i in list_dataframe:
        log("load phase Started",logfile)
        i.to_csv(target_file+str(count)+'.csv',index = False)
        count+=1
        log("load phase Ended",logfile)
        
target_file = 'E:/Learn_python/'
link = 'https://web.archive.org/web/20200318083015/https://en.wikipedia.org/wiki/List_of_largest_banks'

logfile = target_file + 'log.txt'

log('webscraping phase started',logfile)

list_df = webscraping(link)    

log('webscraping phase Ended',logfile)

load(target_file,list_df,logfile)

log("ETL Job Ended",logfile)