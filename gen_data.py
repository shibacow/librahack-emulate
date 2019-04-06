#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import csv
from collections import Counter
import re
import sqlite3
from contextlib import closing
dbname = 'books.db'
def read_data():
    with open('dataset_201901_t_internet.tsv') as rf:
        reader = csv.DictReader(rf, delimiter="\t")
        for row in reader:
            dkt=dict(row)
            yield dkt
def db_insert():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        create_table = 'create table books (url varchar(64), title varchar(512),ISBN varchar(32))'
        c.execute(create_table)
        yield c,conn
def main():
    for c,conn in db_insert():
        ins=[]
        insert_sql='insert into books (url,title,ISBN) values (?,?,?)'
        for dkt in read_data():
            ins.append((dkt['URL'],dkt[u'タイトル'],dkt['ISBN']))
        c.executemany(insert_sql,ins)
        conn.commit()
        
if __name__=='__main__':main()
