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
masterData_df = pd.DataFrame(index=None, columns=None)
keeperData_dict = {}
schoolNameKeeper_list = []

# Import system ids
countyName_df = pd.read_excel('countyIDs_small.xls', sheet_name='Sheet1', header=0)
countyName_df_length = len(countyName_df['County Name'])

#=====County Selector FOR Loop=============================================
# Collect County Names from my previously created Georgia BOE database
for countyName_selectorCounter in range(0, countyName_df_length):
    countyName = countyName_df['County Name'][countyName_selectorCounter]
        
    schoolData_inputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\Addresses\\'
    
    schoolData_fileName = countyName #!!!Change this to variable after testing!!!!!!!
    
    schoolData_fileType = '.csv'
    
    schoolData_fullPath = schoolData_inputPath + schoolData_fileName + schoolData_fileType
    
    schoolData_df = pd.read_csv(schoolData_fullPath, header=0)
    
    # Append data to master dataholder dataframe
    masterData_df = pd.concat([masterData_df, schoolData_df], axis=0, ignore_index=True)
    #=================================================================

# Place in alphabetical order by school name
masterData_df_sorted = masterData_df.sort_values(by=['Unnamed: 0'])

masterData_df_length = len(masterData_df_sorted['Unnamed: 0'])

# Import a previously made county school data dictionary to cross reference school names
schoolList_inputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\FinalDataExports\\FinalSchoolList\\'
schoolList_fileName = 'finalSchoolList_full' 
schoolList_fileType = '.csv'
schoolList_fullPath = schoolList_inputPath + schoolList_fileName + schoolList_fileType
schoolList_df = pd.read_csv(schoolList_fullPath, header=None)
schoolList_df_length = len(schoolList_df[0])



for masterData_crossRef_selectorCounter in range(0, masterData_df_length):
    # Add school name and address to keeper list if it doesn't match original data name
    for schoolNameMatch_selectorCounter in range(0, schoolList_df_length):
        
        checkerName = schoolList_df[0][schoolNameMatch_selectorCounter]
        schoolName = masterData_df_sorted['Unnamed: 0'][masterData_crossRef_selectorCounter]
        schoolLat = masterData_df_sorted['Lat'][masterData_crossRef_selectorCounter]
        schoolLong = masterData_df_sorted['Long'][masterData_crossRef_selectorCounter]
        
        if schoolName == checkerName:
            keeperData_dict[schoolName] = {}
            keeperData_dict[schoolName]['Lat'] = schoolLat
            keeperData_dict[schoolName]['Long'] = schoolLong
            schoolNameKeeper_list.append(masterData_df_sorted['Unnamed: 0'][masterData_crossRef_selectorCounter])

# Convert keeper dict to df
keeperData_df = pd.DataFrame(keeperData_dict,index=None, columns=None)

# Place in alphabetical order by school name
keeperData_df_sorted = keeperData_df.sort_index(axis=1)

# Transpose master dataframe to turn schools into columns
#keeperData_df_transpose = keeperData_df.transpose();

'''
# Get length of dropper list
schoolNameDropper_list_length = len(schoolNameKeeper_list)

# Drop school name from list if it is in the dropper list
for schoolNameDropper_selectorCounter in range(0, schoolNameDropper_list_length):
    masterData_df_transpose = masterData_df_transpose.drop(schoolNameKeeper_list[schoolNameDropper_selectorCounter],axis=0)
'''    
#=====Output===============================
# Output path variables
outputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\FinalDataExports\\LatLong\\'

fileType = '.csv'

# Create unique file name
documentFileName = 'latLong_full'
# Construct complete path and file name
filePath = outputPath
if not os.path.exists(filePath):
    os.makedirs(filePath)
fileName = outputPath + documentFileName + fileType

# Export as CSV
keeperData_df_sorted.to_csv(fileName, header=True)

