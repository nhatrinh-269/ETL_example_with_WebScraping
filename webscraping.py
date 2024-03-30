from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

# Log messages with timestamps
def log(message, path):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now() 
    timestamp = now.strftime(timestamp_format)
    with open(path, "a") as f:
        f.write(timestamp + ',' + message + '\n')

# Perform web scraping
def webscraping(url):
    # Get URL
    response = requests.get(url)
    
    # Retrieve the HTML content of the response
    html_content = response.text
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all tables
    tables = soup.find_all('table')
    list_tables = []
    
    # Iterate over each table found
    for table in tables:
        has_rowspan = False
        # Extract rows from the table's tbody
        rows = table.find('tbody').find_all('tr')
        list_table = []
        
        # Iterate over each row in the table
        for row in rows:
            cell_list = []
            # Extract cells from the row
            cells = row.find_all(['td', 'th'])
            
            # Check if any cell has a rowspan attribute
            if any(cell.has_attr('rowspan') for cell in cells):
                has_rowspan = True
                
            # Extract text from each cell and strip newline characters
            for cell in cells:
                cell_list.append(cell.text.strip('\n'))     
            list_table.append(cell_list)
        
        # Handle rowspan by duplicating data accordingly
        if has_rowspan:
            rank = None
            for i in list_table[1:]:
                if i[0].isdigit():
                    rank = i[0]
                else:
                    i.insert(0, rank)
        
        # Replace special characters in cells
        for i in list_table:
            i[1] = i[1].replace('\xa0', '')
        
        # Append the processed table data to the list of tables
        list_tables.append(list_table)
    
    # Convert each table into a Pandas DataFrame
    list_dataframe = []
    for table in list_tables:
        dataframe = pd.DataFrame(table[1:], columns=table[0])
        list_dataframe.append(dataframe)
        
    return list_dataframe

# Load dataframes into CSV files
def load(target_file, list_dataframe, logfile):
    count = 0
    for i in list_dataframe:
        log("load phase Started", logfile)
        i.to_csv(target_file + str(count) + '.csv', index=False)
        count += 1
        log("load phase Ended", logfile)
        
# Paths and links
target_file = 'path_to_save'  # Provide the path to save CSV files
link = 'https://web.archive.org/web/20200318083015/https://en.wikipedia.org/wiki/List_of_largest_banks'
logfile = target_file + 'log.txt'

# Log the start of the ETL job
log('webscraping phase started', logfile)

# Perform web scraping
list_df = webscraping(link)    

# Log the end of web scraping
log('webscraping phase Ended', logfile)

# Load dataframes into CSV files
load(target_file, list_df, logfile)

# Log the end of the ETL job
log("ETL Job Ended", logfile)
