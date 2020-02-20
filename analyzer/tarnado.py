import tornado.ioloop
import tornado.web
import tornado
import pandas
import sqlalchemy
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly
import plotly.graph_objs as go
import plotly.express as px
import os
import random

DBPASS = os.environ['DBPASSWORD']
DBUSER = os.environ['DBUSER']
DB = os.environ['DB']
DBHOST = os.environ['DBHOST']
CHANNEL = os.environ['CHANNEL']

ngine = sqlalchemy.create_engine(f'postgresql://{DBUSER}:{DBPASS}@{DBHOST}:5432/{DB}')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        time = random.random()
        df = pandas.read_sql_query(f'select * from {CHANNEL} WHERE "timestamp" BETWEEN NOW() - INTERVAL \'10 MINUTES\' AND NOW()',con=ngine)
        print(df['username'])
        frame = {
            "Username": df['username'].value_counts().keys()[:10],
            "Count": df['username'].value_counts().values[:10]
        }
        result = pandas.DataFrame(frame) 
        data = px.data.gapminder()
        fig = px.bar(result, x='Username',y='Count', color=df['username'].value_counts().keys()[:10]).update_layout(showlegend=False)
        fig.update_traces( marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
        fig.update_layout(title_text='Messages spammed for the last 10 minutes')
        plotly.offline.plot(fig, filename=f'template{time}.html', show_link=False)
        self.render(f'template{time}.html', title="My title")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()