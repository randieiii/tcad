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

dh = data_handler.StreamerSlave(
    f'postgresql://{DBUSER}:{DBPASS}@{DBHOST}:5432/{DB}'
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
    def get(self, stream='pokelawls'):
    
        rnumber = random.random()
        dh.query = f'select * from {stream} WHERE "timestamp" BETWEEN NOW() - INTERVAL \'10 HOURS\' AND NOW()'
        

        with open('./vol/sime_file.txt', 'w') as opened_file:
            opened_file.write(dh.top_words_usage("msg", 10).to_string())
            opened_file.write("\n\n\n")
            opened_file.write(f"5heda = {str(dh.get_word_usage('5head', 'msg'))}")
            opened_file.write("\n\n\n")
            opened_file.write(dh.get_words_examples("cock", "msg", 10).to_string())
        df = dh.top_by_coulumn("username", 10)
        self.render(draw_top(df, rnumber), title="My title")

def make_app():
    return tornado.web.Application([
        (r"/([a-zA-Z\-0-9\.:,_]+)/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()