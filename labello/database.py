import os
from datetime import datetime, timedelta

import peewee as pw

db = pw.SqliteDatabase(os.environ.get("DB_PATH", "labello.db"))


class Label(pw.Model):
    name = pw.CharField()
    id = pw.PrimaryKeyField()
    raw = pw.CharField(null=True)
    last_edit = pw.DateTimeField()

    class Meta:
        database = db


example = """
N
q812
S2
A50,0,0,1,1,1,N,"Example 1 0123456789"
A50,50,0,2,1,1,N,"Example 2 0123456789"
A50,100,0,3,1,1,N,"Example 3 0123456789"
A50,150,0,4,1,1,N,"Example 4 0123456789"
A50,200,0,5,1,1,N,"EXAMPLE 5 0123456789"
A50,300,0,3,2,2,R,"Example 6 0123456789"
LO25,600,750,20
B50,800,0,3,3,7,200,B,"998152-001"
P1

"""
