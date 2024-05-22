import streamlit as st
from handler import MyCustomHandler
from crewai import Crew, Process, Agent, Task
from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict, Optional
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()



writer = Agent(
    role='Blog Post Writer',
    backstory='''You are a blog post writer who is capable of writing a travel blog.
                      You generate one iteration of an article once at a time.
                      You never provide review comments.
                      You are open to reviewer's comments and willing to iterate its article based on these comments.
                      ''',
    goal="Write and iterate a decent blog post.",
    # tools=[]  # This can be optionally specified; defaults to an empty list
    llm=llm,
    callbacks=[MyCustomHandler("Writer")],
)
reviewer = Agent(
    role='Blog Post Reviewer',
    backstory='''You are a professional article reviewer and very helpful for improving articles.
                 You review articles and give change recommendations to make the article more aligned with user requests.
                 You will give review comments upon reading entire article, so you will not generate anything when the article is not completely delivered. 
                  You never generate blogs by itself.''',
    goal="list builtins about what need to be improved of a specific blog post. Do not give comments on a summary or abstract of an article",
    # tools=[]  # Optionally specify tools; defaults to an empty list
    llm=llm,
    callbacks=[MyCustomHandler("Reviewer")],
)

st.title("💬 Project Olympus") 

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "What is your product idea?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    task1 = Task(
      description=f"""Write a blog post of {prompt}. """,
      agent=writer,
      expected_output="an article under 300 words."
    )

    task2 = Task(
      description="""list review comments for improvement from the entire content of blog post to make it more viral on social media""",
      agent=reviewer,
      expected_output="Builtin points about where need to be improved."
    )
    # Establishing the crew with a hierarchical process
    project_crew = Crew(
        tasks=[task1, task2],  # Tasks to be delegated and executed under the manager's supervision
        agents=[writer, reviewer],
        manager_llm=llm,
        process=Process.hierarchical  # Specifies the hierarchical management approach
    )
    final = project_crew.kickoff()

    result = f"## Here is the Final Result \n\n {final}"
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result)