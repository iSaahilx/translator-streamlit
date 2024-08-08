import streamlit as st
import os
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

openapi_key = st.secrets.get("OPENAI_API_KEY")
if not openapi_key:
    logging.error("OPENAI_API_KEY is not set in Streamlit secrets")
    st.error("OPENAI_API_KEY is not set. Please set it in your Streamlit secrets.")
else:
    os.environ['OPENAI_API_KEY'] = openapi_key


llm = ChatOpenAI(model="gpt-4o", temperature=0)


def translate(input_language, output_language, input_text):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert translator that translates {input_language} to {output_language}."),
            ("human", "{input}")
        ]
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "input_language": input_language,
            "output_language": output_language,
            "input": input_text
        }
    )

    return response.content
