from datetime import datetime
from crewai import Task

class AIAPTasks():
    def research_task(self, agent, prompt, feature_num = 3):
        return Task(
            description=f'Please evaluate the product idea "{prompt}"and provide feedback on what your needs are in your role. Please list the top {feature_num} features that would help with your job. Also list your top {feature_num} concerns.',
            agent=agent,
            async_execution=True, 
            expected_output="""
            "A well-written list of feedback and insight. "
            "in markdown format, ready for publication, "
            "each section should have 2 or 3 paragraphs."
            "Provide a list of features that would help with the job, and a list of concerns."
            "Provide a potential product name for the idea.
            """
        )
        
    def compile_results_task(self, agent, context, callback_function):
        return Task(
            description='Compile the output from all agents into the final format organized by feature',
            agent=agent,
            context=context,
            expected_output="""A complete summary in markdown format, with a consistent style and layout. Provide your response in machine readable output.
                               List out each agents ideas and feedback in a clear and concise manner.
                               You will need to compile the feedback from the other stakeholders into a single document in priority order. 
                               Note which stakeholders asked for each feature. The document must be in markdown format with no additional text. 
                               Please use a table to visually organize the feedback.""",
            callback=callback_function, # This task requires a callback function to save the markdown output
            human_input=False
        )
