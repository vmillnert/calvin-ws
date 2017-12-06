

from calvin.actor.actor import Actor, manage, condition, stateguard
from calvin.utilities.calvinlogger import get_logger

_log = get_logger(__name__)


class Actuator(Actor):
    """
    Write tokens to standard output
    Input:
      token : Any token
    """

    def exception_handler(self, action, args):
        # Check args to verify that it is EOSToken
        return action(self, *args)

    @manage(['tokens', 'store_tokens', 'quiet', 'active'])
    def init(self, store_tokens=False, quiet=False, active=True):
        self.store_tokens = store_tokens
        self.tokens = []
        self.quiet = quiet
        self.active = active
        self.setup()

    def did_migrate(self):
        self.setup()

    def setup(self):
        if self.quiet:
            self.logger = _log.debug
        else:
            self.logger = _log.info

    @stateguard(lambda self: self.active)
    @condition(action_input=['token'])
    def log(self, token):
        if self.store_tokens:
            self.tokens.append(token)
        self.logger("%s<%s>: %s" % (self.__class__.__name__, self.id, str(token).strip()))

    action_priority = (log, )

    def report(self, **kwargs):
        self.active = kwargs.get('active', self.active)
        if 'port' in kwargs:
            return self.inports['token']._state()
        return self.tokens

    test_kwargs = {'store_tokens': True}

    test_set = [
        {
            'inports': {'token': ['aa', 'ba', 'ca', 'da']},
            'outports': {},
            'postcond': [lambda self: self.tokens == ['aa', 'ba', 'ca', 'da']]
        }
    ]
