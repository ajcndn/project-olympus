import streamlit as st
from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from agents import AIAPAgents
from tasks import AIAPTasks
from file_io import save_markdown
from dotenv import load_dotenv

load_dotenv()

# Initialize the agents and tasks
agents = AIAPAgents()
tasks = AIAPTasks()
num_features = 5

# Initialize the OpenAI GPT-4 language model
llm = ChatOpenAI(
    model="gpt-3.5-turbo"
    #model="gpt-4-turbo"
    #model="gpt-4o"
    
)

st.title("💬 Project Olympus") 

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! Please provide a product idea and our team will provide feedback."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Instantiate the agents
    ap_processor_agent = agents.ap_processor_agent()
    director_of_ap_agent = agents.director_of_ap_agent()
    system_administrator_agent = agents.system_administrator_agent()
    results_compiler_agent = agents.results_compiler_agent()

    research_results = []
    # Instantiate the tasks
    research_results.append(tasks.research_task(ap_processor_agent, prompt, num_features))
    research_results.append(tasks.research_task(director_of_ap_agent, prompt, num_features))
    research_results.append(tasks.research_task(system_administrator_agent, prompt, num_features))
    compile_results_task = tasks.compile_results_task(results_compiler_agent, research_results, save_markdown)

    # Form the crew
    crew = Crew(
        agents=[ap_processor_agent, director_of_ap_agent, system_administrator_agent, results_compiler_agent],
        tasks= research_results + [compile_results_task],
        process=Process.sequential, 
        #process=Process.hierarchical,
        manager_llm=llm,
        verbose=2
    )

    final = crew.kickoff()

    result = f"## Here is the Final Result \n\n {final}"
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result)
 
    # Print the results
    #print("Crew Work Results:")
    #print(final)


