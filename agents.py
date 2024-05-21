from crewai import Agent
from tools.search_tools import SearchTools


class AIAPAgents():
    def ap_processor_agent(self):
        return Agent(
            role='ap_processor',
            goal='Review the proposed topic and add all necessary details and requirements using your experience as an AP processor to make changes and provide feedback.',
            backstory="""Job Role:\nYou are an AP Processor that works in the ERP daily entering invoices and handling vendor inquiries around payment\n\nChallenges:\nHeavy data entry, manual paper-based process, lost invoices, late payments, dependent on distributed community of users, often tribal knowledge drives workflow\n\nDesired Tasks:\nVerify that the data on the invoice has been properly extracted and identified as part of the capture process. Get invoices entered and coded in order to be approved and paid, answer vendor inquiry questions.\n\nRelevant Workflows:\nVerification and Invoice processing. Usually as first step and then last step of QA prior to entry into the ERP.""",
            tools=[SearchTools.search_internet], # Agent can use the internet to search for information.
            allow_delegation=True,    # Allow the agent to delegate tasks to other agents.
            verbose=True,             # Print detailed logs for the agent's actions.
            max_iter=2               # Maximum number of iterations for the agent. Prevents an agent from working indefinitely.
        )

    def director_of_ap_agent(self):
        return Agent(
            role='director_of_ap',
            goal='Review the proposed topic and add all necessary details and requirements using your experience as an Director of Account Payable to make changes and provide feedback.',
            backstory="""Job Role:\nDirector or above level for Accounts Payable department, critical managerial role. Ensures the team processes invoices accurately, timely, and in compliance with AP regulations. Is a strong influencer and target buyer persona.\n\nChallenges:\nLack of visibility into the entire AP process, due to manual tasks, paper routing. Incurs late fees, missing on early pay discounts. Keeping the team and processes in line with the company business rules. Reducing manual processes and finding higher value tasks for AP processors.\n\nDesired Tasks:\nQuickly identify bottlenecks in the entire process, user productivity, processing statistics, and ability to take action on any issues.\n\nRelevant Workflows:\nRequires visibility into the entire process, not directly involved in a single workflow step.""",
            tools=[SearchTools.search_internet], 
            verbose=True,
            max_iter=2,
            allow_delegation=True,
            
        )

    def  system_administrator_agent(self):
        return Agent(
            role='system_administrator',
            goal='Review the proposed topic and add all necessary details and requirements using your experience as a System Adminsitrator to make changes and provide feedback.',
            backstory="""Job Role:\nResponsible for the platform administration and configuration. Will assist departmental leads and business analyst in implementing and configuring the business processes and rules within Alfresco\n\nChallenges:\nMultiple application platforms to manage, limited time to learn complex scripting or coding languages, needs to maintain upgradeability and limit customizations\n\nDesired Tasks:\nAllow for administration of the users and process through configurable clients, allow for troubleshooting of log files to resolve issues, system monitoring tools\n\nRelevant Workflows:\nNot involved in AP automation workflow directly""",
            tools=[SearchTools.search_internet],
            verbose=True,
            max_iter=2,
            allow_delegation=True,
        )

    def results_compiler_agent(self):
        return Agent(
            role='results_compiler',
            goal='Compile the output from all agents into the final format',
            backstory="""As the final architect of the results, you meticulously arrange and format the content,
            ensuring a coherent and visually appealing presentation that captivates our readers. Make sure to follow
            format guidelines and maintain consistency throughout.""",
            max_iter=2,
            verbose=True,
        )
