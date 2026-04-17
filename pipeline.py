from agents import search_agent, reader_agent, writer_chain, critic_chain

def research_pipeline(topic : str):
    state={}

    search_agent=search_agent()
    search_result=search_agent.invoke({
        "message": f"Search the web for recent and reliable information on the topic: {topic}"
    })
    state["search_results"]=search_result['message'][-1].content
    print("Search Results:\n",state["search_results"])

    reader_agent=reader_agent()
    reader_result=reader_agent.invoke({
        "message": [{"user" f"Extract the URLs from the search results and scrape the content of each URL. Summarize the content for better reading."
        f"\nSearch Results:\n{state['search_results'][:900]}"
        }]


    })
    state["scraped_content"]=reader_result['message'][-1].content
    print("Scraped Content:\n",state["scraped_content"])


    writer_result=writer_chain.invoke({
        "topic": topic,
        "content": state["scraped_content"]
        

    })

    state["report"]=writer_result
    print("Generated Report:\n",state["report"])

    critic_result=critic_chain.invoke({
        "report": state["report"]       
    })
    state["critique"]=critic_result
    print("Critique:\n",state["critique"])
    return state


if __name__=="__main__":
    topic=input("Enter the research topic: ")
    research_pipeline(topic)






