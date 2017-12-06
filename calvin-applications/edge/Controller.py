
from calvin.actor.actor import Actor, manage, condition
import time  # NEVER DO THIS OUTSIDE OF TEST

class Controller(Actor):
    """
    forward a token unchanged and Burns cycles
    Inputs:
      token : a token
    Outputs:
      token : the same token
    """
    @manage(['dump', 'last', 'duration'])
    def init(self, dump=False, duration=0.1):
        self.dump = dump
        self.last = None
        self.duration = duration

    def log(self, data):
        print "%s<%s,%s>: %s" % (self.__class__.__name__, self.name, self.id, data)

    @condition(['token'], ['token'])
    def donothing(self, input):
        if self.dump:
            self.log(input)
        self.last = input
        # Burn cycles until duration passed
        t = time.time()
        while time.time() - t < self.duration:
            pass
        return (input, )

    def report(self, **kwargs):
        self.duration = kwargs.get('duration', self.duration)
        return self.last

    action_priority = (donothing, )

    test_set = [
        {
            'setup': [lambda self: self.init(duration=0.0001)],
            'inports': {'token': [1, 2, 3]},
            'outports': {'token': [1, 2, 3]}
        }
    ]
