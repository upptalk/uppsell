
def transition_callback(callback):
    """
    Decorator to check that a user is logged in.
    """
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user", None):
            return HttpResponseRedirect("/activate/")
        return controller(request, *args,  **kwargs)
    wrapper.__doc__ = controller.__doc__
    wrapper.__name__ = controller.__name__  
    return wrapper

class BadTransition(Exception):
    pass

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

class Manager(object):
    
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

    def do_transition(self, transition):
        if not self.can(transition):
            raise BadTransition, u"Model %s in state %s cannot apply transition %s"\
                    % (self._model, self.state, transition)
        new_state = self.state.next(transition)
        setattr(self._model, self._key, new_state.__unicode__())

