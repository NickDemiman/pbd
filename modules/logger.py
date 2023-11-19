import os
from datetime import datetime
from pytablewriter import MarkdownTableWriter
from pandas import DataFrame

class Logger:
    
    def __init__(self, folder='./logs') -> None:
        if not os.path.exists(folder):
            os.mkdir(folder)
        if not os.path.exists(folder + '/diagrams'):
            os.mkdir(folder + '/diagrams')
        
        self.key = int(datetime.now().timestamp()).__str__()
        self.folder = folder
        self.diagrams = 'diagrams/' + self.key
        
        if not os.path.exists(folder + '/' + self.diagrams):
            os.mkdir(folder + '/' + self.diagrams)
        
        self.filepath = folder + '/log_' + self.key +'.md'
        open(self.filepath, "w", encoding='UTF-8').close()
    
    def write(self, message : str) -> None:
        f = open(self.filepath, 'a', encoding='UTF-8')
        f.write('\n' + message+'\n')
        f.close()
        
    def write_image(self, name, filename, format = 'png'):
        f = open(self.filepath, 'a', encoding='UTF-8')
        f.write('\n![{}]({})\n'.format(name, self.diagrams+'/'+filename + '.' + format))
        f.close()
        
    def get_path_for_image(self, name, format):
        return self.diagrams+'/'+ name + format
    
    def write_list(self, messages : list):
        f = open(self.filepath, 'a', encoding='UTF-8')
        for message in messages:
            try:
                f.write('\n- ' + message + '\n')
            except TypeError:
                res = '\n- '
                for elem in message:
                    res += elem.__str__() + '\t'
                f.write('\n' + res[:-2] + '\n')
        f.close()
    
    def write_table(self, df : DataFrame, table_name = ''):
        writer = MarkdownTableWriter(
            table_name=table_name,
            dataframe=df,
        )
        f = open(self.filepath, 'a', encoding='UTF-8')
        f.write('\n' + writer.dumps() + '\n')
        f.close()