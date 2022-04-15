#!/user/bin/env python3 -tt
"""
This Module contains Generic Data Processing APIs for HPC Datasets.
"""
import re
import os
import HISyn_copy.tools.Log as log

import pandas as pd

"""Extract Columns from the Dataset 
            Arguments: 
            File= Path to the file,
            ColumnNames = Comma separated column names
"""
def GetColumn(columnNames, file):
    dataset = pd.read_csv(file)
    df = pd.DataFrame(dataset)
    c_names= columnNames.split(',')
    column=[]
    for each in c_names:
        column.append(each)
    df = df[column]
    print(df.head(10))
    df.to_csv(r'./ExtractColumn.csv', index=False, header=True)
    return df

"""Get Column names from the Dataset 
            Arguments: 
            File= Path to the file,          
"""
def GetColumnNames(file):
    dataset = pd.read_csv(file)
    df = pd.DataFrame(dataset)
    my_list = list(df)
    print(my_list)
    return my_list

"""Do Column Multiplication in a Dataset 
            Arguments: 
            File= Path to the file,
            Col1,col2 = Names of the columns to be multiplied
"""
def Multiplication(col1,col2, file):
    dataset = pd.read_csv(file)
    df = pd.DataFrame(dataset)
    mul = df[col1] * df [col2]
    print(mul.head(10))
    return mul

"""Merge two Datasets and create a new CSV file 
            Arguments: 
            File1, File2= Path to the files to be merged
"""
def MergeDataset(file1,file2):
    df1= pd.DataFrame(pd.read_csv(file1))
    df2 = pd.DataFrame(pd.read_csv(file2))
    df = pd.concat((df1, df2), axis=1)
    print(df.head(10))
    df.to_csv(r'./MergeDataset.csv', index=False, header=True)
    return df

"""Convert JSON file into CSV 
            Arguments: 
            File= Path to the file,
"""
def convertJSON_to_CSV(file):
    read_file = pd.read_json(file)
    print(read_file)
    read_file.to_csv(r'./Converted.csv', index=None)
    return read_file


def hpc_parse(text):
    concept_regex = r'(string\([^\)]+\))'
    match = re.search(concept_regex, text)
    while match:
        newtext = match.group().lstrip("string")
        newtext = newtext [1:-1]
        text = text.replace(match.group(), "\""+newtext+"\"", 1)
        match = re.search(concept_regex, text)

    return text
def file(file):
    return file

def columnName(column):
    return column

def executeWorkflow(expression):
    log.log('Executing Workflow :')
    expression = hpc_parse(expression)
    exec(expression)
    
    #GetColumn(columnName("memLocal,memAtomic,wgSize,coalesced"), file("cgo17-nvidia.csv"))
    #GetColumn(columnName(hpc_arg(memLocal, memAtomic, wgSize, coalesced)), file(hpc_arg(cgo17 - nvidia.csv)))
    #Extract "Memory Frequency" and "Kernel" columns from file "AWS_top5_2688data.csv"
    #ExtractColumn("Memory Frequency,Kernel",'./AWS_top5_2688data.csv')
    #GetColumnNames('./AWS_top5_2688data.csv')
    #Multiplication('SOL L2','Duration','./AWS_top5_2688data.csv')
    #MergeDataset('./ExtractColumn_2.csv','./ExtractColumn.csv')
    #convertJSON_to_CSV('./spec_speed.json')


