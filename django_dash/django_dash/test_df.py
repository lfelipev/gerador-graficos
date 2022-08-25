import pandas as pd
import plotly.express as px

df = pd.read_csv('dimensao_est.csv', sep=';') 
print(df.iloc[[2]])

df = df.iloc[[2]]
df2 = pd.melt(df, value_vars=['E_ESCV', 'E_PROFV', 'E_FAMV', 'E_COMV', 'E_ESTV'], var_name='dim', value_name='medias')

print(df2.head())

fig = px.line_polar(df2, r='medias', theta='dim', line_close=True, markers=True, line_shape='linear', range_r=[1,7])
fig.show()