# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 10:17:59 2020

@author: Marco
"""


#=====Import and Declare=========================================
# Import libraries
import os
import pandas as pd


# Initialize Variables
rootPath = 'C:\\Users\\Marco\\Desktop\\Documentary\\20190502_SavannahSchoolPioneers\\WebScraper\\FinalDataExports\\FinalFinalExports\\V2\\'
fileName = 'latLong_full_noquestions'
fileType = '.csv'
fileName_full = rootPath + fileName + fileType
fileName_export = "savschoolModels_school.json"
fileName_export_full = rootPath + fileName_export
appName = "savschools"
modelName = "school"
school_name = ""
latitude = 0
longitude = 0

# Create data holder dataframe
schoolData_df = pd.DataFrame(index=None, columns=None)
schoolData_dict = {}
schoolData_master = []

# Import data
schoolData_df = pd.read_csv(fileName_full, header=None)
schoolData_df_size = schoolData_df.size
schoolData_df_rowCount = len(schoolData_df)
schoolData_df_columnCount = schoolData_df_size / schoolData_df_rowCount
schoolData_df_columnCount = int(schoolData_df_columnCount)

for schoolData_cs in range(1, schoolData_df_columnCount):
    schoolData_dict["model"] = appName + "." + modelName
    schoolData_dict["pk"] = schoolData_cs
    schoolData_dict["fields"] = {"school_name":schoolData_df[schoolData_cs][0],"latitude":schoolData_df[schoolData_cs][1],"longitude":schoolData_df[schoolData_cs][2]}
    
    schoolData_string = str(schoolData_dict)
    schoolData_master.append(schoolData_string)


print(schoolData_master)
schoolData_string = str(schoolData_master)

document = open(fileName_export_full, "w")
document.write(schoolData_string)
document.close()
    