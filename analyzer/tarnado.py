import tornado.ioloop
import tornado.web
import tornado

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
import plotly.graph_objects as go
import plotly
import os
import random
import zipfile

from data_handler import data_handler

DBPASS = os.environ['DBPASSWORD']
DBUSER = os.environ['DBUSER']
DB = os.environ['DB']
DBHOST = os.environ['DBHOST']
ORCA = '/usr/bin/orca'
SEARCHABLEW = "./searchablew"

words = [line.rstrip('\n') for line in open(SEARCHABLEW)]
plotly.io.orca.config.executable = ORCA
plotly.io.orca.config.save()


def draw_top(df_top, template_number, dir, title, col):
        template = f"template{template_number}.html"
        chart = px.bar(df_top, x=df_top.keys()[0],y=df_top.keys()[1], color=df_top.iloc[:, col])
        chart.update_layout(showlegend=False)
        chart.update_traces( 
            marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5, opacity=0.6
        )
        chart.update_layout(title_text=title)
        chart.write_image(f"./vol/{dir}/chart{template_number}.png")
        plot(chart, filename=template, show_link=False)
        return template
    
def draw_chart_by_time(df, title, dir):
    data = []
    for key, item in df.groupby(df.keys()[1]):
        if item['started_at'].count() > 1:
            data.append(go.Scatter(
                x=item['started_at'],
                y=item['Count'],   
                name=key,     
                marker={'size':15},
                marker_line_width=1
            ))
    layout = {'title': title}
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(legend_orientation="h")
    fig.write_image(f"./vol/{dir}/chart{title}.png")

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

class MainHandler(tornado.web.RequestHandler):
    def get(self, stream='pokelawls'):
        dh = data_handler.StreamerSlave(
            f'postgresql://{DBUSER}:{DBPASS}@{DBHOST}:5432/{DB}',
            f'select * from {stream} WHERE "timestamp" BETWEEN NOW() - INTERVAL \'21 HOURS\' AND NOW()'
        )
        word_by_time = dh.read_sql_to_df(f'select * from {stream}top_words_usage;') 
        users_by_time = dh.read_sql_to_df(f'select * from {stream}top_by_coulumn;')

        draw_chart_by_time(word_by_time, 'top_words_usag', stream)
        draw_chart_by_time(users_by_time, 'top_by_coulumn', stream)

        zipf = zipfile.ZipFile(f'./vol/{stream}.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir(f'./vol/{stream}/', zipf)
        zipf.close()

        self.set_header('Content-Type', 'application/force-download')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % stream) 

        with open(f"./vol/{stream}.zip", "rb") as f:
            while True:
                _buffer = f.read(4096)
                if _buffer:
                    self.write(_buffer)
                else:
                    f.close()
                    self.finish()
                    return

class NotMainHandler(tornado.web.RequestHandler):   
    def get(self, stream='pokelawls', request='refresh_db_data'):  
        if not os.path.exists(f"./vol/{stream}"):
            os.mkdir(f"./vol/{stream}")
        rnumber = random.random()
        dh = data_handler.StreamerSlave(
            f'postgresql://{DBUSER}:{DBPASS}@{DBHOST}:5432/{DB}',
            f'select * from {stream} WHERE "timestamp" BETWEEN NOW() - INTERVAL \'21 HOURS\' AND NOW()'
        )
        top_users = dh.top_by_coulumn("username", 10)
        dh.write_df_to_sql(top_users, f"{stream}{dh.top_by_coulumn.__name__}", {"started_at": dh.data_frame["started_at"][0]})
        top_words = dh.top_words_usage("msg", 10)
        dh.write_df_to_sql(top_words, f"{stream}{dh.top_words_usage.__name__}", {"started_at": dh.data_frame["started_at"][0]})
        with open(f'./vol/{stream}/{stream}_report.txt', 'w+') as opened_file:
            opened_file.write(top_users.to_string())
            opened_file.write(top_words.to_string())
            for i in words:
                opened_file.write(f"\n\nUsage of word `{i}`:{str(dh.get_word_usage(i, 'msg'))}\n")
                opened_file.write(dh.get_words_examples(i, "msg", 9)[['username', 'msg']].to_csv(index=False))

        draw_top(top_users, rnumber, stream, "Top10 humans in the chat", 0)
        draw_top(top_words, rnumber + 1, stream, "Top10 words in the chat", 1)
        self.write("Completed")

def make_app():
    return tornado.web.Application([
        (r"/([a-zA-Z\-0-9\.:,_]+)/", MainHandler),
        (r"/([a-zA-Z\-0-9\.:,_]+)/([a-zA-Z\-0-9\.:,_]+)/", NotMainHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()