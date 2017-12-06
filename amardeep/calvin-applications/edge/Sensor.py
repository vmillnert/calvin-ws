
import sys
from calvin.actor.actor import Actor, manage, condition, stateguard, calvinsys

class Sensor(Actor):

    """
    Produce a counter token on the output every period seconds
    and for steps times, using a timer.
    Outputs:
      integer: Integer counter
    """

    @manage()
    def init(self, sleep=0.1, start=1, steps=sys.maxint):
        self.start = start
        self.count = start
        self.sleep = sleep
        self.steps = steps + start
        self.timer = calvinsys.open(self, 'sys.timer.once', period=self.sleep)

    # The counting action, first 3 use non periodic for testing purpose
    @stateguard(lambda self: self.count < self.start + 3 and self.count < self.steps and calvinsys.can_read(self.timer) and calvinsys.can_write(self.timer))
    @condition(action_output=('integer',))
    def step_no_periodic(self):
        calvinsys.read(self.timer) # Ack
        if self.count == self.start + 2:
            # now continue with periodic timer events
            calvinsys.close(self.timer)
            self.timer = calvinsys.open(self, 'sys.timer.repeating')
        calvinsys.write(self.timer, self.sleep)
        self.count += 1
        return (self.count - 1, )

    # The counting action, handle periodic timer events hence no need to setup repeatedly
    @stateguard(lambda self: self.count < self.steps and calvinsys.can_read(self.timer))
    @condition(action_output=('integer',))
    def step_periodic(self):
        calvinsys.read(self.timer) # Ack
        self.count += 1
        return (self.count - 1, )

    # Stop after given number of steps
    @stateguard(lambda self: self.count == self.steps)
    @condition()
    def stop(self):
        calvinsys.close(self.timer) # Stop
        self.count += 1
        self.timer = None

    def report(self, **kwargs):
        if kwargs.get("stopped", False):
            calvinsys.close(self.timer)
        return self.count - self.start

    action_priority = (step_no_periodic, step_periodic, stop)
    requires = ['sys.timer.once', 'sys.timer.repeating']


    test_calvinsys = {'sys.timer.once': {'read': ["dummy", "dummy", "dummy"],
                                         'write': [0.1, 0.1]},
                      'sys.timer.repeating': {'read': ["dummy", "dummy", "dummy", "dummy", "dummy"]}}
    test_set = [
        {
            'outports': {'integer': [1, 2, 3, 4, 5, 6, 7, 8]}
        }
    ]