from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import requests

app = Flask(__name__)


@app.route('/')
def index():
    api_key = 'demo'
    symbol = 'IBM'  
    interval = '5min'  
    
    
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&outputsize=full&apikey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    #data into a Pandas DataFrame
    df = pd.DataFrame(data[f'Time Series ({interval})']).T
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df = df.astype(float).reset_index()
    
    
    df['index'] = pd.to_datetime(df['index'])
    df = df.sort_values('index')
    

    last_day = df['index'].dt.date.max()
    df = df[df['index'].dt.date == last_day]
    
    fig = px.line(df, x='index', y=['Open', 'Close'], title=f'Stock Prices for {symbol}')
    
    graph_html = fig.to_html(full_html=False)
    
    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
