import math
import random


# 构建概念图谱的函数
def build_concept_graph(extraction_data):
    graph = {}  # 使用普通的字典来存储权重
    node_type_map = {}

    # 根据提取的数据构建图谱结构
    for data in extraction_data:
        topics = data.get("topics", [])
        knowledge_points = data.get("knowledge_points", [])

        # 为每个主题和知识点设定节点类型
        for topic in topics:
            node_type_map[topic] = "topic"
        for kp in knowledge_points:
            node_type_map[kp] = "knowledge_point"

        # 基于共现关系创建链接并计算权重
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

    # 应用对数变换计算边的权重
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            graph[node][neighbor] = math.log(graph[node][neighbor] + 1e-5)

    return graph, node_type_map


# 在图谱上进行随机游走以采样概念的函数
def random_walk_sampling(graph, node_type_map, start_node):
    sampled_nodes = [start_node]
    current_node = start_node
    node_type = node_type_map[current_node]
    visited_nodes = set(sampled_nodes)  # 记录已访问的节点
    remaining_steps = {
        'topic': random.randint(1, 2),  # 主题子图上的步数
        'mixed': 1,  # 混合图上的步数
        'knowledge_point': random.randint(0, 4)  # 知识点子图上的步数
    }

    # 在主题子图上游走1-2步
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

    # 在混合图上游走1步
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

    # 在知识点子图上游走0-4步
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
