from django.dispatch import Signal
from uppsell.exceptions import CancelTransition, BadTransition

pre_transition = Signal(providing_args=["model", "state", "transition"])
post_transition = Signal(providing_args=["model", "state", "transition"])

def pre_transition_handler(callback, on_key, on_model, on_state="__all__", on_transition="__all__"):
    def wrapper(signal, key, transition, sender, model, state):
        if model == on_model and \
           on_state in (state, "__all__") and \
           on_transition in (transition, "__all__"):
               return callback(signal, transition, sender, model, state)
        return
    pre_transition.connect(wrapper)
    return wrapper

def post_transition_handler(callback, on_key, on_model, on_state="__all__", on_transition="__all__"):
    def wrapper(signal, key, transition, sender, model, state):
        if model == on_model and \
           key == on_key and \
           on_state in (state, "__all__") and \
           on_transition in (transition, "__all__"):
               return callback(signal, key, transition, sender, model, state)
        return
    post_transition.connect(wrapper)
    return wrapper

class State(object):
    _manager, _state, _transitions = None, None, None

    def __init__(self, manager, state):
        self._manager = manager
        self._state = state
        self._transitions = {}

    def add_transition(self, transition, end_state):
        if self._transitions.get(transition):
            raise ValueError, u"State %s already has transition %s defined" \
                    % (self.__unicode__(), transition)
        self._transitions[transition] = end_state
    
    @property
    def transitions(self):
        return self._transitions
    def can(self, transition):
        return self._transitions.has_key(transition)
    def next(self, transition):
        if self.can(transition):
            return self._transitions[transition]
        return self
    def __unicode__(self):
        return self._state
    def __repr__(self):
        return "<State %s>"%self._state

class Workflow(object):
    
    _model, _key, _states = None, None, None

    def __init__(self, model, key=u"state", transitions=[]):
        self._model, self._key = model, key
        self.set_transitions(transitions)
    
    @property
    def state(self):
        state_id = getattr(self._model, self._key)
        return self._states[state_id]
    
    def add_state(self, state):
        if self._states.get(state) is None:
            self._states[state] = State(self, state)
        return self._states[state]
    
    def set_transitions(self, transitions):
        self._states = {}
        for (transition, start, finish) in transitions:
            self.add_transition(transition, start, finish)
        return self
    
    def add_transition(self, transition, start, finish):
        self.add_state(start).add_transition(transition, self.add_state(finish))
        return self
    
    def can(self, transition):
        return self.state.can(transition)
    
    @property
    def available(self):
        return self.state.transitions
    
    def do(self, transition):
        if not self.can(transition):
            raise BadTransition, u"Model %s in state %s cannot apply transition %s"\
                % (self._model, self.state, transition)
        cur_state = self.state.__unicode__()
        new_state = self.state.next(transition).__unicode__()
        try:
            pre_transition.send(self, model=self._model, key=self._key, \
                    state=cur_state, transition=transition)
        except CancelTransition:
            return
        setattr(self._model, self._key, new_state)
        post_transition.send_robust(self, model=self._model, key=self._key, \
                state=new_state, transition=transition)

