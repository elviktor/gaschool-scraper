# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 10:29:41 2019

@author: Marco
"""

#=====Import and Declare=========================================
# Import libraries
import os
import pandas as pd

# Create data holder dataframe
keeperData_df = pd.DataFrame(index=None, columns=None)
keeperData_dict = {}
schoolNameKeeper_list = []

#=====County Selector FOR Loop=============================================
# Import full school data sheet
schoolData_inputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\FinalDataExports\\TotalPopulation\\'
schoolData_fileName = 'totalPopulation_full' #!!!Change this to variable after testing!!!!!!!
schoolData_fileType = '.csv'
schoolData_fullPath = schoolData_inputPath + schoolData_fileName + schoolData_fileType
schoolData_df = pd.read_csv(schoolData_fullPath, header=None)
schoolData_df_size = schoolData_df.size
schoolData_df_columnHeight = len(schoolData_df[0])
schoolData_df_columnNumber = int(schoolData_df_size / schoolData_df_columnHeight)

# Import list of latLong school names
schoolList_inputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\FinalDataExports\\LatLong\\'
schoolList_fileName = 'latLong_names' 
schoolList_fileType = '.csv'
schoolList_fullPath = schoolList_inputPath + schoolList_fileName + schoolList_fileType
schoolList_df = pd.read_csv(schoolList_fullPath, header=None)
schoolList_df_length = len(schoolList_df[0])

for column_selectorCounter in range(1, schoolData_df_columnNumber):
    # Add school name and address to keeper list if it doesn't match original data name
    for schoolNameMatch_selectorCounter in range(0, schoolList_df_length):
        
        checkerName = schoolList_df[0][schoolNameMatch_selectorCounter]
        schoolName = schoolData_df[column_selectorCounter][0]
        
        if schoolName == checkerName:
            keeperData_df[schoolName] = schoolData_df[column_selectorCounter]
    
#=====Output===============================
# Output path variables
outputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\FinalDataExports\\TotalPopulation\\'

fileType = '.csv'

# Create unique file name
documentFileName = 'totalPopulation_full_trim'
# Construct complete path and file name
filePath = outputPath
if not os.path.exists(filePath):
    os.makedirs(filePath)
fileName = outputPath + documentFileName + fileType

# Export as CSV
keeperData_df.to_csv(fileName, header=0)
