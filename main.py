from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from agents import AIAPAgents
from tasks import AIAPTasks
from file_io import save_markdown
from dotenv import load_dotenv
from agent_loader import AgentLoader
import streamlit as st
from handlers import MyCustomHandler

load_dotenv()

# Initialize the agents and tasks
agents = AIAPAgents()
tasks = AIAPTasks()
num_features = 5

# Initialize the OpenAI GPT-4 language model
OpenAIGPT4 = ChatOpenAI(
    model="gpt-4o"
)


# User Input
st.title("Welcome to Project Olympus")
st.subheader("Provide a product idea and we will gather feedback from the stakeholders.")
productidea = st.text_input("What is your product idea?")

# Instantiate the agents
ap_processor_agent = agents.ap_processor_agent(callback_handler=MyCustomHandler("ap_processor_agent"))
director_of_ap_agent = agents.director_of_ap_agent(callback_handler=MyCustomHandler("director_of_ap_agent"))
system_administrator_agent = agents.system_administrator_agent(callback_handler=MyCustomHandler("system_administrator_agent"))
product_manager_agent = agents.product_manager_agent(callback_handler=MyCustomHandler("product_manager_agent"))

research_results = []
# Instantiate the tasks
if st.button('Process Idea'):
    research_results.append(tasks.research_task(ap_processor_agent, productidea, num_features))
    research_results.append(tasks.research_task(director_of_ap_agent, productidea, num_features))
    research_results.append(tasks.research_task(system_administrator_agent, productidea, num_features))
    compile_results_task = tasks.compile_results_task(product_manager_agent, research_results, save_markdown)

    crew = Crew(
        agents=[ap_processor_agent, director_of_ap_agent, system_administrator_agent, product_manager_agent],
        tasks= research_results + [compile_results_task],
        process=Process.sequential, 
        manager_llm=OpenAIGPT4,
        verbose=2
    )

    # Kick off the crew's work
    results = crew.kickoff()

    # Print the results
    st.write("Crew Work Results:")
    st.write(results)