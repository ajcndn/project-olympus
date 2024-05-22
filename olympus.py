from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from agents import AIAPAgents
from tasks import AIAPTasks
from file_io import save_markdown
from dotenv import load_dotenv
from agent_loader import AgentLoader

class Olympus:
    def __init__(self):
        load_dotenv()
        self.agents = AIAPAgents()
        self.tasks = AIAPTasks()
        self.num_features = 5
        self.OpenAIGPT4 = ChatOpenAI(model="gpt-4")
        self.research_results = []

    def get_user_input(self):
        print("## Welcome to Mount Olympus")
        print('-------------------------------')
        print("## The AI Council of the Gods")
        self.productidea = input("What is your product idea?\n")

    def instantiate_agents(self):
        self.ap_processor_agent = self.agents.ap_processor_agent()
        self.director_of_ap_agent = self.agents.director_of_ap_agent()
        self.system_administrator_agent = self.agents.system_administrator_agent()
        self.results_compiler_agent = self.agents.results_compiler_agent()

    def instantiate_tasks(self):
        self.research_results.append(self.tasks.research_task(self.ap_processor_agent, self.productidea, self.num_features))
        self.research_results.append(self.tasks.research_task(self.director_of_ap_agent, self.productidea, self.num_features))
        self.research_results.append(self.tasks.research_task(self.system_administrator_agent, self.productidea, self.num_features))
        self.compile_results_task = self.tasks.compile_results_task(self.results_compiler_agent, self.research_results, save_markdown)

    def form_crew_and_kickoff(self):
        crew = Crew(
            agents=[self.ap_processor_agent, self.director_of_ap_agent, self.system_administrator_agent, self.results_compiler_agent],
            tasks= self.research_results + [self.compile_results_task],
            process=Process.sequential, 
            manager_llm=self.OpenAIGPT4,
            verbose=1
        )
        self.results = crew.kickoff()

    def print_results(self):
        print("Crew Work Results:")
        print(self.results)