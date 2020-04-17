# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 10:29:41 2019

@author: Marco
"""

#=====Import and Declare=========================================
# Import libraries
import os
import pandas as pd

# List of fiscal years
fiscalYear_list = ["","19951","19953","19961","19963","19971","19973","19981",
                "19983","19991","19993","20001","20003","20011","20013",
                "20021","20023","20031","20033","20041","20043","20051",
                "20053","20061","20063","20071","20073","20081",
                "20083","20091","20093","20101","20103","20111","20113",
                "20121","20123","20131","20133","20141","20143","20151",
                "20153","20161","20163","20171","20173","20181","20183",
                "20191","20193","20201"]

# Create data holder dataframe
masterData_df = pd.DataFrame()

# Import system ids
countyName_df = pd.read_excel('countyIDs_small.xls', sheet_name='Sheet1', header=0)
countyName_df_length = len(countyName_df['County Name'])

#=====County Selector FOR Loop=============================================
# Collect County Names from my previously created Georgia BOE database
for countyName_selectorCounter in range(0, countyName_df_length):
    countyName = countyName_df['County Name'][countyName_selectorCounter]
        
    # Import a previously made county school data dictionary to cross reference school names
    #schoolData_inputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\Exports\\TotalPopulation\\'
    schoolData_inputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\Exports\\BlackPercentage\\'
    
    schoolData_fileName = countyName #!!!Change this to variable after testing!!!!!!!
    
    schoolData_fileType = '.xlsx'
    
    schoolData_fullPath = schoolData_inputPath + schoolData_fileName + schoolData_fileType
    
    schoolData_df = pd.read_excel(schoolData_fullPath, sheet_name='Sheet1', header=None, index=None)
    
    
    # Place in alphabetical order by school name
    #schoolData_df_sorted = schoolData_df.sort_values(by=[0])
    # Convert dictionary to Pandas dataframe
    #schoolData_df_transpose = schoolData_df_sorted[:-1].transpose();
    
    # Append data to master dataholder dataframe
    masterData_df = pd.concat([masterData_df, schoolData_df[1:]], axis=0)
    #=================================================================

# Place in alphabetical order by school name
masterData_df_sorted = masterData_df.sort_values(by=[0])
# Convert dictionary to Pandas dataframe
#masterData_df_transpose = masterData_df_sorted.transpose();

#=====Output===============================
# Output path variables
#outputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\FinalDataExports\\TotalPopulation\\'
outputPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\FinalDataExports\\FinalSchoolList\\'

fileType = '.csv'

# Create unique file name
documentFileName = 'finalSchoolList_full'
# Construct complete path and file name
filePath = outputPath
if not os.path.exists(filePath):
    os.makedirs(filePath)
fileName = outputPath + documentFileName + fileType

# Export as CSV
masterData_df_sorted.to_csv(fileName, header=False, index=False)
