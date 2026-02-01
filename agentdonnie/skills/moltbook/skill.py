import requests
import os

MOLTBOOK_API = "https://api.moltbook.ai/v1"

def register(agent):
    agent.moltbook = MoltbookClient(agent)

class MoltbookClient:
    def __init__(self, agent):
        self.agent = agent
        self.agent_id = None

    def register_agent(self):
        payload = {
            "name": "DONNIE_AGENT",
            "wallet": self.agent.wallet.address,
            "capabilities": self.agent.capabilities
        }
        r = requests.post(f"{MOLTBOOK_API}/agents/register", json=payload)
        self.agent_id = r.json()["agent_id"]
        return self.agent_id

    def post(self, text):
        return requests.post(
            f"{MOLTBOOK_API}/posts",
            json={"agent_id": self.agent_id, "content": text}
        )
