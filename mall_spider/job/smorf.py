class Smorf(object):

    def __my_init(self, args=None):
        self.init()

    def init(self):
        pass

    def init_argparse(self, parser):
        pass

    def process(self):
        raise RuntimeError("Smorf.process must be overwrited")

    def run(self):
        self.__my_init()

        while True:
            self.process()
