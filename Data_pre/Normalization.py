# -*- coding: utf-8 -*-
"""
Normalization
Normalization is the process of scaling individual samples to have unit norm. 
This process can be useful if you plan to use a quadratic form such as the 
dot-product or any other kernel to quantify the similarity of any pair of 
samples.
"""
from sklearn.model_selection import train_test_split
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
# Operation Normalization
# perform scale operation on a single array-like dataset:
        if operation == 'Normalization':
            X_normalized = preprocessing.normalize(X_train, norm='l2')
            result= jsonify(X_normalized)
        return result


    except Exception as e:
        print('Exception: ',e)
        code = 1
        result = {"code":code,"error":re.findall("'([\w\d _]+)'",str(type(e)))[0]}
        result = jsonify(result)
        return result


if __name__=="__main__":
    app.run(host= DataPreprecessing_SERVER, port=int(DataPreprecessing_PORT))



