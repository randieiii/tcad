import pandas
import re 
from collections import defaultdict
from datetime import datetime

from dbbase import Engine

def read_sql_to_df(query):
    return pandas.read_sql_query(query, con=Engine)

class ChannelTable:
    def __init__(self, stream, time=None):
        self.stream = stream
    
    @property
    def table_name(self):
        return 

    def streams_count(self):
        return read_sql_to_df(f'select DISTINCT started_at from {self.table_name};')


class StreamTable(ChannelTable):
    def __init__(self, stream, time=None):
        self.time = time
        super(StreamTable, self).__init__(stream)
    
    @property
    def condition(self):  
        return f"WHERE started_at = '{self.time}'" if self.time else ''

    @property
    def table_name(self):
        return self.stream

    def top_users_sql(self):
        query = f'SELECT username, COUNT(*) AS "count" from {self.table_name} {self.condition} group by username ORDER BY COUNT DESC;'
        print(query)
        return read_sql_to_df(query)
    
    def get_data_frame(self):
        query = f"SELECT * FROM {self.table_name} {self.condition}"
        return read_sql_to_df(query)
    
    def top_words(self, sort=False):
        sort = 'ORDER BY nentry DESC' if sort else ''
        query = f'SELECT word, nentry as "count" FROM ts_stat($$ \
                                SELECT to_tsvector({self.table_name}.msg) \
                                FROM {self.table_name} {self.condition}\
                                $$) {sort};'
        return read_sql_to_df(query)


    
class PandasHandler:
    def __init__(self, data_frame):
        self.data_frame = data_frame

    def top_by_coulumn(self, column, top):
        return self.data_frame[column].value_counts().rename_axis(column).reset_index(name='count')[:top]

    def top_words_usage(self, column, top):
        result = defaultdict(int)
        for i in self.data_frame[column].to_dict().values():
            for word in re.findall(r"[a-zA-Z\-0-9\.:,_'\"]+", i):
                    result[word] += 1
        return pandas.DataFrame.from_dict(result, orient='index').sort_values(0, ascending=False)[:top].reset_index().rename(columns={0: 'Count', 'index':"Word"})
        # return .split(expand=True).stack().value_counts().rename_axis(column.capitalize()).reset_index(name='Count')[:top]

    def get_word_usage(self, word, column):
        return len(self.data_frame[column].str.lower().str.findall(r"[\b|^]*({})\b".format(word), flags = re.I).sum())

    def get_words_examples(self, word, column, char_limit=10):
        mask = (self.data_frame[column].str.len() >= char_limit )
        return self.data_frame[self.data_frame[column].str.contains(r"[\b|^]*({})\b".format(word), flags = re.I)].loc[mask]
        


class TopTable(ChannelTable):
    top_kind = {
            'w': 'word_usage',
            'u': 'user_usage'
        }
    def __init__(self, stream, top_kind, top_df=None):
        self.top_df = top_df
        self.tkind = top_kind
        super(TopTable, self).__init__(stream)

    @property
    def table_name(self):
        return self.stream + self.top_kind[self.tkind]

    def write_df_to_sql(self, additional_value=None):
        if additional_value:
            (k,v), = additional_value.items()
            self.top_df[k] = v #datetime.strptime(v, '%Y-%m-%dT%XZ').date().isoformat()
        self.top_df.to_sql(self.table_name, Engine,  if_exists="append")