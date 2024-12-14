import math
import random


# Function to build a concept graph
def build_concept_graph(extraction_data):
    graph = {}  # Use a plain dictionary to store weights
    node_type_map = {}

    # Build the graph structure based on the extracted data
    for data in extraction_data:
        topics = data.get("topics", [])
        knowledge_points = data.get("knowledge_points", [])

        # Set node types for each topic and knowledge point
        for topic in topics:
            node_type_map[topic] = "topic"
        for kp in knowledge_points:
            node_type_map[kp] = "knowledge_point"

        # Create links and calculate weights based on co-occurrence
        for i in range(len(topics)):
            for j in range(i + 1, len(topics)):
                if topics[i] not in graph:
                    graph[topics[i]] = {}
                if topics[j] not in graph:
                    graph[topics[j]] = {}
                graph[topics[i]][topics[j]] = graph[topics[i]].get(topics[j], 0) + 1
                graph[topics[j]][topics[i]] = graph[topics[j]].get(topics[i], 0) + 1
            for kp in knowledge_points:
                if topics[i] not in graph:
                    graph[topics[i]] = {}
                if kp not in graph:
                    graph[kp] = {}
                graph[topics[i]][kp] = graph[topics[i]].get(kp, 0) + 1
                graph[kp][topics[i]] = graph[kp].get(topics[i], 0) + 1
        for i in range(len(knowledge_points)):
            for j in range(i + 1, len(knowledge_points)):
                if knowledge_points[i] not in graph:
                    graph[knowledge_points[i]] = {}
                if knowledge_points[j] not in graph:
                    graph[knowledge_points[j]] = {}
                graph[knowledge_points[i]][knowledge_points[j]] = graph[knowledge_points[i]].get(knowledge_points[j],
                                                                                                 0) + 1
                graph[knowledge_points[j]][knowledge_points[i]] = graph[knowledge_points[j]].get(knowledge_points[i],
                                                                                                 0) + 1

    # Apply logarithmic transformation to calculate edge weights
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            graph[node][neighbor] = math.log(graph[node][neighbor] + 1e-5)

    return graph, node_type_map


# Function to perform random walk sampling on the graph
def random_walk_sampling(graph, node_type_map, start_node):
    sampled_nodes = [start_node]
    current_node = start_node
    node_type = node_type_map[current_node]
    visited_nodes = set(sampled_nodes)  # Track visited nodes
    remaining_steps = {
        'topic': random.randint(1, 2),  # Steps on the topic subgraph
        'mixed': 1,  # Steps on the mixed graph
        'knowledge_point': random.randint(0, 4)  # Steps on the knowledge point subgraph
    }

    # Walk on the topic subgraph for 1-2 steps
    while remaining_steps['topic'] > 0:
        if current_node not in graph or not graph[current_node]:
            break
        neighbors = [(neighbor, weight) for neighbor, weight in graph[current_node].items() if
                     neighbor not in visited_nodes]
        if not neighbors:
            break
        total_weight = sum(math.exp(weight) for _, weight in neighbors)
        probabilities = [math.exp(weight) / total_weight for _, weight in neighbors]
        next_node = random.choices([neighbor for neighbor, _ in neighbors], probabilities)[0]
        sampled_nodes.append(next_node)
        visited_nodes.add(next_node)
        current_node = next_node
        node_type = node_type_map[current_node]
        remaining_steps['topic'] -= 1

    # Walk on the mixed graph for 1 step
    if node_type == "topic" and remaining_steps['mixed'] > 0:
        kp_neighbors = [(kp, graph[current_node][kp]) for kp in node_type_map if
                        node_type_map[kp] == "knowledge_point" and kp in graph[
                            current_node] and kp not in visited_nodes]
        if kp_neighbors:
            total_weight = sum(math.exp(weight) for _, weight in kp_neighbors)
            probabilities = [math.exp(weight) / total_weight for _, weight in kp_neighbors]
            next_node = random.choices([kp for kp, _ in kp_neighbors], probabilities)[0]
            sampled_nodes.append(next_node)
            visited_nodes.add(next_node)
            current_node = next_node
            remaining_steps['mixed'] -= 1

    # Walk on the knowledge point subgraph for 0-4 steps
    while remaining_steps['knowledge_point'] > 0:
        if current_node not in graph or not graph[current_node]:
            break
        kp_neighbors = [(neighbor, weight) for neighbor, weight in graph[current_node].items() if
                        neighbor not in visited_nodes]
        if not kp_neighbors:
            break
        total_weight = sum(math.exp(weight) for _, weight in kp_neighbors)
        probabilities = [math.exp(weight) / total_weight for _, weight in kp_neighbors]
        next_node = random.choices([neighbor for neighbor, _ in kp_neighbors], probabilities)[0]
        sampled_nodes.append(next_node)
        visited_nodes.add(next_node)
        current_node = next_node
        remaining_steps['knowledge_point'] -= 1

    return sampled_nodes
