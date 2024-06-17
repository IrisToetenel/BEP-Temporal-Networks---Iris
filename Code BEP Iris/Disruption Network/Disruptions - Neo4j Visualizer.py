from pyvis.network import Network
from neo4j import GraphDatabase
import pandas as pd
from collections import Counter

# Configuration for Neo4j connection
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password3"

def aggregate_edges(query):
    # Connect to Neo4j
    driver = GraphDatabase.driver(uri, auth=(username, password))
    edges = []

    with driver.session() as session:
        result = session.run(query)
        for record in result:
            edge = {
                "source": record["source"],
                "target": record["target"],
                "reason": record["reason"],
                "total_time_minutes": record["total_time_minutes"]
            }
            edges.append(edge)
    
    driver.close()
    return edges

def compute_aggregates(edges):
    df = pd.DataFrame(edges)
    # Group by source and target to compute aggregates
    aggregated = df.groupby(['source', 'target']).agg(
        avg_total_time_minutes=('total_time_minutes', 'mean'),
        disruption_count=('total_time_minutes', 'count'),
        most_frequent_reason=('reason', lambda x: Counter(x).most_common(1)[0][0])
    ).reset_index()
    return aggregated

def format_duration(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{int(hours)}h {int(mins)}m"

def visualize_edges(aggregated_edges, node_names):
    network = Network(height="100%", width="100%", notebook=False, directed=True)

    # Add nodes
    for node_id in node_names:
        network.add_node(node_id, label=str(node_id))

    # Add edges
    for _, edge in aggregated_edges.iterrows():
        avg_duration_str = format_duration(edge['avg_total_time_minutes'])
        edge_title = f"Average Duration: {avg_duration_str}\nMost Frequent Reason: {edge['most_frequent_reason']}"
        edge_width = edge['disruption_count']
        avg_total_time = edge['avg_total_time_minutes']

        # Determine color based on severity
        if avg_total_time < 30:
            edge_color = "green"
        elif avg_total_time < 60:
            edge_color = "orange"
        else:
            edge_color = "red"

        network.add_edge(
            edge['source'], edge['target'],
            value=edge_width,
            title=edge_title,
            color=edge_color,
            arrow='to'
        )

    # Adjusting the height and width of the visualization window
    network.height = '1000px'
    network.width = '2000px'

    # Show the network visualization
    network.set_edge_smooth('dynamic')
    network.show("Disruptions - Neo4j Property Graph.html", notebook=False)

# Query to retrieve all edges
query = """
    MATCH (a)-[r]->(b)
    RETURN a.name as source, b.name as target, r.reason as reason, r.total_time_minutes as total_time_minutes
"""

# Aggregate the data
edges = aggregate_edges(query)
node_names = {edge['source']: edge['source'] for edge in edges}
node_names.update({edge['target']: edge['target'] for edge in edges})
aggregated_edges = compute_aggregates(edges)

# Visualize the edges
visualize_edges(aggregated_edges, node_names)
