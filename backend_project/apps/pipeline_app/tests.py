from django.test import TestCase
import pandas as pd
# Create your tests here.

def excel_to_dict(path):
    '''读取excel的数据,存储为字典'''
    keys = ['sno','name','gender','birthday','mobile','email','address']
    data = pd.read_excel(path,sheet_name=['student'],header = None,index_col=None, names = keys )
    df = data['student']
    result = []
    for row in df.iterrows():
        result.append(row[1].to_dict())
    return result


if __name__ == "__main__":
    print(excel_to_dict('./test.xlsx'))