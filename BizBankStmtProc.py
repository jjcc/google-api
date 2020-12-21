import pandas as pd
import json
import re

code_list=json.load(open('data/codelist.json'))

def map_regex( input ):
    '''
    Search input string for regex match, then return the associated CODE and SUBCODE
    :param input:
    :return: tuple of CODE and SUBCODE
    '''
    for cm in code_list:
        regex_target = cm[0]
        if re.search(regex_target,input):
            return (cm[1],cm[2])

    return (None,None)




def test_map_regex():
    input = 'CRA PAYROLL  U5Y7X9'
    a,b = map_regex(input)
    print(f'{a},{b}')

def main():
    df = pd.read_csv("data/accountactivity20.csv")
    df['Code'] = df['Description'].map(lambda  x:map_regex(x)[0])
    df['Subcode'] = df['Description'].map(lambda  x:map_regex(x)[1])
    df.to_csv('data/acc20output.csv')

if __name__ == "__main__":
    #test_map_regex()

    main()