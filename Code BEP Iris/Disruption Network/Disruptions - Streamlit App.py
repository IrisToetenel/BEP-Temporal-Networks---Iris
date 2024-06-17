import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta

# Load and preprocess data
data = pd.DataFrame(pd.read_pickle("Data\disruptions.pkl"))
data = data.iloc[:1000].dropna().reset_index(drop=True).copy()
data["begin_coordinates"] = [[i[1], i[0]] for i in data["begin_coordinates"]]
data["eind_coordinates"] = [[i[1], i[0]] for i in data["eind_coordinates"]]

df = data.copy()
df['date'] = [d.date() for d in pd.to_datetime(df['date'])]

# Define a function to create the graph based on a selected date
def create_graph(selected_date):
    filtered_df = df[df['date'] == selected_date]
    G = nx.Graph()
    
    # Add nodes and edges
    for index, row in filtered_df.iterrows():
        G.add_node(row['begin_station'], pos=row['begin_coordinates'], station_name=row['begin_station'])
        G.add_node(row['eind_station'], pos=row['eind_coordinates'], station_name=row['eind_station'])
        G.add_edge(row['begin_station'], row['eind_station'], reason=row['reason'], date=row['date'])
    
    pos = nx.get_node_attributes(G, 'pos')
    edge_trace = []
    node_trace = []
    
    # Add edges first to ensure they are below nodes in the final plot
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(go.Scattermapbox(
            lon=[x0, x1, None],
            lat=[y0, y1, None],
            mode='lines',
            line=dict(width=2, color='blue'),
            text=edge[2]['reason'],
            hoverinfo='text',
            customdata=[edge[2]['reason']],
            name=f"{edge[0]} - {edge[1]}"
        ))
    
    # Add nodes
    for node in G.nodes():
        x, y = pos[node]
        node_trace.append(go.Scattermapbox(
            lon=[x],
            lat=[y],
            text=node,
            mode='markers',
            marker=dict(size=10),
            name=node,
            hoverinfo='text',
            customdata=[G.nodes[node]['station_name']]
        ))
    
    # Create the figure
    fig = go.Figure(data=edge_trace + node_trace)
    
    # Update layout for map display
    fig.update_layout(
        mapbox_style="open-street-map",
        width=500,
        height=500,
        margin=dict(l=5, r=5, b=5, t=5),
        mapbox=dict(
            center=go.layout.mapbox.Center(lat=52, lon=5.8),
            zoom=5.8,
        ),
        showlegend=False
    )
    
    # Adding interactivity
    for trace in fig.data:
        if trace.mode == 'markers':
            trace.hovertemplate = '<b>Station:</b> %{customdata}<extra></extra>'
        elif trace.mode == 'lines':
            trace.hovertemplate = '<b>Disruption Reason:</b> %{customdata}<extra></extra>'
    
    return fig

# set app title & Flavicon
st.set_page_config(page_title='NS Train Disruptions', layout='centered', page_icon="Disruptions - Streamlit NS Logo.png")


st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)


st.title("Train Disruptions Visualization")
key_nr=0

# Create placeholders for the slider and info display
slider_ph = st.empty()

# Initialize the datetime range and the initial value
unique_dates = df['date'].unique()
initial_value = min(unique_dates)
start_datetime = initial_value
end_datetime = max(unique_dates)

# Initialize session state variables for animation control
if 'animation' not in st.session_state:
    st.session_state.animation = False
if 'current_date' not in st.session_state:
    st.session_state.current_date = initial_value

# Create the slider and display the initial value
selected_date = slider_ph.slider("Select a Date", min_value=start_datetime, max_value=end_datetime, value=st.session_state.current_date, format="YYYY-MM-DD", key="initial_slider")

# Create graph for the selected date
fig = create_graph(selected_date)

# Display the graph
plot_ph = st.empty()
plot_ph.plotly_chart(fig, use_container_width=True)

# Animate button
animate_button_col, stop_button_col = st.columns([1, 1])  # Divide the available space into two columns
with animate_button_col:
    animate_button = st.button('Animate')

# Stop button
with stop_button_col:
    stop_button = st.button('Stop Animation')

# Handle the animate button click
if animate_button:
    st.session_state.animation = True

# Handle the stop button click
if stop_button:
    st.session_state.animation = False

# Animation loop
if st.session_state.animation:
    while st.session_state.animation:
        time.sleep(1)

        # Update the current date
        st.session_state.current_date += timedelta(days=1)

        # Reset the date if it exceeds the end date
        if st.session_state.current_date > end_datetime:
            st.session_state.current_date = initial_value

        # Update the slider and info display with a unique key
        selected_date = slider_ph.slider("Select a Date", min_value=start_datetime, max_value=end_datetime, value=st.session_state.current_date, format="YYYY-MM-DD", key=f"slider_{st.session_state.current_date}_{key_nr}")
        key_nr += 1

        # Update the graph
        fig = create_graph(st.session_state.current_date)
        plot_ph.plotly_chart(fig, use_container_width=True)
