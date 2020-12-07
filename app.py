from flask import Flask
from flask import render_template
from flask import request
import os
import pandas as pd

app = Flask(__name__, static_url_path='',
            static_folder='Finance',
            template_folder='templates')
#PATH
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'Finance')
APP_STATIC_DATA = os.path.join(APP_STATIC, 'data')
APP_STATIC_COMPJ= os.path.join(APP_STATIC_DATA, 'compj')
APP_STATIC_COMP= os.path.join(APP_STATIC_DATA, 'comp')

#Dictionary
SW_LIST = {}  # dictionary of component list with key as index code



def load_meta():
    '''
    Load SW_LIST
    :return:
    '''
    list_file = os.path.join(APP_STATIC_DATA,'sw_index_class1')
    df_indexlist = pd.read_csv(list_file)
    df_indexlist = df_indexlist.set_index('index_code')
    for code, row in df_indexlist.iterrows():
        name = row["index_name"]
        print(u"code:%d, name:%s" % (code, name))
        json_file = os.path.join(APP_STATIC_COMPJ,f'{code}_componentsx.json')
        #file = 'data/comp/801010_components.csv'
        df_comp_one = pd.read_json(json_file,dtype = {"stock_code" : "str"})
        df_selected = df_comp_one[['stock_code', 'stock_name', 'weight']]
        SW_LIST[code] = df_selected

load_meta()

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/stocksinsector')
def show_stocks_in_sector():


    sw_code = request.args.get('cd')
    start = request.args.get('st')
    count = request.args.get('cnt')

    # with open(os.path.join(APP_STATIC,'record.txt'),'w') as f:
    #     f.write(f"sw:{sw_code}")
    component_list = SW_LIST[int(sw_code)]
    list_as_str = '#'.join(component_list['stock_code'].to_list())

    cd_list = component_list[['stock_code','stock_name']].to_records().tolist()[int(start):int(start)+int(count)]
    model = {"code":sw_code,"count":count, "start":start,"list":list_as_str, "cd_list":cd_list}
    return render_template('stocks_in_sector.html', model=model)


if __name__ == '__main__':

    app.run(debug=True)
