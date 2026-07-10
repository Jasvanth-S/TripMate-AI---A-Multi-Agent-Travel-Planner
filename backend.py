import json

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

from psycopg.rows import dict_row
import psycopg
import re

from typing import TypedDict, Annotated
import operator
import uuid
import os

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, AnyMessage
from langchain_groq import ChatGroq

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights

# Get Database URL
def get_database_url():
    Database_url = os.getenv("DATABASE_URL")

    if not Database_url:
        raise ValueError("Database URL is not Set in the ENV configuration.")
    
    if "sslmode=" not in Database_url:
        separator = '&' if '?' in Database_url else '?'
        database_url = f"{Database_url}{separator}sslmode=require"

    return database_url


Groq = os.getenv("GROQ_API_KEY")

if not Groq:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    api_key = Groq
)

class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int

def flight_agent(state: TravelState):
    print("\n========== Flight Agent ==========")
    print(state)

    query = state["user_query"]
    flight_results = search_flights(query)

    return {
        "flight_results": flight_results,
        "messages": [AIMessage(content="Flight results Fetched!")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }

def hotel_agent(state: TravelState):
    print("\n========== Hotel Agent ==========")
    print(state)

    query = f"best hotels for state({state['user_query']}) "
    hotel_results = tavily_search(query)

    return {
        "hotel_results": hotel_results,
        "messages": [AIMessage(content="Hotel results Fetched!")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }

def itinerary_agent(state: TravelState):
    print("\n========== Itinerary Agent ==========")
    print(state)

    prompt = f"""
        You are a travel agent. You have been given the following information about a user's travel plans:
        User Query: {state['user_query']}
        Flight Results: {state['flight_results']}
        Hotel Results: {state['hotel_results']}
        make itinerary practical, budget aware and easy to follow. Provide a day-wise breakdown of the itinerary, including suggested activities, sightseeing spots, and any other relevant information. Ensure that the itinerary is well-structured and provides a comprehensive travel plan for the user."""

    response = llm.invoke([
        SystemMessage(content="You are a expert World Class Travel Planner"),
        HumanMessage(content=prompt),
    ])

    return {
        "itinerary": response.content,
        "messages": [AIMessage(content="Itinerary Generated!")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }

def final_agent(state: TravelState):
    print("\n========== Final Agent ==========")
    print(state)

    final_prompt = f"""
        Generate the final travel response for the user.

        User Request:
        {state['user_query']}

        Flights:
        {state['flight_results']}

        Hotels:
        {state['hotel_results']}

        Itinerary:
        {state['itinerary']}

        Format the final answer beautifully using these sections:

        1. Trip Summary
        2. Flight Information
        3. Hotel Suggestions
        4. Day-by-Day Itinerary
        5. Estimated Budget
        6. Final Recommendations

        Important:
        - Be clear and practical.
        - Mention that live flight API may not provide ticket prices if pricing is unavailable.
        - Keep the response useful for real travel planning.
    """

    response = llm.invoke([
        SystemMessage(content="You are a professional AI travel booking assistant."),
        HumanMessage(content=final_prompt),
    ])

    print(response)
    print(type(response))
    print(response.content)

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }




# ---------------------------------------------------------------------
# Graph State Definition
#---------------------------------------------------------------------

graph = StateGraph(TravelState)

graph.add_node("Flight_Agent", flight_agent)
graph.add_node("Hotel_Agent", hotel_agent)
graph.add_node("Itinerary_Agent", itinerary_agent)
graph.add_node("Final_Agent", final_agent)

graph.add_edge(START, "Flight_Agent")
graph.add_edge("Flight_Agent", "Hotel_Agent")
graph.add_edge("Hotel_Agent", "Itinerary_Agent")
graph.add_edge("Itinerary_Agent", "Final_Agent")
graph.add_edge("Final_Agent", END)

 # postgres Checkpoint

URL = get_database_url()

__conn = psycopg.connect(
    URL,
    autocommit = True, 
    row_factory=dict_row
)

check_pointer = PostgresSaver(__conn)
check_pointer.setup()

travel_graph = graph.compile(checkpointer=check_pointer)

## Function for FASTAPI

def run_travel_agent(user_query: str, thread_id: str | None = None):
    if not thread_id:
        thread_id = f"user_{uuid.uuid4().hex}"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = travel_graph.invoke({
        "messages": [HumanMessage(content=user_query)],
        "user_query": user_query,
        "flight_results": "",
        "hotel_results": "",
        "itinerary": "",
        "llm_calls": 0
    }, 
    config=config)

    print("=" * 100)
    print(result)
    print(type(result))
    print(result.keys())
    print("=" * 100)

    messages = result.get("messages", [])

    if messages:
        final_answer = messages[-1].content
    else:
        final_answer = "No response generated."

    return {
        "thread_id": thread_id,
        "answer": final_answer,
        "flight_results": result.get("flight_results", ""),
        "hotel_results": result.get("hotel_results", ""),
        "itinerary": result.get("itinerary", ""),
        "llm_calls": result.get("llm_calls", 0),
    }