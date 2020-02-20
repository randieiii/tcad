import tornado.ioloop
import tornado.web
import tornado

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
import os
import random

from data_handler import data_handler

DBPASS = os.environ['DBPASSWORD']
DBUSER = os.environ['DBUSER']
DB = os.environ['DB']
DBHOST = os.environ['DBHOST']
CHANNEL = os.environ['CHANNEL']

dh = data_handler.StreamerSlave(
    f'postgresql://{DBUSER}:{DBPASS}@{DBHOST}:5432/{DB}',
    f'select * from {CHANNEL} WHERE "timestamp" BETWEEN NOW() - INTERVAL \'10 MINUTES\' AND NOW()'
    )

def draw_top(df_top, template_number):
        template = f"template{template_number}.html"
        chart = px.bar(df_top, x=df_top.keys()[0],y=df_top.keys()[1], color=df_top.iloc[:, 0])
        chart.update_layout(showlegend=False)
        chart.update_traces( 
            marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5, opacity=0.6
        )
        chart.update_layout(title_text='Messages spammed for the last 10 minutes')
        plot(chart, filename=template, show_link=False)
        return template

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        rnumber = random.random()
        df = dh.top_by_coulumn("username", 10)
        self.render(draw_top(df, rnumber), title="My title")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()