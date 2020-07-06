from opendatatools import swindex

list_file = "data/sw_index_class1"


def get_sw_class1_list(file):
    '''
    Get the list of SW class1 list and save to file
    :param file:
    :return:
    '''
    df, msg = swindex.get_index_list()
    print(msg)
    df_class_one = df[df['section_name'] == u'一级行业']
    df_class_one.to_csv(file)


get_sw_class1_list(list_file)


#sample

#df_code = df_class_one['index_code']
#df_code_list = df_class_one['index_code'].to_list()
#df_cons, msg = swindex.get_index_cons('801040')
#df_daily, msg = swindex.get_index_daily('801040')

#pass

