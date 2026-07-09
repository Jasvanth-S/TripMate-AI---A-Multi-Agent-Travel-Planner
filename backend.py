from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

from psycopg.rows import dict_row
import psycopg

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
    message: Annotated[list[AnyMessage], operator.add]
    user_query:str
    flight_results: str
    hotel_results: str
    itenerary: str
    llm_call: int

def flight_agent(state: TravelState):
    query =  state["user_query"]
    flight_results = search_flights(query)

    return {
        "flights_results" :flight_results,
        "messages":[ AIMessage(content= "Flight results Fetched!") ],
        "llm_calls": state["llm_calls"] + 1
    }

def hotel_agent(state: TravelState):
    query = f"best hotels for state({state['user_query']}) "
    hotel_results = tavily_search(query)

    return {
        "hotel_search_results" : hotel_results,
        "messages":[ AIMessage(content= "Hotel results Fetched!") ],    
        "llm_calls": state["llm_calls"] + 1
    }


def itenerary_agent(State: TravelState):
    prompt = f"""
        You are a travel agent. You have been given the following information about a user's travel plans:
        User Query: {State['user_query']}   
        Flight Results: {State['flight_results']}
        Hotel Results: {State['hotel_results']}
        make itenerary practical, budget aware and easy to follow. Provide a day-wise breakdown of the itinerary, including suggested activities, sightseeing spots, and any other relevant information. Ensure that the itinerary is well-structured and provides a comprehensive travel plan for the user."""

    response = llm.invoke([
        SystemMessage(content = You are a expert World Class Travel Planner),
        HumanMessage(content = prompt)
         ])
    
    return {
        "itenerary" : response.content,
        "messages":[ AIMessage(content= "Itenerary Generated!") ],    
        "llm_calls": State["llm_calls"] + 1
    }
    

def final_agent(state: TravelState):
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
        HumanMessage(content=final_prompt)
    ])

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }




# ---------------------------------------------------------------------
# Graph State Definition
#---------------------------------------------------------------------

graph = StateGraph(TravelState)

graph.add_node("Flight_Agent", flight_agent)
graph.add_node("Hotel_Agent", hotel_agent)
graph.add_node("Iteneary_Agent", itenerary_agent)
graph.add_node("Final_Agent", final_agent)

graph.add_edge(START, "Flight_Agent")
graph.add_edge("Flight_Agent", "Hotel_Agent")
graph.add_edge("Hotel_Agent", "Iteneary_Agent")
graph.add_edge("Iteneary_Agent", "Final_Agent")
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

