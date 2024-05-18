# ETL example with Webscraping

In this project I will show a simple example of building ETL(Extract-Tranform-Loading) with webscraping. By collecting all the tabular data on Wiki. 

## Description

The Python script utilizes the BeautifulSoup library for web scraping and the Pandas library for data manipulation. It performs the following tasks:

1. **Web Scraping**: 
   - Fetches data from a specified Wikipedia page containing a list of the largest banks.
   - Parses the HTML content using BeautifulSoup to extract tabular data.

2. **Data Processing**:
   - Processes the extracted data to handle special characters and table formats.
   - Converts the tabular data into Pandas DataFrames for further processing.

3. **Data Loading**:
   - Saves each DataFrame into separate CSV files.

## Prerequisites

To run the script, ensure you have the following installed:

- Python 3.x
- BeautifulSoup library (`beautifulsoup4`)
- Requests library (`requests`)
- Pandas library (`pandas`)

