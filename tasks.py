from datetime import datetime
from crewai import Task


class AIAPTasks():
    def research_task(self, agent, productidea):
        return Task(
            description=f'Review the new product idea: {productidea} and give unique insight for how to improve it. Give specific ideas for what to add or change for the product to be successful in a Accounts Payable workflow using your unique perspective. Provide a single suggestion for a name for the new product.',
            agent=agent,
            async_execution=True, 
            expected_output=""""A well-written list of feedback and insight. "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs."
            """
        )

    def analyze_task(self, agent, context):
        return Task(
            description='Analyze all feedback and check for errors or grammar issues.',
            agent=agent,
            async_execution=True, 
            context=context, # This task depends on the output of the research_task
            expected_output=""""A well-written list of feedback and insight. "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs."
            """
        )

    def compile_results_task(self, agent, context, callback_function):
        return Task(
            description='Compile the summary',
            agent=agent,
            context=context,
            expected_output="""A complete summary in markdown format, with a consistent style and layout. List out each agents ideas and feedback in a clear and concise manner.""",
            callback=callback_function # This task requires a callback function to save the markdown output
        )
