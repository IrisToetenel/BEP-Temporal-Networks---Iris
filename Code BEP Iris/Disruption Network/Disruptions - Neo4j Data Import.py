import pandas as pd
import numpy as np
from neo4j import GraphDatabase

df = pd.read_pickle("\Data\disruptions.pkl")

# Add a column for the total time of each disruption in minutes
def convert_to_minutes(duration):
    total_minutes = 0
    parts = duration.split(', ')
    for part in parts:
        if 'hour' in part:
            total_minutes += int(part.split()[0]) * 60
        elif 'minute' in part:
            total_minutes += int(part.split()[0])
    return total_minutes

df['total_time_minutes'] = df['total_time'].apply(convert_to_minutes)

# Transform the coordinates to a tuple
df["begin_coordinates"] = [(c[0],c[1]) if c!=None else np.nan for c in df["begin_coordinates"]]
df["eind_coordinates"] = [(c[0],c[1]) if c!=None else np.nan for c in df["eind_coordinates"]]

# Filter the columns
filtered_cols = [
    'data_key', 'date', 'reason', 'start_time', 'end_time', 'total_time', 'HSL',
    'begin_station', 'eind_station', 'begin_coordinates', 'eind_coordinates',
    'total_time_minutes'
]
df = df[filtered_cols].copy()

# Drop NaN values and reset the index
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password3"

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def close_driver(driver):
    driver.close()

# Helper functions
def create_station_nodes(tx, station_name, coords):
    query = (
        "MERGE (s:Station {name: $name}) "
        "SET s.coordinates = $coords"
    )
    tx.run(query, name=station_name, coords=coords)

def create_disruption_relationship(tx, begin_station, eind_station, data_key, reason, date, start_time, end_time, total_time, HSL, total_time_minutes):
    query = (
        "MATCH (b:Station {name: $begin_station}), (e:Station {name: $eind_station}) "
        "MERGE (b)-[r:DISRUPTION {data_key: $data_key, reason: $reason, date: $date, start_time: $start_time, end_time: $end_time, total_time: $total_time, HSL: $HSL, total_time_minutes: $total_time_minutes}]->(e)"
    )
    tx.run(query, begin_station=begin_station, eind_station=eind_station, data_key=data_key, reason=reason, date=date, start_time=start_time, end_time=end_time, total_time=total_time, HSL=HSL, total_time_minutes=total_time_minutes)

# Load the data into Neo4j
# Extract unique stations
stations = pd.concat([df[['begin_station', 'begin_coordinates']], df[['eind_station', 'eind_coordinates']].rename(columns={'eind_station': 'begin_station', 'eind_coordinates': 'begin_coordinates'})]).drop_duplicates()

# Create nodes
with driver.session() as session:
    for _, row in stations.iterrows():
        session.execute_write(create_station_nodes, row['begin_station'], row['begin_coordinates'])

# Create relationships with additional properties
with driver.session() as session:
    for _, row in df.iterrows():
        session.execute_write(create_disruption_relationship, 
                                  row['begin_station'], row['eind_station'], 
                                  row['data_key'], row['reason'], 
                                  row['date'], row['start_time'], 
                                  row['end_time'], row['total_time'], 
                                  row['HSL'], row['total_time_minutes'])

# Close the driver connection
close_driver(driver)
