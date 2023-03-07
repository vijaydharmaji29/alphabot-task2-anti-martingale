import plotly.graph_objects as go

import pandas as pd
from datetime import datetime

df = pd.read_csv('data_reduced/TCS.csv')
df = df[:349]

fig = go.Figure(data=[go.Candlestick(x=df['datetime'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

fig.show()