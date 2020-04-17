# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 10:29:41 2019

@author: Marco
"""

#=====Import and Declare=========================================
# Import libraries
import requests, bs4, os
import pandas as pd
import numpy as np

# List of fiscal years

fiscalYear_list = ["19951","19953","19961","19963","19971","19973","19981",
                "19983","19991","19993","20001","20003","20011","20013",
                "20021","20023","20031","20033","20041","20043","20051",
                "20053","20061","20063","20071","20073","20081",
                "20083","20091","20093","20101","20103","20111","20113",
                "20121","20123","20131","20133","20141","20143","20151",
                "20153","20161","20163","20171","20173","20181","20183",
                "20191","20193","20201"]

fiscalYear_list_length = len(fiscalYear_list)

# Import system ids
countyID_df = pd.read_excel('countyIDs_small.xls', sheet_name='Sheet1', header=0)
countyID_df_length = len(countyID_df['ID'])

#=====County Selector FOR Loop=============================================
for countyID_selectorCounter in range(0, countyID_df_length):
    countyID_int = countyID_df['ID'][countyID_selectorCounter]
    countyID = str(countyID_int)
    countyName = countyID_df['County Name'][countyID_selectorCounter]
    #=====Year Selector FOR Loop
    for fiscalYear_selectorCounter in range(0, fiscalYear_list_length):
        fiscalYear = fiscalYear_list[fiscalYear_selectorCounter]
        # Declare global variables: root URL string, comment total integer storage, 
        # and global info storage dictionary variable
        rootURL_prefix = "https://oraapp.doe.k12.ga.us/ows-bin/owa/fte_pack_ethnicsex_pub.display_system?p_fiscal_year="
        rootURL_suffix = "&p_system_id="

        rootURL_combined = rootURL_prefix + fiscalYear + rootURL_suffix + countyID
        infoDictionary = {}
        
        #=====Prepare Main FOR Loop===============================
        # Save root URL HTML data into bs4 object
        rootURL_data = requests.get(rootURL_combined)
        rootURL_soup = bs4.BeautifulSoup(rootURL_data.text)
        
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
                # 1) School Name
                schoolData_schoolName = schoolData_list[1].string
                infoDictionary[schoolIngestionCounter]['School Name'] = schoolData_schoolName
                # 2) Ethnic Hispanic
                schoolData_ethnicHispanic_int = 0
                schoolData_ethnicHispanic = schoolData_list[3].string
                if schoolData_ethnicHispanic == '*':
                    schoolData_ethnicHispanic_int = 0
                    infoDictionary[schoolIngestionCounter]['Ethnic Hispanic'] = schoolData_ethnicHispanic_int
                elif schoolData_ethnicHispanic != '*':
                    schoolData_ethnicHispanic = schoolData_ethnicHispanic.replace(',', '')
                    schoolData_ethnicHispanic_int = int(schoolData_ethnicHispanic)
                    infoDictionary[schoolIngestionCounter]['Ethnic Hispanic'] = schoolData_ethnicHispanic_int
                # 3) Indian
                schoolData_indian_int = 0
                schoolData_indian = schoolData_list[4].string
                if schoolData_indian == '*':
                    schoolData_indian_int = 0
                    infoDictionary[schoolIngestionCounter]['Indian'] = schoolData_indian_int
                elif schoolData_indian != '*':
                    schoolData_indian = schoolData_indian.replace(',', '')
                    schoolData_indian_int = int(schoolData_indian)
                    infoDictionary[schoolIngestionCounter]['Indian'] = schoolData_indian_int
                # 4) Asian
                schoolData_asian_int = 0
                schoolData_asian = schoolData_list[5].string
                if schoolData_asian == '*':
                    schoolData_asian_int = 0
                    infoDictionary[schoolIngestionCounter]['Asian'] = schoolData_asian_int
                elif schoolData_asian != '*':
                    schoolData_asian = schoolData_asian.replace(',', '')
                    schoolData_asian_int = int(schoolData_asian)
                    infoDictionary[schoolIngestionCounter]['Asian'] = schoolData_asian_int
                # 5) Black
                schoolData_black_int = 0
                schoolData_black = schoolData_list[6].string
                if schoolData_black == '*':
                    schoolData_black_int = 0
                    infoDictionary[schoolIngestionCounter]['Black'] = schoolData_black_int
                elif schoolData_black != '*':
                    schoolData_black = schoolData_black.replace(',', '')
                    schoolData_black_int = int(schoolData_black)
                    infoDictionary[schoolIngestionCounter]['Black'] = schoolData_black_int
                # 6) Pacific
                schoolData_pacific_int = 0
                schoolData_pacific = schoolData_list[7].string
                if schoolData_pacific == '*':
                    schoolData_pacific_int = 0
                    infoDictionary[schoolIngestionCounter]['Pacific'] = schoolData_pacific_int
                elif schoolData_pacific != '*':
                    schoolData_pacific = schoolData_pacific.replace(',', '')
                    schoolData_pacific_int = int(schoolData_pacific)
                    infoDictionary[schoolIngestionCounter]['Pacific'] = schoolData_pacific_int
                # 7) White
                schoolData_white_int = 0
                schoolData_white = schoolData_list[8].string
                if schoolData_white == '*':
                    schoolData_white_int = 0
                    infoDictionary[schoolIngestionCounter]['White'] = schoolData_white_int
                elif schoolData_white != '*':
                    schoolData_white = schoolData_white.replace(',', '')
                    schoolData_white_int = int(schoolData_white)
                    infoDictionary[schoolIngestionCounter]['White'] = schoolData_white_int
                # 8) Multi
                schoolData_multi_int = 0
                schoolData_multi = schoolData_list[9].string
                if schoolData_multi == '*':
                    schoolData_multi_int = 0
                    infoDictionary[schoolIngestionCounter]['Multi'] = schoolData_multi_int
                elif schoolData_multi != '*':
                    schoolData_multi = schoolData_multi.replace(',', '')
                    schoolData_multi_int = int(schoolData_multi)
                    infoDictionary[schoolIngestionCounter]['Multi'] = schoolData_multi_int
            elif schoolData_checkIfATotalRow_string != 'Total':
                infoDictionary[schoolIngestionCounter] = np.nan
            print('Working!')
        
        #===============================================================
        
        #=====Output===============================
        # Output path variables
        outputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\Data\\'
        countyFolder = countyName + '\\' #I need to output to CountyID folders not year
        fileType = '.xlsx'
        '''
        # Retrieve file name
        schoolsData_pageTitle_list = rootURL_soup.select('th')
        schoolsData_pageTitle_string = schoolsData_pageTitle_list[0].string
        schoolsData_pageTitle_string = schoolsData_pageTitle_string.replace('/',' ')
        '''
        # Create unique file name
        documentFileName = fiscalYear
        # Construct complete path and file name
        filePath = outputPath + countyFolder
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        fileName = outputPath + countyFolder + documentFileName + fileType
        # Convert dictionary to Pandas dataframe
        infoDictionary_df = pd.DataFrame(infoDictionary)
        # Remove empty rows
        infoDictionary_df.dropna(axis='columns', how='all', inplace=True)
        # Export as CSV
        infoDictionary_df.to_excel(fileName)
