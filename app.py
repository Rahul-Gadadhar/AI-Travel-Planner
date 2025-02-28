import streamlit as st
import json
import re
from travel_chain import create_travel_chain

st.set_page_config(page_title="AI Travel Planner", layout="wide")

def main():
    st.title("🌍 AI-Powered Travel Planner")
    
    st.markdown("""
    Enter your source and destination to get comprehensive travel options including:
    * 🚕 Cab services
    * 🚆 Trains
    * 🚌 Buses
    * ✈️ Flights
    """)

    col1, col2 = st.columns(2)
    with col1:
        source = st.text_input("Source Location")
    with col2:
        destination = st.text_input("Destination Location")

    if st.button("Find Travel Options", type="primary"):
        if source and destination:
            with st.spinner("Generating travel options..."):

                travel_chain = create_travel_chain()
                response = travel_chain.run(source=source, destination=destination)
                
                travel_data = extract_json(response)
                
                if travel_data:
                    display_travel_options(travel_data)
                else:
                    st.error("Could not parse JSON response. Please try again.")
                    with st.expander("Raw Response"):
                        st.text(response)
        else:
            st.warning("Please enter both source and destination.")

def extract_json(text):
    """Extract and parse JSON from text, handling common errors and markdown code blocks."""

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    code_block_pattern = r'```(?:json)?\s*([\s\S]*?)```'
    code_match = re.search(code_block_pattern, text)
    if code_match:
        try:
            json_str = code_match.group(1).strip()
            return json.loads(json_str)
        except:
            pass
        
    json_pattern = r'({[\s\S]*})'
    match = re.search(json_pattern, text)
    
    if match:
        try:
            json_str = match.group(1)
            json_str = json_str.replace("'", '"')
            json_str = re.sub(r'(\w+):\s*"', r'"\1": "', json_str)
            json_str = re.sub(r'(\w+):\s*\[', r'"\1": [', json_str)
            json_str = re.sub(r'(\w+):\s*{', r'"\1": {', json_str)
            json_str = re.sub(r'(\w+):\s*(\d+)', r'"\1": \2', json_str)
            return json.loads(json_str)
        except:
            pass
    
    return None

def display_travel_options(data):
    st.subheader("📍 Trip Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**From:** {data.get('source', 'Not available')}")
    with col2:
        st.info(f"**To:** {data.get('destination', 'Not available')}")
    
    if 'distance_km' in data:
        st.metric("Distance", f"{data.get('distance_km', 'Unknown')} km")
    
    st.subheader("🚀 Available Transport Options")
    
    if 'travel_options' in data and data.get('travel_options'):
        modes = [option.get('mode', f'Option {i+1}') for i, option in enumerate(data['travel_options'])]
        
        mode_emojis = {
            'Cab': '🚕',
            'Taxi': '🚕',
            'Car': '🚗',
            'Train': '🚆',
            'Bus': '🚌',
            'Flight': '✈️',
            'Airplane': '✈️'
        }
        
        tab_names = [f"{mode_emojis.get(mode, '🚀')} {mode}" for mode in modes]
        tabs = st.tabs(tab_names)
        
        for i, mode in enumerate(modes):
            with tabs[i]:
                option = data['travel_options'][i]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Cost Range", option.get('estimated_cost_range_inr', 'N/A'))
                    st.metric("Comfort Level", option.get('comfort_level', 'N/A'))
                with col2:
                    st.metric("Travel Time", f"{option.get('travel_time_hours', 'N/A')} hours")
                    st.metric("Frequency", option.get('frequency', 'N/A'))
                
                if 'notes' in option and option['notes']:
                    st.info(f"**Note:** {option['notes']}")
    
    if 'route_highlights' in data and data['route_highlights']:
        st.subheader("🏛️ Points of Interest")
        for highlight in data['route_highlights']:
            st.write(f"• {highlight}")

if __name__ == "__main__":
    main()