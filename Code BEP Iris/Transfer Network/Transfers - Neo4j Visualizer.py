from py2neo import Graph
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# Obtain transfer data using query
# This query contains all data
query = """
MATCH (c1:Club)-[r:TRANSFERRED_TO]->(c2:Club)
RETURN c1.name AS from_club, c1.country AS from_country, 
       c2.name AS to_club, c2.country AS to_country,
       r.name AS player_name, r.age AS age, r.nationality AS nationality, 
       r.position AS position, r.market_value AS market_value, 
       r.fee AS fee, r.year AS year
"""

# To obtain a sub graph that shows only the years 2022 and 2023 with players aged 22 for better understanding
# query = """
# MATCH (c1:Club)-[r:TRANSFERRED_TO]->(c2:Club)
# WHERE r.age = '22' AND r.year = '2022' OR r.year = '2023'
# RETURN c1.name AS from_club, c1.country AS from_country, 
#        c2.name AS to_club, c2.country AS to_country,
#        r.name AS player_name, r.age AS age, r.nationality AS nationality, 
#        r.position AS position, r.market_value AS market_value, 
#        r.fee AS fee, r.year AS year
# """

# Run the query
results = graph.run(query)

# Create a Pyvis Network instance
net = Network(notebook=True)

# Define colors for edges based on year
year_colors = {
    '1992': 'magenta',
    '1993': 'yellow',
    '1994': 'black',
    '1995': 'pink',
    '1996': 'olive',
    '1997': 'gold',
    '1998': 'navy',
    '1999': 'teal',
    '2000': 'maroon',
    '2001': 'lime',
    '2002': 'aqua',
    '2003': 'fuchsia',
    '2004': 'silver',
    '2005': 'chocolate',
    '2006': 'coral',
    '2007': 'crimson',
    '2008': 'darkblue',
    '2009': 'darkgreen',
    '2010': 'darkred',
    '2011': 'darkcyan',
    '2012': 'darkmagenta',
    '2013': 'darkorange',
    '2014': 'darkviolet',
    '2015': 'deeppink',
    '2016': 'khaki',
    '2017': 'plum',
    '2018': 'purple', 
    '2019': 'orange',
    '2020': 'cyan',
    '2021': 'lavender',
    '2022': 'blue',
    '2023': 'red',
    '2024': 'brown',
}

# year_colors = {
#     '2022': 'blue',
#     '2023': 'red'
# }

# Iterate through the results and add nodes and edges to the network
for record in results:
    from_club = record['from_club']
    to_club = record['to_club']
    year = record['year']
    market_value = record['market_value']
    age = record['age']
    nationality = record['nationality']
    position = record['position']
    player_name = record['player_name']

    # Add clubs as nodes
    if record['from_country'] == 'England':
        net.add_node(from_club, color='green')
    else:
        net.add_node(from_club, color='grey')

    if record['to_country'] == 'England':
        net.add_node(to_club, color='green')
    else:
        net.add_node(to_club, color='grey')

    # Add transfer as edge
    edge_color = year_colors.get(year, 'black')  # Use predefined color for the year, default to black
    edge_title = f"Player: {player_name}\nAge: {age}\nNationality: {nationality}\nPosition: {position}\nYear: {year}\nMarket Value: {market_value}"
    edge_width = float(market_value[1:-1]) / 10 if market_value != "-" else 1 # Adjust thickness based on market value
    #net.add_edge(from_club, to_club, value=edge_width, title=record['player_name'], arrows='to')
    net.add_edge(from_club, to_club, value=edge_width, title=edge_title, color=edge_color, arrows='to')

    # Adjusting the height and width of the visualization window
    net.height = '1000px'
    net.width = '2000px'

# Show the network
net.show("Transfers - Neo4j Property Graph.html")
