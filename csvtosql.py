import mysql.connector
import os

DB_NAME=''
for i in os.listdir():
	if i.endswith('.csv'):
		DB_NAME=i.replace('.csv','')
		break

conn = mysql.connector.connect(user='root', password='toor')

crsr = conn.cursor()

def cmdexec(lst):
	for i in lst:
		crsr.execute(i.replace('\n',''))
		conn.commit()

def listasstr(lst):
	temp=''
	for i in lst.split(','):
		temp+=(f"'{i}'")
		if i!=lst.split(',')[-1]:
			temp+=', '
	return temp.replace('\n','')

with open(f'{DB_NAME}.csv') as f:
	DB_HDGS=f.readlines()[0]

dbcreate=f'CREATE TABLE {DB_NAME}TABLE ('

creationappend=DB_HDGS.split(',')
try:
	creationappend=creationappend.remove(' ')
except:
	pass
try:
	creationappend=creationappend.remove(' ')
except:
	pass

for hdg in creationappend:
	for j in hdg:
		dbcreate+=j
	dbcreate+=' VARCHAR(20)'
	if hdg!=creationappend[-1]:
		dbcreate+=', '
dbcreate+=');'

try:
	cmdexec([f'CREATE DATABASE {DB_NAME};'])
except:
	cmdexec([f'DROP DATABASE {DB_NAME};',f'CREATE DATABASE {DB_NAME};'])


tablecreator=[f'USE {DB_NAME};',dbcreate]

commands=[]

with open(f'{DB_NAME}.csv') as f:
	first=True
	for rec in f.readlines():
		if first==False:
			commands.append(f"INSERT INTO {DB_NAME}TABLE ( {(DB_HDGS)} ) VALUES ( {listasstr(rec)} );")
		first=False

cmdexec(tablecreator)

cmdexec(commands)

crsr.execute(f"SELECT * FROM {DB_NAME}table")
for i in crsr:
	print(i)

conn.close()