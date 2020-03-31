# memastikan database bisa dipindah menjadi dataframe pandas
from sqlalchemy import create_engine
import pymysql 
import pandas as pd

sqlEngine = create_engine('mysql+pymysql://root:mysql123@127.0.0.1', pool_recycle = 3306)
dbConnection = sqlEngine.connect()

dfTips = pd.read_sql('SELECT * FROM flaskapp.tips', dbConnection)

print(dfTips)