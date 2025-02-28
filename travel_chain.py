import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain

load_dotenv()

def create_travel_chain():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2
    )
    
    travel_template = """
    You are an AI travel assistant. Based on the following source and destination, 
    provide travel options including cab, train, bus, and flights if applicable, 
    along with estimated costs and travel times.

    Source: {source}
    Destination: {destination}

    Respond with a structured JSON with the following format:
    {{
    "source": "Source City Name",
    "destination": "Destination City Name",
    "distance_km": approximate_distance_in_km,
    "travel_options": [
        {{
        "mode": "Transport Mode Name",
        "estimated_cost_range_inr": "Cost range in INR",
        "travel_time_hours": "Estimated time in hours",
        "frequency": "How often this transport is available",
        "comfort_level": "Low/Medium/High",
        "notes": "Additional information about this option"
        }}
    ],
    "route_highlights": [
        "Point of interest 1",
        "Point of interest 2"
    ]
    }}

    Ensure your response is valid JSON that can be parsed by Python's json.loads().
    """
    
    prompt = PromptTemplate(
        input_variables=["source", "destination"],
        template=travel_template
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return chain