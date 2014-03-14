from django.test import TestCase
from django.db import models
from uppsell.workflow import Workflow, State, BadTransition,\
        pre_transition, post_transition

class ExampleModel(object):
    state = 'A'
    flag = 'RED'
    def __init__(self):
        self.state, self.flag = "A", "RED"
    #def __repr__(self): return "<ExampleModel %s>"%self.state

class WorkflowTestCase(TestCase):
    
    _model = None
    _manager = None

    def set_up(self):
        self._model = ExampleModel()
        self._manager = Workflow(self._model)
    
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
        manager = Workflow(model)
        manager.set_transitions(transitions)
        
        self.assertRaises(BadTransition, manager.do, "TR_2")
        self.assertRaises(BadTransition, manager.do, "TR_3")
        
        self.assertTrue(manager.can("TR_1"))
        self.assertFalse(manager.can("TR_2"))
        self.assertFalse(manager.can("TR_3"))
        
        manager.do("TR_1")

        self.assertEqual("B", getattr(model, "state"))
        self.assertTrue(manager.can("TR_1"))
        self.assertTrue(manager.can("TR_2"))
        self.assertFalse(manager.can("TR_3"))
        
        manager.do("TR_1")

        self.assertEqual("A", model.state)
        self.assertTrue(manager.can("TR_1"), "TR_1 is a valid transition from state A")
        self.assertFalse(manager.can("TR_2"), "TR_2 is not a valid transition from state A")
        self.assertFalse(manager.can("TR_3"), "TR_3 is not a valid transition from state A")
        
        self.assertRaises(BadTransition, manager.do, "TR_3")

    def test_manager_pre_transition_signal(self):
        transitions = (
            ("TR_1", "A", "B"),
        )
        model = ExampleModel()
        self.assertEqual('RED', model.flag)
        manager = Workflow(model)
        manager.set_transitions(transitions)
        
        def pre_transition_event(signal, transition, sender, model, state):
            self.assertEqual("A", state)
            self.assertEqual("TR_1", transition)
            self.assertEqual("ExampleModel", model.__class__.__name__)
            ExampleModel.flag = "BLUE"
        
        pre_transition.connect(pre_transition_event)
        manager.do("TR_1")
        self.assertEqual("B", getattr(model, "state"))
        self.assertEqual('BLUE', ExampleModel.flag)
        
    def test_manager_post_transition_signal(self):
        transitions = (
            ("TR_1", "A", "B"),
        )
        model = ExampleModel()
        self.assertEqual('RED', model.flag)
        manager = Workflow(model)
        manager.set_transitions(transitions)
        
        def post_transition_event(signal, transition, sender, model, state):
            self.assertEqual("B", state)
            self.assertEqual("TR_1", transition)
            self.assertEqual("ExampleModel", model.__class__.__name__)
            ExampleModel.flag = "BLUE"
        
        post_transition.connect(post_transition_event)
        manager.do("TR_1")
        self.assertEqual("B", getattr(model, "state"))
        self.assertEqual('BLUE', ExampleModel.flag)
        
