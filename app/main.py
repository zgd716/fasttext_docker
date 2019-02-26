#!/usr/bin/env python
# encoding: utf-8
'''
@author: jellyzhang
@contact: zhangguodong_12@126.com
@time: 2019/2/26 10:11
@desc:
'''
import decimal
import flask.json
from flask import Flask,request,jsonify
import logging
import tensorflow as tf
import pickle
import datetime
from predict import *
from config import config
import numpy as np

#解决jsonfy  不能传decimal类型
class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


#日志
handler = logging.FileHandler('./logs/logs.txt', encoding='UTF-8')
handler.setLevel(logging.DEBUG)
logging_format = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
handler.setFormatter(logging_format)


#初始化操作
app=Flask(__name__)
app.json_encoder = MyJSONEncoder
app.logger.addHandler(handler)
model_api =Predict(config)


@app.route('/api/classification',methods=['POST'])
def classification():
    '''
    分类
    :return:
    '''
    try:
        start_time=datetime.datetime.now()
        if request.mimetype=='application/json':  #json
            forms = request.json
        elif request.mimetype=='multipart/form-data' or request.mimetype=='application/x-www-form-urlencoded': #form
            forms = request.form
        else:
            app.logger.warn('mimetype:{}'.format(request.mimetype))
        text=forms['text']  #获取需要提取的文本
        _predictions= model_api.predict(text)
        result={}
        result['msg']=True
        result['text']=text
        result['prediction']=_predictions
        return jsonify(result)
    except Exception as ex:
        app.logger.error(ex)
        return jsonify({'msg':False})




if __name__=='__main__':
    app.run(host='0.0.0.0', debug=False, port=80)
