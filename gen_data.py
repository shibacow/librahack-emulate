#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import csv
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
        sqls=(
            'create table books (url varchar(64), title varchar(512),ISBN varchar(32),count int);',
            'create index urlindex on books(url);',
            'create index count_index on books(count);',
            'create index count_url_index on books(count,url);'
            )
        for sql in sqls:
            c.execute(sql)
        yield c,conn
        c.close()
        conn.close()
def main():
    for c,conn in db_insert():
        ins=[]
        insert_sql='insert into books (url,title,ISBN,count) values (?,?,?,?)'
        for cnt in range(30): #35万件なので30倍して、１千万件程度にする
            for dkt in read_data():
                ins.append((dkt['URL'],dkt[u'タイトル'],dkt['ISBN'],cnt))
            c.executemany(insert_sql,ins)
            print(cnt,len(ins))
            conn.commit()
            ins=[]
        
if __name__=='__main__':main()
