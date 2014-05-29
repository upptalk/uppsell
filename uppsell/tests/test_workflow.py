from django.test import TestCase
from django.db import models
from uppsell.workflow import Workflow, State, BadTransition, \
        pre_transition_signal, post_transition_signal, \
        pre_transition, post_transition

class ExampleModel(object):
    test_state = 'A'
    flag = 'RED'
    def __init__(self):
        self.test_state = "A"

class WorkflowTestCase(TestCase):
    
    _model = None
    _manager = None
    
    def setUp(self):
        self._model = ExampleModel()
        self._manager = Workflow(self._model, "test_state")
        ExampleModel.flag = "RED"
    
    def tearDown(self):
        self._model, self._manager = None, None
    
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
        manager = Workflow(model, "test_state")
        manager.set_transitions(transitions)
        
        self.assertRaises(BadTransition, manager.do, "TR_2")
        self.assertRaises(BadTransition, manager.do, "TR_3")
        
        self.assertTrue(manager.can("TR_1"))
        self.assertFalse(manager.can("TR_2"))
        self.assertFalse(manager.can("TR_3"))
        
        manager.do("TR_1")

        self.assertEqual("B", getattr(model, "test_state"))
        self.assertTrue(manager.can("TR_1"))
        self.assertTrue(manager.can("TR_2"))
        self.assertFalse(manager.can("TR_3"))
        
        manager.do("TR_1")

        self.assertEqual("A", model.test_state)
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
        manager = Workflow(model, "test_state")
        manager.set_transitions(transitions)
        
        def pre_transition_event(signal, key, transition, sender, model, state):
            self.assertEqual("A", state)
            self.assertEqual("TR_1", transition)
            self.assertEqual(ExampleModel, model.__class__)
            ExampleModel.flag = "BLUE"
        
        pre_transition_signal.connect(pre_transition_event)
        manager.do("TR_1")
        self.assertEqual("B", getattr(model, "test_state"))
        self.assertEqual('BLUE', ExampleModel.flag)
        pre_transition_signal.disconnect(pre_transition_event)
        
    def test_manager_post_transition_signal(self):
        transitions = (("TR_1", "A", "B"),)
        model = ExampleModel()
        manager = Workflow(model, "test_state")
        manager.set_transitions(transitions)
        
        def post_transition_event(signal, *args, **kwargs):
            self.assertEqual("B", kwargs["state"])
            self.assertEqual("TR_1", kwargs["transition"])
            self.assertEqual(ExampleModel, kwargs["model"].__class__)
            ExampleModel.flag = "BLUE"
        
        post_transition_signal.connect(post_transition_event)
        manager.do("TR_1")
        self.assertEqual("B", getattr(model, "test_state"))
        self.assertEqual('BLUE', ExampleModel.flag)
       
    def test_pre_transition_decorator(self):
        transitions = (("TR_5", "A", "B"),)
        self.assertEqual('RED', ExampleModel.flag)
        self._manager.set_transitions(transitions)
        
        # This get's called
        @pre_transition("test_state", ExampleModel, "TR_5", "A")
        def pre_transition_task(signal, key, transition, sender, model, state):
            self.assertEqual("A", state)
            self.assertEqual("TR_5", transition)
            self.assertEqual(ExampleModel, model.__class__)
            ExampleModel.flag = "BLUE"
        
        # This doesn't get called
        @pre_transition("test_state", ExampleModel, "WRONG_TRANS", "A")
        def pre_transition_task_2(signal, key, transition, sender, model, state):
            ExampleModel.flag = "ORANGE"
        
        self._manager.do("TR_5")
        self.assertEqual("B", getattr(self._model, "test_state"))
        self.assertEqual('BLUE', ExampleModel.flag)
       
    def test_post_transition_decorator(self):
        transitions = (("TR_6", "A", "B"),)
        self.assertEqual('RED', ExampleModel.flag)
        self._manager.set_transitions(transitions)
        
        @post_transition("test_state", ExampleModel, "TR_6")
        def post_transition_task(signal, key, transition, sender, model, state):
            self.assertEqual("B", state)
            self.assertEqual("TR_6", transition)
            self.assertEqual(ExampleModel, model.__class__)
            ExampleModel.flag = "BLUE"
        
        self._manager.do("TR_6")
        self.assertEqual("B", getattr(self._model, "test_state"))
        self.assertEqual('BLUE', ExampleModel.flag)
       

