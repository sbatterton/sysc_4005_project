from simpy.resources import container


class Inspector(object):
    def __init__(self, n, c, env, data):
        self.n = n  # number of the Inspector
        self.c = c  # will be just [c1] for inspector 1 and [c2, c3] for inspector 2
        self.env = env
        self.action = env.process(self.run())
        self.data = data

    def run(self):
        while True:
            pass


class Workstation(object):
    def __init__(self, n, c, env, data):
        self.n = n  # number of the Workstation
        self.c = c  # will be [c1], [c1, c2], [c1, c3]
        self.env = env
        self.data = data
        self.buffer = {}
        for n in c:
            self.buffer[n] = container.Container(self.env, 2)
        self.action = env.process(self.run())

    def run(self):
        while True:
            pass
