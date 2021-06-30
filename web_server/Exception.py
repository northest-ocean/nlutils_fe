class WSConfigureLoadException(Exception):

    def __init__(self, *args):
        self.args = args