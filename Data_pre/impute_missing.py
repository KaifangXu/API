import numpy as np
import pandas as pd

from flask import Flask,request,jsonify
import json
import re
import os
import data_utils as utils
from sklearn.preprocessing import Imputer


configpath=os.path.join(os.path.dirname(__file__),'config.txt')
try:
    config = utils.py_configs(configpath)
    Signal_SERVER = config["Signal_SERVER"]
    Signal_PORT = config["Signal_PORT"]
except:
    raise Exception("Configuration error")

app = Flask(__name__)
@app.route('/Preprocessing/impute_missing',methods=['POST'])
def impute_missing():   ### 参数以json格式传送
    try:
        file_key=list(request.files.to_dict().keys())
        form_key = list(request.form.to_dict().keys())
        print('k: ',file_key,form_key)

        keys=['file','strategy','axis']
        strategies=['','mean','median','most_frequent']
        axises=['',0,1]
        for key in keys:
            if (key not in file_key)and (key not in form_key):
                code = 2
                output = {"code": code, "KeyError": str(key)}
                output = json.dumps(output)
                return output
        file=request.files.get('file')
        strategy=request.form['strategy']
        axis=request.form['axis']
        if strategy not in strategies:
            raise Exception('Strategy must be \'mean\',\'median\'or \'most_frequent\'')
        else:
            if strategy=='':
                strategy='mean'
        if axis not in axises:
            raise Exception('axis must be \'0\'or \1\'')
        else:
            if axis=='':
                axis=0
            else:
                axis=int(axis)

        df=pd.read_csv(file)
        data=df.values
        print(data)
        imp = Imputer(missing_values='NaN', strategy=strategy, axis=axis)
        imp.fit(data)
        new_data = imp.transform(data)
        print(new_data)
        result={'Imputation Result':new_data.tolist()}
        return jsonify(result)
    except Exception as e:
        print('Exception: ',e)
        code = 1
        result = {"code":code,"error":re.findall("'([\w\d _]+)'",str(type(e)))[0]}
        result = jsonify(result)
        return result

if __name__=="__main__":

    app.run(host=Signal_SERVER, port=int(Signal_PORT))
