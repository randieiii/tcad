import tornado.ioloop
import tornado.web
import tornado

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
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

dh = data_handler.StreamerSlave(
    f'postgresql://{DBUSER}:{DBPASS}@{DBHOST}:5432/{DB}'
)
words = [line.rstrip('\n') for line in open(SEARCHABLEW)]
plotly.io.orca.config.executable = ORCA
plotly.io.orca.config.save()



def draw_top(df_top, template_number, dir, title):
        template = f"template{template_number}.html"
        chart = px.bar(df_top, x=df_top.keys()[0],y=df_top.keys()[1], color=df_top.iloc[:, 0])
        chart.update_layout(showlegend=False)
        chart.update_traces( 
            marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5, opacity=0.6
        )
        chart.update_layout(title_text=title)
        chart.write_image(f"./vol/{dir}/chart{template_number}.png")
        plot(chart, filename=template, show_link=False)
        return template

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

class MainHandler(tornado.web.RequestHandler):
    def get(self, stream='pokelawls'):
        if not os.path.exists(f"./vol/{stream}"):
            os.mkdir(f"./vol/{stream}")
        rnumber = random.random()
        dh.query = f'select * from {stream} WHERE "timestamp" BETWEEN NOW() - INTERVAL \'10 HOURS\' AND NOW()'
        with open(f'./vol/{stream}/{stream}_report.txt', 'w+') as opened_file:
            for i in words:
                opened_file.write(f"Usage of word `{i}`:{str(dh.get_word_usage(i, 'msg'))}\n")
                opened_file.write(dh.get_words_examples(i, "msg", 10)[['username', 'msg']].to_csv(index=False))

        draw_top(dh.top_by_coulumn("username", 10), rnumber, stream, "Top10 humans in the chat")
        draw_top(dh.top_words_usage("msg", 10), rnumber + 1, stream, "Top10 words in the chat")
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

def make_app():
    return tornado.web.Application([
        (r"/([a-zA-Z\-0-9\.:,_]+)/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()