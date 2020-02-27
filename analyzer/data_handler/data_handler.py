import pandas
import sqlalchemy
import re 

class StreamerSlave:
    def __init__(self, dburl, query=None):
        self.engine = sqlalchemy.create_engine(dburl)
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

    def top_by_coulumn(self, column, top):
        return self.data_frame[column].value_counts().rename_axis(column.capitalize()).reset_index(name='Count')[:top]

    def top_words_usage(self, column, top):
        return self.get_df_str(column).split(expand=True).stack().value_counts()[:top]

    def get_word_usage(self, word, column):
        return len(self.get_df_str(column).lower().str.findall(r"[\b|^]*({})\b".format(word), flags = re.I).sum())

    def get_words_examples(self, word, column, char_limit=10):
        mask = (self.get_df_str(column).len() >= char_limit )
        return self.data_frame[self.get_df_str(column).contains(r"[\b|^]*({})\b".format(word), flags = re.I)].loc[mask]


        



    

    
