from typing import NamedTuple, Dict, Any

class SimulatorModel:
    def __init__(self):
        # TODO: Perform any global runtime simulator initialization that is needed here.
        pass

    def reset(self, config) -> Dict[str, Any]:
        # TODO: Reset state from the previous episode that needs to be cleared.
        # TODO: Perform initialization in preparation for running an episode using the values in the config dictionary.
        return { 
            'sim_halted': False,
            # TODO: Add simulator state as dictionary with key as the state and value as the state's value.
            'key': value,
        }

    def step(self, action) -> Dict[str, Any]:
        # TODO: Perform a simulation step using the values in the action dictionary.
        return {
            # TODO: If 'sim_halted' is set to True, that indicates that the simulator is unable to continue and the
            # episode will be discarded. If your simulator cannot reach an unrecoverable state, always set 'sim_halted'
            # to False.
            'sim_halted': False,
            # TODO: Add simulator state as dictionary with key as the state and value as the state's value.
            'key': value,
        }
