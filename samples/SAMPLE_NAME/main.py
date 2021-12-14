import os
import time
from microsoft_bonsai_api.simulator.client import BonsaiClient, BonsaiClientConfig
from microsoft_bonsai_api.simulator.generated.models import SimulatorInterface, SimulatorState, SimulatorSessionResponse

workspace = os.getenv("SIM_WORKSPACE")
accesskey = os.getenv("SIM_ACCESS_KEY")

config_client = BonsaiClientConfig()
client = BonsaiClient(config_client)

registration_info = SimulatorInterface(
    name="MY_SIMULATOR_NAME",
    timeout=60,
    simulator_context=config_client.simulator_context,
    description=None,
)

registered_session: SimulatorSessionResponse = client.session.create(workspace_name=config_client.workspace, body=registration_info)
print(f"Registered simulator. {registered_session.session_id}")

sequence_id = 1
sim_model = SimulatorModel()
sim_model_state = { 'sim_halted': False }

try:
    while True:
        sim_state = SimulatorState(sequence_id=sequence_id, state=sim_model_state, halted=sim_model_state.get('sim_halted', False))
        event = client.session.advance(
            workspace_name=config_client.workspace,
            session_id=registered_session.session_id,
            body=sim_state,
        )
        sequence_id = event.sequence_id

        if event.type == "Idle":
            time.sleep(event.idle.callback_time)
        elif event.type == "EpisodeStart":
            sim_model_state = sim_model.reset(event.episode_start.config)
        elif event.type == "EpisodeStep":
            sim_model_state = sim_model.step(event.episode_step.action)
        elif event.type == "EpisodeFinish":
            sim_model_state = { 'sim_halted': False }
        elif event.type == "Unregister":
            print(f"Simulator Session unregistered by platform because '{event.unregister.details}'")
            return
except BaseException as err:
    client.session.delete(workspace_name=config_client.workspace, session_id=registered_session.session_id)
    print(f"Unregistered simulator because {type(err).__name__}: {err}")
