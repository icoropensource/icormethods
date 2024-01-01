# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

"""Finite state machine class

Right now, just about anything I read about programming
techniques and patterns makes me think "How would I do
that in Python?", so when http://www.imatix.com/ recently
posted about their Libero FSM-generator (which doesn't
do Python yet), I just had to try it myself.

(I am aware of Skip Montanaro's FSM module at
http://www.automatrix.com/~skip/python/fsm.py , but I
wanted to try a slightly different approach)
"""

class ICORFSM:
  """Finite State Machine Base Class

  Define a subclass with a mapping attribute for each
  state of the FSM.  These states map events to
  ('state', 'action') transitions, where 'state' is the name
  of the next state, and 'action' is the name of the action
  to perform before changing state.  Initialize an instance
  with an actor object which defines the implementations
  of the transition actions, then call the start method with
  the initial event.

  The pre-defined state 'initial_state' must be overridden,
  and a set of global default transitions may be defined
  by overriding 'defaults'.

  An event is first checked for a literal match.  If that fails,
  it is then passed to any callable keys until one of them
  returns a true value.  After that, global default transitions
  are checked for.

  An 'action' may be a callable attribute of the actor
  object with which the FSM was initialized, or it may be
  an event value (either literal or looked up in the actor).

  Callable actions may use the passed FSM parameter
  to look up the state, event, next_state, and match. They
  can also use it to set next_state explicitly.
  """
  initial_state = None
  STOP = []
  Error = ValueError
  defaults = {}

  def _noact(self, x):
    pass
  def _prep_states(self, states):
    memo = {'STOP': self.STOP}
    for statename in states:
      memo[statename] = getattr(self, statename)
    si = 0
    while si < len(states):
      statesrc = getattr(self, states[si])
      for item in statesrc.items():
        (event, (statename, actname)) = item
        if not memo.has_key(statename):
           states.append(statename)
           memo[statename] = getattr(self, statename)
      setattr(self, states[si], {})
      si = si + 1
    for statename in states:
      state = getattr(self, statename)
      for item in memo[statename].items():
        (event, (statename, actname)) = item
        # Actions are either attributes of actor, or literals
        try:
          action = getattr(self.actor, actname)
        except:
          action = actname
        state[event] = (getattr(self, statename), action)
      # Remember which 'events' are actually callable event tests.
      state[callable] = filter(callable, state.keys())

  def __init__(self, actor):
    self.actor = actor
    try:
      self._pre = getattr(actor, '__pre_hook__')
    except:
      self._pre = self._noact
    try:
      self._post = getattr(actor, '__post_hook__')
    except:
      self._post = self._noact
    self._prep_states(['initial_state', 'defaults'])

  def _get_transition(self, state, event):
      transition = state.get(event, None)
      if not transition:
         for event_test in state[callable]:
           self.match = event_test(event)
           if self.match:
              transition = state[event_test]
              break
         else:
           if state is self.defaults:
              raise self.Error, (self.state, self.event)
           else:
              return self._get_transition(self.defaults, event)
      self.next_state, action = transition
      return action

  def start(self, event):
    state = self.initial_state
    while state != self.STOP:
      self.state, self.event, self.match = state, event, None
      action = self._get_transition(state, event)
      self._pre(self)
      if callable(action):
         event = action(self)
      else:
         event = action
      self._post(self)
      state = self.next_state


