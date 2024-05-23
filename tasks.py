from datetime import datetime
from crewai import Task

class AIAPTasks():
    def research_task(self, agent, prompt, feature_num = 3):
        return Task(
            description=f'Please evaluate the product idea "{prompt}"and provide feedback on what your needs are in your role. Make a subtle joke if the product idea does not seem to be related to AP. Please list the top {feature_num} features that would specifically help with your job. Also list your top {feature_num} concerns.',
            agent=agent,
            async_execution=True, 
            expected_output="""
            "A well-written list of feedback and insight."
            "In markdown format, ready for publication, "
            "each section should have 1 or 2 paragraphs."
            "Provide a list of very specific features that would help you specifically with your job, and a list of concerns.
            "Incorporate some of your backstory as to why these features are important to you specifically."
            "Provide a potential product name for the idea.
            """
        )
        
    def compile_results_task(self, agent, context, callback_function):
        return Task(
            description='Compile the output from all agents into markdown format. Use a table to visually organize the feedback organized by feature. Do not enclose the output in triple backticks.',
            agent=agent,
            context=context,
            expected_output="""A complete summary in markdown format, with a consistent style and layout.
                               """,
            callback=callback_function, # This task requires a callback function to save the markdown output
            human_input=False
        )


