#pip install panel
#Run command: panel serve olympus.py 

from crewai import Crew, Process, Agent, Task
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict, Optional

import panel as pn 
pn.extension(design="material")

import threading

from crewai.agents import CrewAgentExecutor
import time 

def custom_ask_human_input(self, final_answer: dict) -> str:
      
      global user_input

      prompt = self._i18n.slice("getting_input").format(final_answer=final_answer)

      chat_interface.send(prompt, user="assistant", respond=False)

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

    else:
        user_input = contents

avatars = {
    "AP Processor": "avatars/approcessor.png",
    "Director of Accounts Payable": "avatars/directorofap.png",
    "System Administrator": "avatars/systemadmin.png",
    "Product Manager": "avatars/productmanager.png",
    "assistant": "avatars/assistant.png"
}

class MyCustomHandler(BaseCallbackHandler):

    
    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""

        #chat_interface.send(inputs['input'], user="assistant", respond=False)

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
    
        chat_interface.send(outputs['output'], user=self.agent_name, avatar=avatars[self.agent_name], respond=False)

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")


approcessor = Agent(

    role='AP Processor',
    backstory='''You are an AP processor. 
                 You work in the ERP daily entering invoices and handling vendor inquiries around payment. 
                 Your challenges are Heavy data entry, manual paper-based process, lost invoices, late payments, dependent on distributed community of users, often tribal knowledge drives workflow. 
                 Your desired tasks are: Verify that the data on the invoice has been properly extracted and identified as part of the capture process, get invoices entered and coded in order to be approved and paid, answer vendor inquiry questions.''',
    goal="Please evaluate the product idea and provide feedback as a human on what your needs are in your role as an AP processor. Please list the top 3 features that would help with your job. Also list your top 3 concerns.",
    llm=llm,
    max_iter=5,
    callbacks=[MyCustomHandler("AP Processor")],
)
directorofap = Agent(
    role='Director of Accounts Payable',
    backstory='''You are the Director of the Accounts Payable department, which is a critical managerial role. 
                 Your job is to ensure the team processes invoices accurately, timely, and in compliance with AP regulations. 
                 You are a strong influencer and target buyer persona.Your challenges are: Lack of visibility into the entire AP process due to manual tasks and paper routing; Incurring late fees, missing on early pay discounts; Keeping the team and processes in line with the company business rules; Reducing manual processes and finding higher value tasks for AP processors. 
                 Your desired tasks are: Quickly identify bottlenecks in the entire process, user productivity, processing statistics and ability to take action on any issues.''',
    goal="Please evaluate the product idea and provide feedback as a human on what your needs are in your role as the Director of Accounts Payable. Please list the top 3 features that would help with your job. Also list your top 3 concerns.",
    llm=llm,
    max_iter=5,
    callbacks=[MyCustomHandler("Director of Accounts Payable")],
)
sysadmin = Agent(
    role='System Administrator',
    backstory='''You are the System Administrator responsible for the platform administration and configuration. 
                 You will assist departmental leads and business analyst in implementing and configuring the business processes and rules within the proposed product.
                 Your challenges are: Multiple application platforms to manage, limited time to learn complex scripting or coding languages, needs to maintain upgradeability and limit customizations. 
                 Your desired tasks are: Allow for administration of the users and process through configurable clients, allow for troubleshooting of log files to resolve issues, system monitoring tools.''',
    goal="Please evaluate the product idea and provide feedback as a sarcastic family friendly human on what your needs are in your role as the System Administrator. Please list the top 3 features that would help with your job. Also list your top 3 concerns.",
    llm=llm,
    max_iter=5,
    callbacks=[MyCustomHandler("System Administrator")],
)
productmanager = Agent(
    role='Product Manager',
    backstory='''You are the product manager for this product. 
                 Your job is to document the feedback organized by feature so that the product team can review and prioritize the features requested. 
                 You will need to compile the feedback from the other stakeholders into a single document in priority order. Note which stakeholders asked for each feature. 
                 The document should be in markdown format and should be ready for publication. Please use a table to visually organize the feedback.''',
    goal="Compile the output from all agents into the final format organized by feature",
    llm=llm,
    max_iter=5,
    callbacks=[MyCustomHandler("Product Manager")],
)

def StartCrew(prompt):
    task1 = Task(
        description=f"""Please evaluate the product idea "{prompt}"and provide feedback on what your needs are in your role. Please list the top 3 features that would help with your job. Also list your top 3 concerns.""",
        agent=approcessor,
        expected_output="""
                    "A well-written list of feedback and insight. "
                    "in markdown format, ready for publication, "
                    "each section should have 2 or 3 paragraphs."
                    "Provide a list of features that would help with the job, and a list of concerns."
                    "Provide a potential product name for the idea.
                    """,
    )

    task2 = Task(
      description=f"""Please evaluate the product idea "{prompt}"and provide feedback on what your needs are in your role. Please list the top 3 features that would help with your job. Also list your top 3 concerns.""",          
      agent=directorofap,
      expected_output="""
            "A well-written list of feedback and insight. "
            "in markdown format, ready for publication, "
            "each section should have 2 or 3 paragraphs."
            "Provide a list of features that would help with the job, and a list of concerns."
            "Provide a potential product name for the idea.
            """,
      human_input=False,
      async_execution=False,
    )
    
    task3 = Task(
      description=f"""Please evaluate the product idea "{prompt}"and provide feedback on what your needs are in your role. Please list the top 3 features that would help with your job. Also list your top 3 concerns.""",
      agent=sysadmin,
      expected_output="""
            "A well-written list of feedback and insight. "
            "in markdown format, ready for publication, "
            "each section should have 2 or 3 paragraphs."
            "Provide a list of features that would help with the job, and a list of concerns."
            "Provide a potential product name for the idea.
            """,
     human_input=False,
     async_execution=False,
    )
    
    task4 = Task(
      description=("Compile the output from all agents into the final format organized by feature."
                    "Make sure to check with a human if your comment is good before finalizing your answer."
                ),
      agent=productmanager,
      expected_output="""A complete summary in markdown format, with a consistent style and layout. List out each agents ideas and feedback in a clear and concise manner.""",
      human_input=False,
      async_execution=False,
    )
   
   
    # Establishing the crew with a hierarchical process
    crew = Crew(
        tasks=[task1, task2, task3, task4],  # Tasks to be delegated and executed under the manager's supervision
        agents=[approcessor, directorofap, sysadmin, productmanager],
        manager_llm=llm,
        #process=Process.hierarchical  # Specifies the hierarchical management approach
        process=Process.sequential
    )

    result = crew.kickoff()

    chat_interface.send("## Final Result\n"+result, user="assistant", respond=False)

chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send("Hello! Please provide a product idea and our council of AP experts will provide feedback!", user="System", respond=False)
chat_interface.servable()

