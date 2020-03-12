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

ORCA = '/usr/bin/orca'
SEARCHABLEW = "./searchablew"

words = [line.rstrip('\n') for line in open(SEARCHABLEW)]
plotly.io.orca.config.executable = ORCA
plotly.io.orca.config.save()


def draw_top(df_top, template_number, dir, title, col):
        chart = px.bar(df_top, x=df_top.keys()[0],y=df_top.keys()[1], color=df_top.iloc[:, col])
        chart.update_layout(showlegend=False)
        chart.update_traces( 
            marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5, opacity=0.6
        )
        chart.update_layout(title_text=title)
        chart.write_image(f"./vol/{dir}/chart{template_number}.png")

    
def draw_chart_by_time(df, title, dir):
    data = []
    for key, item in df.groupby(df.keys()[1]):
        if item['started_at'].count() > 1:
            data.append(go.Scatter(
                x=item['started_at'],
                y=item['count'],   
                name=key,     
                marker={'size':5},
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
        top_tab = data_handler.TopTable(stream)

        for k, v in top_tab.read_tops().items():
            draw_chart_by_time(v, k, stream)

        zipf = zipfile.ZipFile(f'./vol/{stream}.zip', 'Words', zipfile.ZIP_DEFLATED)
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

        worker = data_handler.Worker(stream)

        for j in worker.get_subset().values: 
            print(j[0])
            data_frame = worker._get_data_frame(j[0])

            top_words = data_frame.top_words_usage('msg', 10)
            worker._set_top_attr('Words', top_words)
            top_users = worker.stream_t.top_users_sql()[:10]
            worker._set_top_attr('Users', top_users)
            
            worker.top_t.write_df_to_sql({'started_at': j[0]})

        # forming a shitty report
            with open(f'./vol/{stream}/{stream}_report.txt', 'a+') as opened_file:
                
                # writing tu and tw to report file
                opened_file.write(top_users.to_string())
                opened_file.write(top_words.to_string())
                
                # for every word in SEARCHABLEW  (that is global btw ) finding usage and examples 
                for i in words:
                    opened_file.write(f"\n\nUsage of word `{i}`:{str(data_frame.get_word_usage(i, 'msg'))}\n")
                    opened_file.write(data_frame.get_words_examples(i, "msg", 9)[['username', 'msg']].to_csv(index=False))


            # draw top graphs 
            draw_top(top_users, j[0] + "u", stream, "Top10 humans in the chat", 0)
            draw_top(top_words, j[0] + "w", stream, "Top10 words in the chat", 1)
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


"""
What we need to do: 
    1. Find what streams are missing and calculate for them 
    2. Do I want to calculate total every time? (Dont think so)
    3. Create diff requests 
        1. Update data and fullfill gaps in top (for ex)
        2. Get report where I actually want to get total
    4. Format report better()

For refresh:
    1. Get substrickt between top and chat log
    2. Find tw/tu and write it.
    3. Generate images for /\
    4. Get examples for words and write to the report


"""