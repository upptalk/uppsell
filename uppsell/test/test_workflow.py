from django.test import TestCase
from django.db import models
from uppsell.workflow import Manager, State, BadTransition

class ExampleModel(object):
    state = 'A'
    #def __repr__(self): return "<ExampleModel %s>"%self.state

class WorkflowManagerTestCase(TestCase):
    
    _model = None
    _manager = None

    def set_up(self):
        self._model = ExampleModel()
        self._manager = Manager(self._model)
    
    def test_state(self):
        s1 = State(self._manager, "A")
        s2 = State(self._manager, "B")
        s1.add_transition("go", s2)
        self.assertTrue(s1.can("go"))
        self.assertFalse(s1.can("stop"))
        self.assertEqual(s2, s1.next("go"))

    def test_manager(self):
        transitions = (
            ("TR_1", "A", "B"),
            ("TR_1", "B", "A"),
            ("TR_2", "B", "C"),
            ("TR_3", "C", "D"),
        )
        model = ExampleModel()
        manager = Manager(model)
        manager.set_transitions(transitions)
        
        self.assertTrue(manager.can("TR_1"))
        self.assertFalse(manager.can("TR_2"))
        self.assertFalse(manager.can("TR_3"))
        
        manager.do_transition("TR_1")

        self.assertEqual("B", getattr(model, "state"))
        self.assertTrue(manager.can("TR_1"))
        self.assertTrue(manager.can("TR_2"))
        self.assertFalse(manager.can("TR_3"))
        
        self.assertRaises(BadTransition, manager.do_transition, "TR_3")

