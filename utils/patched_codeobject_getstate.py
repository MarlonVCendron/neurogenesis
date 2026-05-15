from brian2 import *
from brian2.core.functions import DEFAULT_FUNCTIONS

def patched_codeobject_getstate(self):
    state = self.__dict__.copy()
    state["owner"] = self.owner.__repr__.__self__
    state["variables"] = self.variables.copy()
    for k, v in state["variables"].items():
        if isinstance(v, Function) and k in DEFAULT_FUNCTIONS and v is DEFAULT_FUNCTIONS[k]:
            state["variables"][k] = k
    return state