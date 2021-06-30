class WSConfigureLoadException(Exception):

    def __init__(self, *args):
        self.args = args

class WSFetchGPUServerInfoException(Exception):

    def __init__(self, *args):
        self.args = args

class WSConditionTypeException(Exception):

    def __init__(self, *args):
        self.args = args