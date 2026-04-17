from langchain_openai import ChatOpenAI
from langchain_core import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tool import web_search, web_scrape
from dotenv import load_dotenv
import os
load_dotenv()

#model setup
llm = ChatOpenAI(model="gpt-40-mini",temperature=0)

#agent1
def search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

#agent2
def reader_agent():
    return create_agent(
        model=llm,
        tools=[web_scrape]
    )

#creating chain

#chain1 writer
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that writes a comprehensive report on the given topic using the provided information."),
    ("human", """Write a comprehensive report on the topic: {topic}
     
     research={content}

Structure the report as:
1. Introduction
2. Main Content
3. Conclusion
4. References or sources (list all URLs used in the report)

The tone should be professional and the content should be reliable.
"""),
])


writer_chain=writer_prompt | llm | StrOutputParser()


critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that critiques the given report and provides suggestions for improvement."),
    ("human", """Review the following report and provide constructive feedback on how to improve it. Focus on the clarity, coherence, and depth of the content. Also, suggest any additional information or sources that could enhance the report."""
    ),

])
critic_chain=critic_prompt | llm | StrOutputParser()