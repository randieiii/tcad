import pandas
import sqlalchemy
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px


class StreamerSlave:
    def __init__(self, dburl, query):
        self.engine = sqlalchemy.create_engine(dburl)
        self.query = query
    
    @property
    def data_frame(self):
        return pandas.read_sql_query(self.query, con=self.engine)

    def top_by_coulumn(self, column, top):
        return self.data_frame[column].value_counts().rename_axis(column.capitalize()).reset_index(name='Count')[:10]
