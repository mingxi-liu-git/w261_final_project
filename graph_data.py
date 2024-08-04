import csv
import json
import os
os.chdir("/Users/thebobs/Downloads/")

def parse_csv(file_path):
    data = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) == 2:
                airport_code, pagerank = row
                data[airport_code] = float(pagerank)
    return data

def parse_airport_csv(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def create_nodes_and_links(airport_data, pagerank_data):
    nodes = {}
    links = []
    
    for row in airport_data:
        origin = row['ORIGIN']
        dest = row['DEST']
        
        # Add nodes if they don't exist
        if origin not in nodes:
            nodes[origin] = {
                "id": origin, 
                "type": row['origin_type'],
                "pagerank": pagerank_data.get(origin, 0)  # Add PageRank value
            }
        if dest not in nodes:
            nodes[dest] = {
                "id": dest, 
                "type": row['dest_type'],
                "pagerank": pagerank_data.get(dest, 0)  # Add PageRank value
            }
        
        # Create link
        links.append({
            "source": origin,
            "target": dest,
            "year": int(row['YEAR']),
            "delay_count": int(row['delay_count'])
        })
    
    return list(nodes.values()), links

def generate_graph_json(nodes, links):
    graph = {
        "nodes": nodes,
        "links": links
    }
    return json.dumps(graph, indent=2)

# Main process
pagerank_file_path = 'pagerank.csv'
airport_csv_file_path = 'airport_network.csv'

pagerank_data = parse_csv(pagerank_file_path)
airport_data = parse_airport_csv(airport_csv_file_path)

nodes, links = create_nodes_and_links(airport_data, pagerank_data)
graph_json = generate_graph_json(nodes, links)

# Save the JSON to a file
output_file_path = 'airport_network_graph_with_pagerank.json'
with open(output_file_path, 'w') as json_file:
    json_file.write(graph_json)

print(f"JSON file with PageRank values saved as {output_file_path}")