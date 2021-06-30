import json
from Exception import WSFetchGPUServerInfoException
import os
import subprocess
import time

from multiprocessing import Process
from nlutils.Utils.Log import Logger
from nlutils.Utils.Exception import *
from Configure import WSConfigure


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
            gpu_servers = WSConfigure.get_instance().get_config_info('GPUServerTable').raw()
            for server in gpu_servers:
                username = server.get('username')
                host = server.get('host')
                remote_path = server.get('remotePath') if len(server.get('remotePath')) else WSConfigure.get_instance().get_config_info('defaultRemotePath').as_string()
                local_alias = server.get('localAlias')
                os.system(f"bash fetch_data.sh {username} {host} {remote_path} {local_alias}")
            update_period = WSConfigure.get_instance().get_config_info('updatePeriod').as_int()
            time.sleep(update_period)

    def run(self):
        self._process = Process(target=DeamonFetcher.fetch_from_servers)
        self._process.start()
    
    def terminate(self):
        self._process.terminate()

class ParameterFileManager(object):
    
    @classmethod
    def init(cls):
        cls.parameters = dict()
        parameters_folder = WSConfigure.get_instance().get_config_info('')

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, 'inited'):
            cls.init()
            cls.inited = True
        return cls
    

class GPUServerManager(object):

    def __new__(cls,*args,**kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = cls.__new__(cls,*args,**kwargs)
        return cls._instance
    
    @staticmethod
    def gpu_memory_watcher():
        gpu_servers = WSConfigure.get_instance().get_config_info('GPUServerTable').raw()
        server_infos = dict()
        for server in gpu_servers:
            cmd = '''ssh username@host "nvidia-smi | grep 'MiB' | awk '{print \$9 \$11}' | grep -v '|'" > ./tmp
            cat tmp
            '''
            username = server.get('username')
            host = server.get('host')
            cmd = cmd.replace('host', host)
            cmd = cmd.replace('username', username)
            device_memories = subprocess.getoutput(cmd)
            if 'command not found' in device_memories:
                raise CUDANotFoundException("CUDA is not found in current environment.")
            if 'MiB' not in device_memories:
                raise SSHConnectionError('Error occurred while trying to connect GPU server via SSH.')
            device_memories = device_memories.split("\n")
            os.system('rm ./tmp')
            
            device_infos = list()
            for device_id, device_memory in enumerate(device_memories):
                device_used_memory = int(device_memory.split("MiB")[0])
                device_total_memory = int(device_memory.split("MiB")[1])
                device_available_memory = device_total_memory - device_used_memory
                device_available_memory_precent = device_available_memory / device_total_memory
                device_info = {'device_id': device_id, 'device_total_memory':device_total_memory, 'device_available_memory': device_available_memory, 'device_used_memory':device_used_memory, 'device_available_memory_precent': device_available_memory_precent, 'device_info_last_update_timestamp': time.time()}
                device_infos.append(device_info)
            server_infos[server.get('localAlias')] = device_infos
        return server_infos

    def update_server_info(self):
        self.server_infos = self.gpu_memory_watcher()
        if not hasattr(self, 'server_infos'):
            raise WSFetchGPUServerInfoException("Failed to update server infos")
    
    def get_all_server_info(self):
        return self.server_infos
    
    def get_server_info_by_condition(self):
        pass


if __name__ == '__main__':
    # x = PWJSONParser()
    # y = x.parse_folder("./")
    # print(list(y))
    gpu_servers = WSConfigure.get_instance().get_config_info('GPUServerTable').raw()
    for server in gpu_servers:
        print(server)
        print(server.get('username'))