# auther:zhu
# 2024年03月17日14时50分59秒

from agentscope.message import Msg
from agentscope.msghub import msghub
from agentscope.pipelines.functional import sequentialpipeline
import agentscope
from agentscope.agents.user_agent import UserAgent
from functools import partial

def main() -> None:
    # default settings
    HostMsg = partial(Msg, name="Moderator", echo=True)
    actors = agentscope.init(
        model_configs="model_configs.json",
        agent_configs="agent_configs.json"
    )
    roles = ["consulter1", "consulter2", "Manager"]
    consulter1,consulter2,Manager = actors[0],actors[1],actors[2]
    user_agent = UserAgent()
    msg = Msg(name="Manager",content="Please discuss the fashion and outfit choices")
    x = None
    while x is None or x.content != "exit":
        with msghub(participants=[consulter1,consulter2,Manager],announcement=x) as hub:
            x = sequentialpipeline([consulter1, user_agent], x)
            consulter2()
            hub.broadcast(HostMsg(content="let the manager judge the result!"))
            Manager()


if __name__ == "__main__":
    main()