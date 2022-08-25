import mysql.connector
import pandas as pd

wafermaps_db = mysql.connector.connect(
            host='34.95.242.184',
            user='postgres',
            password='ScRTnRI0pA,LV`bO',
            database='postgres',
            use_pure=True
        )

# Tabela DIM
# data_dim = {'dado_1': [1, 2, 3, 4, 5, 6, 7],
#             'dado_2': [11, 12, 13, 14, 15, 16, 17]}

# df_dim = pd.DataFrame(data_dim)

# print('\nDados - Tabela Dim')
# print(df_dim.head())
