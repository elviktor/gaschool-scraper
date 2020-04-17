# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 10:29:41 2019

@author: Marco
"""

#=====Import and Declare=========================================
# Import libraries
import os
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
countyID_df = pd.read_excel('countyIDs_small.xls', sheet_name='Sheet1')
countyID_df_length = len(countyID_df['ID'])

#=====County Selector FOR Loop=============================================
for countyID_selectorCounter in range(0, countyID_df_length):
    countyID_int = countyID_df['ID'][countyID_selectorCounter]
    countyID = str(countyID_int)
    countyName = countyID_df['County Name'][countyID_selectorCounter]
    
    # Create Black race percentage and Total population dictionaries
    blackRacialPercentage_dict = {}
    totalPopulation_dict = {}
    # Create fiscal year index FOR loop
    for fiscalYear_counterSelector in range(0, fiscalYear_list_length):
        blackRacialPercentage_dict[fiscalYear_list[fiscalYear_counterSelector]] = {}
        totalPopulation_dict[fiscalYear_list[fiscalYear_counterSelector]] = {}
        
    #=====Year Selector FOR Loop
    for fiscalYear_selectorCounter in range(0, fiscalYear_list_length):
        fiscalYear = fiscalYear_list[fiscalYear_selectorCounter]
        
        # Import year of school county data
        countyDataImportPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\Data\\'
        countyFolder = countyName + '\\' #I need to output to CountyID folders not year
        fileType = '.xlsx'
        fileName = countyDataImportPath + countyFolder + fiscalYear + fileType
        countyYearData_df = pd.read_excel(fileName, sheet_name='Sheet1', header=None)
        countyYearData_df_size = countyYearData_df.size
        countyYearData_df_rowCount = len(countyYearData_df)
        countyYearData_df_columnCount = countyYearData_df_size / countyYearData_df_rowCount
        
        #=====County School Black racial percentage FOR Loop
        for countySchoolData_selectorCounter in range(2, int(countyYearData_df_columnCount)):
        #To Do: 
        #   a) Copy and save school name to storage dictionaries (use if statement to check
        #       if column is already labeled)
            if countyYearData_df[countySchoolData_selectorCounter][7] != 'N/A':
                countyYearData_schoolName = countyYearData_df[countySchoolData_selectorCounter][7]
                totalPopulation_dict[fiscalYear][countyYearData_schoolName] = {}
                blackRacialPercentage_dict[fiscalYear][countyYearData_schoolName] = {}
            elif countyYearData_df[countySchoolData_selectorCounter][7] == 'N/A':
                totalPopulation_dict[fiscalYear][np.nan] = {}
                blackRacialPercentage_dict[fiscalYear][np.nan] = {}
       
        #   b) Collect student population data from county sheet
            countyYearData_asianPop = countyYearData_df[countySchoolData_selectorCounter][1]
            countyYearData_blackPop = countyYearData_df[countySchoolData_selectorCounter][2]
            countyYearData_hispanicPop = countyYearData_df[countySchoolData_selectorCounter][3]
            countyYearData_indianPop = countyYearData_df[countySchoolData_selectorCounter][4]
            countyYearData_multiPop = countyYearData_df[countySchoolData_selectorCounter][5]
            countyYearData_pacificPop = countyYearData_df[countySchoolData_selectorCounter][6]
            countyYearData_whitePop = countyYearData_df[countySchoolData_selectorCounter][8]
        
        #   c) Calculate and store total population number to proper storage DF
            countyYearData_totalPop = countyYearData_asianPop + countyYearData_blackPop + countyYearData_hispanicPop + countyYearData_indianPop + countyYearData_multiPop+ countyYearData_pacificPop + countyYearData_whitePop
            
            totalPopulation_dict[fiscalYear][countyYearData_schoolName] = countyYearData_totalPop
            
        #   d) Calculate and store black race percentage to proper storage DF
            if countyYearData_totalPop != 0:
                countyYearData_blackPercentage = countyYearData_blackPop / countyYearData_totalPop * 100
                blackRacialPercentage_dict[fiscalYear][countyYearData_schoolName] = countyYearData_blackPercentage
            elif countyYearData_totalPop == 0:
                blackRacialPercentage_dict[fiscalYear][countyYearData_schoolName] = 0

        #   e) Print status update
            print('Working!')
            
    #=====Output===============================
    # Output path variables
    outputPath_totalPop = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\Exports\\TotalPopulation\\'
    outputPath_blackPercentage = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\Exports\\BlackPercentage\\'
    countyFolder = countyName + '\\' 
    fileType = '.xlsx'

    # Create unique file name
    documentFileName = countyName
    # Construct complete path and file name
    filePath_totalPop = outputPath_totalPop
    if not os.path.exists(filePath_totalPop):
        os.makedirs(filePath_totalPop)
    fileName_totalPop = outputPath_totalPop + documentFileName + fileType
    
    filePath_blackPercentage = outputPath_blackPercentage
    if not os.path.exists(filePath_blackPercentage):
        os.makedirs(filePath_blackPercentage)
    fileName_blackPercentage = outputPath_blackPercentage + documentFileName + fileType
    
    # Convert dictionary to Pandas dataframe
    totalPopulation_df = pd.DataFrame(totalPopulation_dict)
    blackPercentage_df = pd.DataFrame(blackRacialPercentage_dict)

    # Remove empty rows
    totalPopulation_df.dropna(axis='rows', how='any', inplace=True)
    blackPercentage_df.dropna(axis='rows', how='any', inplace=True)
        
    # Export as CSV
    totalPopulation_df.to_excel(fileName_totalPop)
    blackPercentage_df.to_excel(fileName_blackPercentage)
      