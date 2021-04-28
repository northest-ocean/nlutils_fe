import json
import os
import time

from multiprocessing import Process
from nlutils.Utils.Log import Logger


global_logger = Logger.get_logger()


def request_args_to_folder(data_dict):
    server = data_dict['server']
    name = data_dict['name']
    if name is None:
        name = ''
    return f'./params/{name}/' if server is None else f'./{server}/{name}/'

class PWJSONParser(object):

    def __new__(cls,*args,**kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls,*args,**kwargs)
        return cls._instance


    def __init__(self):
        pass

    def parse_file(self, filename):
        with open(filename, 'r') as f:
            obj = json.load(f)
        return obj

    def parse_folder(self, folder):
        if not os.path.isdir(folder):
            raise ValueError(f"{folder} is not a folder")
        json_paths = []
        for folder, _ , folder_files in os.walk(folder):
            for folder_file in folder_files:
                abs_path = os.path.join(folder, folder_file)
                if abs_path.split('.')[-1] == 'json' and 'fail' not in abs_path:
                    json_paths.append(abs_path)
        return list(map(lambda x:self.parse_file(x),json_paths))

class DeamonFetcher(object):

    def __init__(self):
        pass

    @staticmethod
    def fetch_from_servers():
        while True:
            with open('./server.conf', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.replace('\n', '')
                    username, server, remote_path, local_alias = line.split(' ')
                    global_logger.info(f"Fetching data from {server}.")
                    os.system(f"bash fetch_data.sh {username} {server} {remote_path} {local_alias}")
            time.sleep(1000)

    def run(self):
        self._process = Process(target=DeamonFetcher.fetch_from_servers)
        self._process.start()
    
    def terminate(self):
        self._process.terminate()




if __name__ == '__main__':
    x = PWJSONParser()
    y = x.parse_folder("./")
    print(list(y))