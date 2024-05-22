from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from agents import AIAPAgents
from tasks import AIAPTasks
from file_io import save_markdown
from dotenv import load_dotenv
from agent_loader import AgentLoader


load_dotenv()

# Initiate AgentOps
#import agentops
#agentops.init()

# Initialize the agents and tasks
agents = AIAPAgents()
tasks = AIAPTasks()
num_features = 5

# Initialize the OpenAI GPT-4 language model
OpenAIGPT4 = ChatOpenAI(
    #model="gpt-4"
    model="gpt-4o"
)

# User Input
print("## Welcome to Project Olympus")
print('-------------------------------')
print("## Provide a product idea and we will gather feedback from the stakeholders.")
# Ask the user for the topic
productidea = input("What is your product idea?\n")

# Instantiate the agents
ap_processor_agent = agents.ap_processor_agent()
director_of_ap_agent = agents.director_of_ap_agent()
system_administrator_agent = agents.system_administrator_agent()
product_manager_agent = agents.product_manager_agent()

research_results = []
# Instantiate the tasks
research_results.append(tasks.research_task(ap_processor_agent, productidea, num_features))
research_results.append(tasks.research_task(director_of_ap_agent, productidea, num_features))
research_results.append(tasks.research_task(system_administrator_agent, productidea, num_features))
#analyze_task = tasks.analyze_task(system_administrator_agent, research_results)
compile_results_task = tasks.compile_results_task(product_manager_agent, research_results, save_markdown)

#loader = AgentLoader('agents.json')
# Load agents from the file
#agents = loader.load_agents()

# Form the crew
#agentops.monitor.start("Overall Crew Process")
crew = Crew(
    agents=[ap_processor_agent, director_of_ap_agent, system_administrator_agent, product_manager_agent],
    tasks= research_results + [compile_results_task],
    process=Process.sequential, 
    manager_llm=OpenAIGPT4,
    verbose=2
)

# Kick off the crew's work
results = crew.kickoff()
#agentops.monitor.stop("Overall Crew Process")

# Print the results
print("Crew Work Results:")
print(results)


