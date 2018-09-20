import numpy as np
import pandas as pd
from scipy import signal,stats

from flask import Flask,request,jsonify
import json
import re
import os
import data_utils as utils
import sklearn.preprocessing as pre


configpath=os.path.join(os.path.dirname(__file__),'config.txt')
try:
    config = utils.py_configs(configpath)
    Signal_SERVER = config["Signal_SERVER"]
    Signal_PORT = config["Signal_PORT"]
except:
    raise Exception("Configuration error")

app = Flask(__name__)
@app.route('/Preprocessing/encoding_feature',methods=['POST'])
def encoding_feature():   ### 参数以json格式传送
    try:
        file_key=list(request.files.to_dict().keys())
        print('k: ',file_key)

        ## 'file' 是输入的信号数据文件; 'window'表示窗口,一般为`boxcar`, `triang`, `blackman`, `hamming`, `hann`等; 'index'是数据文件中需要进行小波分析的该组数据
        keys=['file']
        for key in keys:
            if (key not in file_key):
                code = 2
                output = {"code": code, "KeyError": str(key)}
                output = json.dumps(output)
                return output
        file=request.files.get('file')
        index=int(request.form['index'])
        df=pd.read_csv(file)
        data=df.values
        cols=df.columns
        onehot_dict={}

        for i in range(data.shape[1]):
            attr_set=set(data[:,i])
            temp_dict={}
            j=0
            for attr in attr_set:
                temp_dict[attr]=j
                j+=1
            onehot_dict[cols[i]]=temp_dict

        data_to_bi = []
        for i in range(data.shape[0]):
            rows=[]
            for j in range(data.shape[1]):
                onehot=onehot_dict[cols[j]][data[i][j]]
                rows.append(onehot)
            data_to_bi.append(rows)
        enc = pre.OneHotEncoder()
        print(onehot_dict)
        print(data_to_bi)
        enc.fit(data_to_bi)
        a=enc.transform(data_to_bi).toarray()
        result={'OneHot Result':str(a)}
        return jsonify(result)
    except Exception as e:
        print('Exception: ',e)
        code = 1
        result = {"code":code,"error":re.findall("'([\w\d _]+)'",str(type(e)))[0]}
        result = jsonify(result)
        return result

if __name__=="__main__":

    app.run(host=Signal_SERVER, port=int(Signal_PORT))