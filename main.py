from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from agents import AIAPAgents
from tasks import AIAPTasks
from file_io import save_markdown
from dotenv import load_dotenv
from agent_loader import AgentLoader

load_dotenv()

# Initialize the agents and tasks
agents = AIAPAgents()
tasks = AIAPTasks()
num_features = 5

# Initialize the OpenAI GPT-4 language model
OpenAIGPT4 = ChatOpenAI(
    model="gpt-4"
)

# User Input
print("## Welcome to Mount Olympus")
print('-------------------------------')
print("## The AI Council of the Gods")
# Ask the user for the topic
productidea = input("What is your product idea?\n")

# Instantiate the agents
ap_processor_agent = agents.ap_processor_agent()
director_of_ap_agent = agents.director_of_ap_agent()
system_administrator_agent = agents.system_administrator_agent()
results_compiler_agent = agents.results_compiler_agent()

research_results = []
# Instantiate the tasks
research_results.append(tasks.research_task(ap_processor_agent, productidea, num_features))
research_results.append(tasks.research_task(director_of_ap_agent, productidea, num_features))
research_results.append(tasks.research_task(system_administrator_agent, productidea, num_features))
#analyze_task = tasks.analyze_task(system_administrator_agent, research_results)
compile_results_task = tasks.compile_results_task(results_compiler_agent, research_results, save_markdown)

#loader = AgentLoader('agents.json')
# Load agents from the file
#agents = loader.load_agents()

# Form the crew
crew = Crew(
    agents=[ap_processor_agent, director_of_ap_agent, system_administrator_agent, results_compiler_agent],
    tasks= research_results + [compile_results_task],
    process=Process.sequential, 
    manager_llm=OpenAIGPT4,
    verbose=1
)

# Kick off the crew's work
results = crew.kickoff()

# Print the results
print("Crew Work Results:")
print(results)


