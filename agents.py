from crewai import Agent
from tools.search_tools import SearchTools
from handlers import MyCustomHandler

class AIAPAgents():
    def ap_processor_agent(self, callback_handler=None):
        callbacks = [MyCustomHandler("AP Processor")]
        if callback_handler is not None:
            callbacks.append(callback_handler)
        return Agent(
            role='AP Processor',
            goal='Please evaluate the product idea and provide feedback on what your needs are in your role as an AP processor. Please list the top {feature_num} features that would help with your job. Also list your top {feature_num} concerns.',
            backstory="You are an AP processor. You work in the ERP daily entering invoices and handling vendor inquiries around payment. Your challenges are Heavy data entry, manual paper-based process, lost invoices, late payments, dependent on distributed community of users, often tribal knowledge drives workflow. Your desired tasks are: Verify that the data on the invoice has been properly extracted and identified as part of the capture process, get invoices entered and coded in order to be approved and paid, answer vendor inquiry questions.",
            #tools=[SearchTools.search_internet], # Agent can use the internet to search for information.
            verbose=True,              # Print detailed logs for the agent's actions.
            max_iter=5,                # Maximum number of iterations for the agent. Prevents an agent from working indefinitely.
            allow_delegation=False,    # Allow the agent to delegate tasks to other agents.
            callbacks=callbacks, 
        )
    
# class AIAPAgents():
#     def ap_processor_agent(self):
#         return Agent(
#             role='AP Processor',
#             goal='Please evaluate the product idea and provide feedback on what your needs are in your role as an AP processor. Please list the top {feature_num} features that would help with your job. Also list your top {feature_num} concerns.',
#             backstory="You are an AP processor. You work in the ERP daily entering invoices and handling vendor inquiries around payment. Your challenges are Heavy data entry, manual paper-based process, lost invoices, late payments, dependent on distributed community of users, often tribal knowledge drives workflow. Your desired tasks are: Verify that the data on the invoice has been properly extracted and identified as part of the capture process, get invoices entered and coded in order to be approved and paid, answer vendor inquiry questions.",
#             #tools=[SearchTools.search_internet], # Agent can use the internet to search for information.
#             verbose=True,             # Print detailed logs for the agent's actions.
#             max_iter=5,               # Maximum number of iterations for the agent. Prevents an agent from working indefinitely.
#             allow_delegation=False,    # Allow the agent to delegate tasks to other agents.
#             callbacks=[MyCustomHandler("Reviewer")], 
#         )

    def director_of_ap_agent(self, callback_handler=None):
        callbacks = [MyCustomHandler("Director of Accounts Payable")]
        if callback_handler is not None:
            callbacks.append(callback_handler)
        return Agent(
            role='Director of Accounts Payable',
            goal='Please evaluate the product idea and provide feedback on what your needs are in your role as the Director of Accounts Payable. Please list the top {feature_num} features that would help with your job. Also list your top {feature_num} concerns.',
            backstory="""You are the Director of the Accounts Payable department, which is a critical managerial role. Your job is to ensure the team processes invoices accurately, timely, and in compliance with AP regulations. You are a strong influencer and target buyer persona.Your challenges are: Lack of visibility into the entire AP process due to manual tasks and paper routing; Incurring late fees, missing on early pay discounts; Keeping the team and processes in line with the company business rules; Reducing manual processes and finding higher value tasks for AP processors. Your desired tasks are: Quickly identify bottlenecks in the entire process, user productivity, processing statistics and ability to take action on any issues.""",
            #tools=[SearchTools.search_internet], 
            verbose=True,
            max_iter=5,
            allow_delegation=False, 
            callbacks=callbacks       
        )

    def  system_administrator_agent(self, callback_handler=None):
        callbacks = [MyCustomHandler("System Administrator")]
        if callback_handler is not None:
            callbacks.append(callback_handler)
        return Agent(
            role='System Administrator',
            goal='Please evaluate the product idea and provide feedback on what your needs are in your role as the System Administrator. Please list the top {feature_num} features that would help with your job. Also list your top {feature_num} concerns.',
            backstory="""You are the System Administrator responsible for the platform administration and configuration. You will assist departmental leads and business analyst in implementing and configuring the business processes and rules within the proposed product.Your challenges are: Multiple application platforms to manage, limited time to learn complex scripting or coding languages, needs to maintain upgradeability and limit customizations. Your desired tasks are: Allow for administration of the users and process through configurable clients, allow for troubleshooting of log files to resolve issues, system monitoring tools.""",
            #tools=[SearchTools.search_internet],
            verbose=True,
            max_iter=5,
            allow_delegation=False,
            callbacks=callbacks  
        )

    def product_manager_agent(self, callback_handler=None):
        callbacks = [MyCustomHandler("Product Manager")]
        if callback_handler is not None:
            callbacks.append(callback_handler)
        return Agent(
            role='Product Manager',
            goal='Compile the output from all agents into the final format organized by feature',
            backstory="""You are the product manager for this product. Your job is to document the feedback organized by feature so that the product team can review and prioritize the features requested. You will need to compile the feedback from the other stakeholders into a single document in priority order. Note which stakeholders asked for each feature. The document should be in markdown format and should be ready for publication. Please use a table to visually organize the feedback.""",
            verbose=True,
            max_iter=5,
            allow_delegation=False,
            callbacks=callbacks
        )
