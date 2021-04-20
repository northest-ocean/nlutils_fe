import json
import os

def request_args_to_folder(data_dict):
    name = data_dict['name']
    return f'./params/{name}/'



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

if __name__ == '__main__':
    x = PWJSONParser()
    y = x.parse_folder("./")
    print(list(y))