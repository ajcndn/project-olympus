from crewai import Crew, Process, Agent, Task
from agents import AIAPAgents
from tasks import AIAPTasks
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict, Optional
from dotenv import load_dotenv
from file_io import save_markdown
import panel as pn 
from crewai.agents import CrewAgentExecutor
import time 
#from crewai.agents import ChatOpenAI
pn.extension(design="material")
#pn.extension('chat', design='material', theme='dark')  # Set dark mode theme
import threading

load_dotenv()

def custom_ask_human_input(self, final_answer: dict) -> str:
      
      global user_input

      prompt = self._i18n.slice("getting_input").format(final_answer=final_answer)

      chat_interface.send(prompt, user="Assistant", respond=False)

      while user_input == None:
          time.sleep(1)  

      human_comments = user_input
      user_input = None

      return human_comments

CrewAgentExecutor._ask_human_input = custom_ask_human_input

user_input = None
initiate_chat_task_created = False

def initiate_chat(message):

    global initiate_chat_task_created
    # Indicate that the task has been created
    initiate_chat_task_created = True

    StartCrew(message)
    
def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    
    global initiate_chat_task_created
    global user_input

    if not initiate_chat_task_created:
        thread = threading.Thread(target=initiate_chat, args=(contents,))
        thread.start()
        # Directly call the function without creating a new thread
        #initiate_chat(contents)
        #initiate_chat_task_created = True
    else:
        user_input = contents

avatars = {
    "AP Processor": "avatars/approcessor.png",
    "Director of Accounts Payable": "avatars/directorofap.png",
    "System Administrator": "avatars/systemadmin.png",
    "Product Manager": "avatars/productmanager.png",
    "Assistant": "avatars/assistant.png"
}

class MyCustomHandler(BaseCallbackHandler):

    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""
        # comment this out if "assistant" is too chatty
        #chat_interface.send(inputs['input'], user="Assistant", respond=False)

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
    
        chat_interface.send(outputs['output'], user=self.agent_name, avatar=avatars[self.agent_name], respond=False)


llm = ChatOpenAI(model="gpt-4o")


approcessorllm = ChatOpenAI(model="gpt-3.5-turbo")
directorofAPllm = ChatOpenAI(model="gpt-3.5-turbo")
sysadminllm = ChatOpenAI(model="gpt-3.5-turbo")
productmanagerllm = ChatOpenAI(model="gpt-4o")

#handler
agent=AIAPAgents(callback=MyCustomHandler, llm=llm)
tasks = AIAPTasks()

#Agents
approcessor = agent.ap_processor_agent(approcessorllm)
directorofAP = agent.director_of_ap_agent(directorofAPllm)
sysadmin = agent.system_administrator_agent(sysadminllm)
productmanager = agent.product_manager_agent(productmanagerllm)

num_features = 5

#Tasks
def StartCrew(prompt):

    research_results = []
# Instantiate the tasks
    research_results.append(tasks.research_task(approcessor, prompt, num_features))
    research_results.append(tasks.research_task(directorofAP, prompt, num_features))
    research_results.append(tasks.research_task(sysadmin, prompt, num_features))
    compile_results_task = tasks.compile_results_task(productmanager, research_results, save_markdown)
       
    # Establishing the crew 
    crew = Crew(
        agents=[approcessor, directorofAP, sysadmin, productmanager],
        tasks= research_results + [compile_results_task],
        manager_llm=llm,
        #process=Process.hierarchical
        verbose=3,
        process=Process.sequential
    )

    result = crew.kickoff()


    #chat_interface.send(" Final Result\n"+result, user="Assistant", respond=False)
    chat_interface.send("💬 Thank you! Please refresh if you'd like to provide another idea!", user="Assistant", respond=False)

chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send("💬 Hello! Please provide a product idea and our council of AP experts will provide feedback!", user="Assistant", respond=False)
chat_interface.servable()
