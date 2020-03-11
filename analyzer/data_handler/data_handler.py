import pandas
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
import re 
from collections import defaultdict
from datetime import datetime

class StreamerSlave:
    def __init__(self, dburl, query=None):
        self.engine = create_engine(dburl)
        self.query = query
        self.frame = None
        self.column_str = {}

    @property
    def data_frame(self):
        if self.frame is None:
            self.frame =  pandas.read_sql_query(self.query, con=self.engine)
        return self.frame

    def get_df_str(self, column):
        if not self.column_str:
            self.column_str[column] = self.data_frame[column].str
        return self.column_str[column]

    def top_users_sql(self):
        return self.read_sql_to_df('select username, COUNT(*) AS "count" from sodapoppin group by username ORDER BY COUNT DESC;')

    def amount_of_streams(self)
        return self.read_sql_to_df('select DISTINCT started_at from sodapoppin;')

    def top_by_coulumn(self, column, top):
        return self.data_frame[column].value_counts().rename_axis(column.capitalize()).reset_index(name='Count')[:top]

    def top_words_usage(self, column, top):
        result = defaultdict(int)
        for i in self.data_frame[column].to_dict().values():
            for word in re.findall(r"[a-zA-Z\-0-9\.:,_'\"]+", i):
                    result[word] += 1
        return pandas.DataFrame.from_dict(result, orient='index').sort_values(0, ascending=False)[:top].reset_index().rename(columns={0: 'Count', 'index':"Word"})
        # return .split(expand=True).stack().value_counts().rename_axis(column.capitalize()).reset_index(name='Count')[:top]

    def get_word_usage(self, word, column):
        return len(self.get_df_str(column).lower().str.findall(r"[\b|^]*({})\b".format(word), flags = re.I).sum())

    def get_words_examples(self, word, column, char_limit=10):
        mask = (self.get_df_str(column).len() >= char_limit )
        return self.data_frame[self.get_df_str(column).contains(r"[\b|^]*({})\b".format(word), flags = re.I)].loc[mask]

    def write_df_to_sql(self, df, table_name, additional_value=None):
        if additional_value:
            (k,v), = additional_value.items()
            df[k] = datetime.strptime(v, '%Y-%m-%dT%XZ').date().isoformat()
        df.to_sql(table_name, self.engine,  if_exists="append")

    def read_sql_to_df(self, query):
        return pandas.read_sql_query(query, con=self.engine)
