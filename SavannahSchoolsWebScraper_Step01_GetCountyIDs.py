# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 10:29:41 2019

@author: Marco
"""

#=====Import and Declare=========================================
# Import libraries
import requests, bs4, re
import pandas as pd
import numpy as np

# Declare global variables: root URL string, comment total integer storage, 
# and global info storage dictionary variable

rootURL_prefix = "https://oraapp.doe.k12.ga.us/ows-bin/owa/fte_pack_ethnicsex_pub.display_system?p_fiscal_year="
fiscal_year = "20201"
rootURL_suffix = "&p_system_id="
system_id = "761"
#rootURL_combined = rootURL_prefix + fiscal_year + rootURL_suffix + system_id
rootURL_combined = "https://oraapp.doe.k12.ga.us/ows-bin/owa/fte_pack_ethnicsex_pub.display_allsystem?p_fiscal_year=20201"
infoDictionary = {}

#=====Prepare Main FOR Loop===============================
# Save root URL HTML data into bs4 object
rootURL_data = requests.get(rootURL_combined)
rootURL_soup = bs4.BeautifulSoup(rootURL_data.text)

'''
#==========Function Test Zone===================================
pageDataTables = rootURL_soup.select('table')
schoolsDataTable_list = pageDataTables[0]
schoolsData_list = schoolsDataTable_list.select('tr')
schoolsData_list_length = len(schoolsData_list)
schoolData_list = schoolsData_list[8].select('td')  #can automate this total tr elements
schoolData_checkIfATotalRow_string = schoolData_list[2].string 
#====Info about schoolData_list rows:=========
print(schoolData_list[1]) # Row[1] = School name
print(schoolData_list[2]) # Row[2] = *Check if Total/Male/Female
print(schoolData_list[3]) # Row[3] = *Ethnic Hispanic
print(schoolData_list[4]) # Row[4] = *Indian
print(schoolData_list[5]) # Row[5] = *Asian
print(schoolData_list[6]) # Row[6] = *Black
print(schoolData_list[7]) # Row[7] = *Pacific
print(schoolData_list[8]) # Row[8] = *White
print(schoolData_list[9]) # Row[9] = *Multi
#====Get school data from rows
schoolData_schoolName = schoolData_list[1].string
print(schoolData_schoolName) #Add to dictionary under name key
'''

#======FOR Loop: Data Ingestion=======================================
pageDataTables = rootURL_soup.select('table')
schoolsDataTable_list = pageDataTables[0]
schoolsData_list = schoolsDataTable_list.select('tr')
schoolsData_list_length = len(schoolsData_list)

for schoolIngestionCounter in range(3, schoolsData_list_length):
    # Append unique reviewer dictionary to info storage dictionary
    infoDictionary[schoolIngestionCounter] = {}
    schoolData_list = schoolsData_list[schoolIngestionCounter].select('td')  #can automate this total tr elements
    schoolData_checkIfATotalRow_string = schoolData_list[2].string 
    
    # Append only 'Total' rows to dictionary
    if schoolData_checkIfATotalRow_string == 'Total':
        # Append school row data to dictionary
        # 1) School ID
        schoolData_schoolID = schoolData_list[0].string
        infoDictionary[schoolIngestionCounter]['School ID'] = schoolData_schoolID
        # 2) School Name
        schoolData_schoolName = schoolData_list[1].string
        infoDictionary[schoolIngestionCounter]['School Name'] = schoolData_schoolName
    elif schoolData_checkIfATotalRow_string != 'Total':
        infoDictionary[schoolIngestionCounter] = np.nan

#===============================================================




#=====Output===============================

# Output path variables
outputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\Data\\Test\\'
fileType = '.xlsx'
# Retrieve file name
schoolsData_pageTitle_list = rootURL_soup.select('th')
schoolsData_pageTitle_string = schoolsData_pageTitle_list[0].string
schoolsData_pageTitle_string = schoolsData_pageTitle_string.replace('/',' ')
# Construct complete path and file name
filename = outputPath + schoolsData_pageTitle_string + fileType
# Convert dictionary to Pandas dataframe
infoDictionary_df = pd.DataFrame(infoDictionary)
# Remove empty rows
infoDictionary_df.dropna(axis='columns', how='all', inplace=True)
print(infoDictionary_df)
# Export as Excel
infoDictionary_df.to_excel(filename)

