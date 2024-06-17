import pandas as pd
from py2neo import Graph, Node, Relationship

# Load the pickle file into a dataframe
df = pd.read_pickle("\Data\transfer.pkl")

# Connect to neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
# graph

# Create nodes and relationships and add them to graph
# Function to create or get a club node
def get_or_create_club(club_name, country):
    club_node = graph.nodes.match("Club", name=club_name, country=country).first()
    if not club_node:
        club_node = Node("Club", name=club_name, country=country)
        graph.create(club_node) 
    return club_node
    
# Create nodes and relationships
for _, row in df.iterrows():
    # Get or create 'left' club node
    left_club_name, left_club_country = row['Left']
    left_club_node = get_or_create_club(left_club_name, left_club_country)
    
    # Get or create 'joined' club node
    joined_club_name, joined_club_country = row['Joined']
    joined_club_node = get_or_create_club(joined_club_name, joined_club_country)
    
    # Create the player transfer relationship
    transfer = Relationship(left_club_node, "TRANSFERRED_TO", joined_club_node,
                            name=row['Name'],
                            age=row['Age'],
                            nationality=row['Nationality'],
                            position=row['Position'],
                            market_value=row['Market value'],
                            fee=row['Fee'],
                            year=row['Year'])
    graph.create(transfer)
