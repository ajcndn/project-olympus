# agent_loader.py
import json
from crewai import Agent

class AgentLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_agents(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)

        agents = []
        for agent_data in data:
            agent = Agent(
                role=agent_data['role'],
                goal=agent_data['goal'],
                backstory=agent_data['backstory'],
                allow_delegation=agent_data['allow_delegation'],
                verbose=agent_data.get('verbose', False)  # optional field, default to False if not present
            )
            agents.append(agent)

        return agents

    def save_agents(self, agents):
        data = []
        for agent in agents:
            agent_data = {
                'role': agent.role,
                'goal': agent.goal,
                'backstory': agent.backstory,
                'allow_delegation': agent.allow_delegation,
                'verbose': agent.verbose
            }
            data.append(agent_data)

        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)