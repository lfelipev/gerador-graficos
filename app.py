from sqlalchemy import create_engine
import mysql.connector
import pandas as pd
from dash import Dash
import dash_html_components as html
from plotlyflask_tutorial import init_app


mysql_conn_str = "mysql+pymysql://root:password@mysql_db:3306/graficos_teste"
engine = create_engine(mysql_conn_str)
connection = engine.connect()
q = connection.execute('SHOW DATABASES')
available_tables = q.fetchall()
print(available_tables)

def createTable():
    wafermaps_db = mysql.connector.connect(
        host='mysql_db',
        user='user',
        password='password',
        database='graficos_teste'
    )

    cursor = wafermaps_db.cursor()

    # Syntax: column_name data_type(length) [NOT NULL] [DEFAULT value] [AUTO_INCREMENT] column_constraint;

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS grafico_padrao 
                        (ID INT AUTO_INCREMENT PRIMARY KEY,
                        DADO_1 INTEGER(64), 
                        DADO_2 INTEGER(64))
                        """)

    cursor.execute("SHOW TABLES")

    for x in cursor:
        print(x)

def listTables():
    wafermaps_db = mysql.connector.connect(
        host='mysql_db',
        user='user',
        password='password',
        database='graficos_teste'
    )

    cursor = wafermaps_db.cursor()

    cursor.execute("SHOW TABLES")

    for x in cursor:
        print(x)

def insertInTables():
    wafermaps_db = mysql.connector.connect(
            host='mysql_db',
            user='user',
            password='password',
            database='graficos_teste'
        )
    
    cursor = wafermaps_db.cursor()

    # Tabela DIM
    DADO_1 = [1, 2, 3, 4, 5, 6, 7]
    DADO_2 = [11, 12, 13, 14, 15, 16, 17]
    data_dim = {'DADO_1': DADO_1,
                'DADO_2': DADO_2}

    df_dim = pd.DataFrame(data_dim)

    print('\nDados - Tabela Dim')
    print(df_dim.head())

    for i in range(0, len(DADO_1)-1):
        query_fato = f"""INSERT INTO grafico_padrao
                                (DADO_1,
                                DADO_2)

                                VALUES
                                ('{DADO_1[i]}',
                                '{DADO_2[i]}')"""

        cursor.execute(query_fato)
                            
    wafermaps_db.commit()

    print(cursor.rowcount, "Dados inseridos no banco.")

def selectTable():
    wafermaps_db = mysql.connector.connect(
        host='mysql_db',
        user='user',
        password='password',
        database='graficos_teste'
    )

    cursor = wafermaps_db.cursor()

    cursor.execute("select * from grafico_padrao")

    for x in cursor:
        print(x)

if __name__ == '__main__':
    app.run_Server(debug=True)
#listTables()
#insertInTables()
#selectTable()

# docker-compose exec python_app bash
# compose_flask/app.py
# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "hello world!"

# if __name__ == "__main__":
#     app.run(host="0.0.0.0")