from flask import Flask, render_template, request, redirect, session
import requests
import pandas as pd
from bokeh.plotting import figure, show
from datetime import datetime
from bokeh.embed import components
from jinja2 import Template



app = Flask(__name__)
#app.vars={}


page = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  <link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-2.0.2.min.css" type="text/css" />
  <script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-2.0.2.min.js"></script>
</head>
<body>
<p>The daily {{ dat }} price for {{ sym }} : </p>
  <div id="myplot"></div>
  <script>
  fetch('/test')
    .then(function(response) { return response.json(); })
    .then(function(item) { return Bokeh.embed.embed_item(item); })
  </script>
  
</body>
""")

@app.route('/',methods=['GET','POST'])
def index():
   if request.method == 'GET':
       return render_template('ticker.html',ans1='Open',ans2='Close',ans3='High',ans4='Low')
   else:
        #request was a POST
        #app_lulu.vars['name'] = request.form['name_lulu']
        symb = request.form['ticker_lulu']
        typp = request.form['answer_from_layout_lulu']
        mon = request.form['month_lulu']
        
        #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=PVR1OFAF4I0GTWX7'
        path = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'
        API_key = 'PVR1OFAF4I0GTWX7'
        symbol = str(symb)
        url = path+'&symbol='+f'{symbol}'+'&apikey='+API_key
        r = requests.get(url)
        data = r.json()
        data_df = pd.DataFrame.from_dict(data)
        data_df = data_df.drop(['Meta Data'],axis=1)
        data_df = data_df.dropna()
        data_df = data_df['Time Series (Daily)'].apply(pd.Series)
        dates = data_df.index
        data_df['dates']=dates
        dt = []
        for i in range(len(data_df)):
            dt.append(datetime.strptime(data_df['dates'].iloc[i],'%Y-%m-%d'))
        data_df['dates'] = dt
        
        
        typ = str(typp)
        if typ == 'Open':
            p = figure(x_axis_type='datetime',x_axis_label="Date", y_axis_label="Closing value")
            p.line(x='dates', y='1. open', line_width=2, source=data_df)
        elif typ == 'Close':
            p = figure(x_axis_type='datetime',x_axis_label="Date", y_axis_label="Closing value")
            p.line(x='dates', y='4. close', line_width=2, source=data_df)
        elif typ == 'High':
            p = figure(x_axis_type='datetime',x_axis_label="Date", y_axis_label="Closing value")
            p.line(x='dates', y='2. high', line_width=2, source=data_df)
        else:
            p = figure(x_axis_type='datetime',x_axis_label="Date", y_axis_label="Closing value")
            p.line(x='dates', y='3. low', line_width=2, source=data_df)
        
        # p = figure(title="Simple line example", x_axis_label="x", y_axis_label="y")
        # p.line(x=[0,1,2,3],y=[0,1,2,3])
        # script, div = components(p)
        # return render_template('plots.html', script=script, div=div)
        
        #show(p)
        script, div = components(p)
        return render_template('plots.html', symb = symb, typ= typ, script=script, div=div)
        

# @app.route('/display',methods=['POST'])
# def data_import():
#     #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=PVR1OFAF4I0GTWX7'
#     path = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'
#     API_key = 'PVR1OFAF4I0GTWX7'
#     #symbol=session['symbol']
#     sym = request.args.get['ticker_lulu']
#     symbol = str(sym)
#     url = path+'&symbol='+symbol+'&apikey='+API_key
#     r = requests.get(url)
#     data = r.json()
#     data_df = pd.DataFrame.from_dict(data)
#     data_df = data_df.drop(['Meta Data'],axis=1)
#     data_df = data_df.dropna()
#     data_df = data_df['Time Series (Daily)'].apply(pd.Series)
#     dates = data_df.index
#     data_df['dates']=dates
#     dt = []
#     for i in range(len(data_df)):
#         dt.append(datetime.strptime(data_df['dates'].iloc[i],'%Y-%m-%d'))
#     data_df['dates'] = dt
    
#     #p = figure(x_axis_type='datetime',x_axis_label="Date", y_axis_label="Closing value")
#     #p.line(x='dates', y='4. close', line_width=2, source=data_df)
#     #show(p)
#     p = figure(title="Simple line example", x_axis_label="x", y_axis_label="y")
#     p.line(x=[0,1,2,3],y=[0,1,2,3])
#     script, div = components(p)
#     return render_template('plots.html', script=script, div=div)
#     #show(p)
   


if __name__ == '__main__':
  app.run(port=33507)
