from sklearn import preprocessing
import numpy as np
import pandas as pd
from scipy import signal,stats
from flask import Flask,request,jsonify
import json
import re
import os
import codecs


def py_configs(configpath,conf=None, delete=None):
    if not os.path.exists(configpath):
        obj = {}
    else:
        with codecs.open(configpath, 'r', 'utf-8') as f:
            str1 = f.read()
            #            obj = obj.encode('utf8').decode('utf8')
            if not str1:
                obj = {}
            try:
                obj = json.loads(str1)
            except:
                #
                obj = {}
    if isinstance(delete, str):
        obj.pop(delete)
        with codecs.open(configpath, 'w', 'utf-8') as f:
            str1 = jsonify(obj)
            f.write(str1)
        return obj
    if isinstance(conf, dict):
        for key in conf:
            obj[key] = conf[key]
        with codecs.open(configpath, 'w', 'utf-8') as f:
            str1 = jsonify(obj)
            f.write(str1)
    elif isinstance(conf, str):
        if conf in obj:
            return obj[conf]
        else:
            return {}
    return obj

configpath=os.path.join(os.path.dirname(__file__),'config.txt')
try:
    config = py_configs(configpath)
    DataPreprecessing_SERVER = config["DataPreprecessing_SERVER"]
    DataPreprecessing_PORT = config["DataPreprecessing_PORT"]
except:
    raise Exception("Configuration error")



app = Flask(__name__)
@app.route('/Data_preprocessing/scaling_data',methods=['POST'])
def daqfft():
    try:
        form_key=list(request.form.to_dict().keys())
        file_key=list(request.files.to_dict().keys())
        print('k: ',form_key)

        keys=['file','operation']
        for key in keys:
            if key not in form_key or key not in file_key:
                code = 2
                output = {"code": code, "KeyError": str(key)}
                output = json.dumps(output)
                return output        

        operation = request.form['operation']
        file_get = request.files.get('file')
        X_train = pd.read_csv(file_get)
        
        result=''
# Operation 1.Standardization mean=0  std=1
# perform scale operation on a single array-like dataset:
        if operation == 'Standardization':
            X_scaled = preprocessing.scale(X_train)
            result= jsonify(X_scaled)
# Operation 2. Scaling features to a range--MinMaxScaler  (eg, range[0,1])
        elif operation == 'MinMaxScaler':
            min_max_scaler = preprocessing.MinMaxScaler()
            X_train_minmax = min_max_scaler.fit_transform(X_train)
            result= jsonify(X_train_minmax)
# Operation 3. Scaling features to a range--MaxAbsScaler range [-1, 1]
        else:
            max_abs_scaler = preprocessing.MaxAbsScaler()
            X_train_maxabs = max_abs_scaler.fit_transform(X_train)
            result= jsonify(X_train_maxabs)
            
        return result


    except Exception as e:
        print('Exception: ',e)
        code = 1
        result = {"code":code,"error":re.findall("'([\w\d _]+)'",str(type(e)))[0]}
        result = jsonify(result)
        return result


if __name__=="__main__":
    app.run(host= DataPreprecessing_SERVER, port=int(DataPreprecessing_PORT))


