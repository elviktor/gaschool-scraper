# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 10:29:41 2019

@author: Marco
"""

#=====Import and Declare=========================================
# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests, bs4, os, re
import pandas as pd

# Create school address database dictionary
schoolAddress_dict = {}

# Import system ids
countyName_df = pd.read_excel('countyIDs_small.xls', sheet_name='Sheet1', header=0)
countyName_df_length = len(countyName_df['County Name'])

# Declare Root URL variables
rootURL_prefix = 'http://georgia.educationbug.org/public-schools/county-'
rootURL_suffix = '.html'

#=====County Selector FOR Loop=============================================
# Collect County Names from my previously created Georgia BOE database
for countyName_selectorCounter in range(0, countyName_df_length):
    countyName = countyName_df['County Name'][countyName_selectorCounter]
    countyName_filter = re.compile("([^\n\r]*).*County*")
    countyName_filtered = countyName_filter.search(countyName)
    countyName_filtered_string = countyName_filtered[1]
    countyName_filtered_lower = countyName_filtered_string.lower()
    
    # Add County name to school address data dictionary
    schoolAddress_dict = {}
    
    # Build County Name URL
    countyURL = rootURL_prefix + countyName_filtered_lower + rootURL_suffix
    
    # Save County Name URL HTML data into bs4 object
    countyURL_data = requests.get(countyURL)
    countyURL_soup = bs4.BeautifulSoup(countyURL_data.text)
    
    # Get school name and url
    schoolName_list = countyURL_soup.select('table .schoolDataset td a')
    schoolName_list_length = len(schoolName_list)
    
    #========BEGIN SCHOOL FOR LOOP
    for schoolAddress_selectorCounter in range(0, schoolName_list_length):
        schoolName_list_row = schoolName_list[schoolAddress_selectorCounter]
        schoolName_string = schoolName_list_row.string
        schoolName_URL = schoolName_list_row.get('href')
        
        # Import a previously made county school data dictionary to cross reference school names
        schoolData_inputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\Exports\\TotalPopulation\\'
        schoolData_fileName = countyName #!!!Change this to variable after testing!!!!!!!
        schoolData_fileType = '.xlsx'
        schoolData_fullPath = schoolData_inputPath + schoolData_fileName + schoolData_fileType
        schoolData_df = pd.read_excel(schoolData_fullPath, sheet_name='Sheet1', header=None)
        schoolData_df_length = len(schoolData_df[0])
        
        # Add school name and address to dictionary if it matches original data name
        for schoolNameMatch_selectorCounter in range(1, schoolData_df_length):
            if schoolName_string == schoolData_df[0][schoolNameMatch_selectorCounter]:
                 # Save School URL HTML data into bs4 object
                schoolURL_data = requests.get(schoolName_URL)
                schoolURL_soup = bs4.BeautifulSoup(schoolURL_data.text)
                
                # Get school address
                schoolAddress_list = schoolURL_soup.select('div .dContent')
                schoolAddress_address = schoolAddress_list[0].contents
                schoolAddress_street = schoolAddress_address[0]
                schoolAddress_street = str(schoolAddress_street) 
                schoolAddress_state = schoolAddress_address[2]
                schoolAddress_state = schoolAddress_state.replace('\t','')
                schoolAddress_state = schoolAddress_state.replace('\n',' ')
                schoolAddress_state = schoolAddress_state.replace(',',' ')
                schoolAddress_complete = schoolAddress_street + schoolAddress_state
                
                # Place School Name and Address into LatLong Database Dictionary

                # Type school address in the latlong.net search bar
                # Setup Selenium and target latlong.net
                browser = webdriver.Chrome()
                browser.get('https://get-direction.com/address-to-lat-long.html')
                elem = browser.find_element_by_id('txtPlace')
                elem.clear()
                elem.send_keys(schoolAddress_complete)
                elem.send_keys(Keys.RETURN)
                
                # Get HTML data from source and parse with BS4
                page_HTML = browser.page_source
                page_soup = bs4.BeautifulSoup(page_HTML, 'html.parser')
                
                latLong_list = page_soup.find(id='latlongDDD')
                latLong_string = latLong_list.string
                
                # Check to see if data has loaded, if not reload page data
                if latLong_string == "??.?????????, ??.?????????":
                    for x in range(0, 100):
                        page_HTML = browser.page_source
                        page_soup = bs4.BeautifulSoup(page_HTML, 'html.parser')
                        latLong_list = page_soup.find(id='latlongDDD')
                        latLong_string = latLong_list.string
                        if latLong_string != "??.?????????, ??.?????????":
                            break
                
                latLong_array = [x.strip() for x in latLong_string.split(',')]
                lat = latLong_array[0]
                long = latLong_array[1]
                
                # Add address to dictionary                
                schoolAddress_dict[schoolName_string] = {}
                schoolAddress_dict[schoolName_string]['Lat'] = lat
                schoolAddress_dict[schoolName_string]['Long'] = long
                #schoolAddress_dict[schoolName_string]['Address'] = schoolAddress_complete
                #schoolAddress_dict[schoolName_string]['URL'] = schoolName_URL
                
                browser.quit()
    
    #=====Output===============================
    # Output path variables
    outputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\Addresses\\'
    #countyFolder = countyName + '\\' #I need to output to CountyID folders not year
    fileType = '.csv'

    # Create unique file name
    documentFileName = countyName
    # Construct complete path and file name
    filePath = outputPath
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    fileName = outputPath + documentFileName + fileType
    # Convert dictionary to Pandas dataframe
    schoolAddress_df = pd.DataFrame(schoolAddress_dict)
    schoolAddress_df_transpose = schoolAddress_df.transpose();
    # Remove empty rows
    #schoolAddress_df.dropna(axis='columns', how='all', inplace=True)
    # Export as CSV
    schoolAddress_df_transpose.to_csv(fileName)
    #=================================================================