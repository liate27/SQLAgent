import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.utilities import SQLDatabase
from langchain_openai import OpenAI
from langchain.agents import create_sql_agent

def get_answer(prompt):
    # define the database we want to use for our test
    db = SQLDatabase.from_uri('sqlite:///sql_lite_database.db')

    # choose llm model, in this case the default OpenAI model
    llm = OpenAI(
                temperature=0,
                verbose=True,
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                                )
    # setup agent
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    result =  agent_executor.invoke(prompt)
    return result

st.title('SQL Agent At Your Service')
# Initialize chat history
if "messages" not in st.session_state:
   st.session_state.messages = []



if prompt := st.chat_input("Ask me anything about the database?"):
   # Display user message in chat message container
   with st.chat_message("user"):
       st.markdown(prompt)

   response = get_answer(prompt)

   with st.chat_message("assistant"):
       st.markdown(response)


