#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sqlite3
from flask import Flask,request
import json
app=Flask(__name__)

@app.route("/")
def index():
    conn=sqlite3.connect('books.db')
    c=conn.cursor()
    cnt=request.args.get('count')
    cnt=int(cnt)
    app.logger.info("cnt={}".format(cnt))
    c.execute("select * from books where count=? order by url limit 200",(str(cnt),))
    data=json.dumps(c.fetchall())
    #リリース開放処理
    c.close() #MDISはこのいずれかの処理を怠る
    conn.close() #MDISはこのいずれかの処理を怠る
    return data

def main():
    app.run(debug=True,host='0.0.0.0')
if __name__=='__main__':main()
