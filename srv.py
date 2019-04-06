#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sqlite3
from flask import Flask
import json
app=Flask(__name__)

@app.route("/")
def index():
    conn=sqlite3.connect('books.db')
    c=conn.cursor()
    c.execute("select * from books order by url limit 200")
    data=json.dumps(c.fetchall())
    c.close()
    conn.close()
    return data

def main():
    app.run(debug=True,host='0.0.0.0')
if __name__=='__main__':main()
