import networkx as nx
import itertools
import matplotlib.pyplot as plt

f = open("output.txt", "w")

# updated function to use networkx graph
def find_vertex_cover(G_nx, budget):
    f.write("\nGreedy vertex cover search\n")
    G = G_nx.copy()
    vertex_cover = set()

    while G.number_of_edges() > 0:
        # Select the node with the highest degree
        max_cover_node = max(G.nodes(), key=lambda x: G.degree[x])
        f.write(f"max_cover_node: {max_cover_node}\n")

        # Add node to the vertex cover
        vertex_cover.add(max_cover_node)
        f.write(f"vertex cover in progress: {vertex_cover}\n")

        # Remove all edges connected to the node
        covered_edges = list(G.edges(max_cover_node))
        f.write(f"Covered_edges: {covered_edges}\n")
        G.remove_edges_from(covered_edges)

        # Remove the node from the graph
        G.remove_node(max_cover_node)
        f.write(f"Remaining graph nodes: {list(G.nodes())}\n")

    if len(vertex_cover) > budget:
        f.write(f"Vertex cover is not optimal, it is {len(vertex_cover) - budget} bigger\n")
        print("Greedy Vertex Cover was not found within budget")
    else:    
        f.write(f"Greedy Vertex Cover found: {vertex_cover}\n")
        print("Greedy Vertex Cover found:" , vertex_cover)
    

    return vertex_cover

def is_vertex_cover(graph, vertex_cover):

    uncovered_edges = []
    # loop to check all the edges
    for u, v in graph.edges():
           # if neither endpoint of the edge is in the vertex cover, it's not a valid vertex cover
           if u not in vertex_cover and v not in vertex_cover:
            uncovered_edges.append((u,v))
    
    if uncovered_edges:
        f.write(f"The set:  {vertex_cover}  is not a vertex cover\n")
        f.write(f"The set has uncovered edges {uncovered_edges}\n")
        return False
    print("The set: ", vertex_cover, " is a vertex cover. ")
    print ("All edges covered\n")

    f.write(f"The set:  {vertex_cover}  is a vertex cover. ")
    f.write(f"All edges covered\n")
    return True

def minimum_vertex_cover_search(G, budget): # brute force approach to finding the minimum vertex cover by looping through all possible combinations of vertices, incrementing the size limit of a possible set in each iteration
    f.write("\nBrute force vertex cover search\n")
    # Get all nodes
    nodes = list(G.nodes())
    
    # Try all possible combinations of nodes
    for k in range(budget + 1):
        for candidate_set in itertools.combinations(nodes, k): # creates set containg nodes of length k in sorted order, no repeated elements
            # Check if this set is a vertex cover
            f.write(f"\nTrying vertex set: {set(candidate_set)}\n")
            if is_vertex_cover(G, set(candidate_set)):
                f.write(f"Found vertex cover Brute Force: {set(candidate_set)}  with budget: {k}\n")
                print("Found vertex cover using Brute Force:" , set(candidate_set),  "with budget: ",k,"\n")
                return set(candidate_set)
    print ("No Vertex cover is possible for budget: ", budget)
    return None

def visualize_graph(G, title, filename, highlight_nodes):
    #print ("highlight: ", highlight_nodes)
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)  # consistent layout
    
    # Draw all nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=300)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos)
    
    # Highlight specific nodes
    if highlight_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=list(highlight_nodes), node_color='red', node_size=400)
    # Draw labels
    nx.draw_networkx_labels(G, pos)
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()  # Close the plot to free up memory

# Function to verify if the hitting set is valid
def is_hitting_set(original_subsets, hitting_set):
    uncovered_subsets = []
    for subset in original_subsets:
        # Check if the subset has at least one element in the hitting set
        if not (subset & hitting_set):  # Intersection of subset and hitting_set
            uncovered_subsets.append(subset)
    
    if uncovered_subsets:
        f.write(f"The set: {hitting_set} is not a hitting set\n")
        f.write(f"The set has uncovered subsets: {uncovered_subsets}\n")
        return False
    print("The set: ", hitting_set, " is a hitting set. ")
    print("All subsets are hit\n")

    f.write(f"The set:  {hitting_set} is a hitting set. ")
    f.write(f"All subsets are hit\n")
    return True

def compute_element_frequencies(universe, remaining_subsets):
    freq = {elem: 0 for elem in universe}
    for subset in remaining_subsets:
        for elem in subset:
            if elem in freq:
                freq[elem] += 1
    return freq

def brute_force_hitting_set(universe, subsets, budget):
    f.write("\nBrute force Hitting set search\n")
    # Try all subsets of the universe in increasing order of size
    for r in range(budget + 1):
        for candidate in itertools.combinations(universe, r):
            candidate_set = set(candidate)
            f.write(f"\nTrying Hitting set: {(candidate_set)}\n")
            if is_hitting_set(subsets, candidate_set):
                f.write(f"Found Hitting set Brute Force: {(candidate_set)}  with budget: {r}\n")
                print("Found Hitting set using Brute Force:" , (candidate_set),  "with budget: ",r,"\n")
                return candidate_set
    print ("No Hitting set is possible for budget: ", budget)
    return set()  # No hitting set found (shouldn't happen for edge-based graphs)

def find_greedy_hitting_set(universe, subsets):
    f.write("\nGreedy Hitting set search\n")
    hitting_set = set()
    remaining_subsets = subsets.copy()
    while remaining_subsets:
        freq = compute_element_frequencies(universe, remaining_subsets)
        f.write(f"Element frequencies: {freq}\n")
        max_cover_element = max(freq, key=freq.get)
        f.write(f"Selected element: {max_cover_element}\n")
        hitting_set.add(max_cover_element)
        f.write(f"Hitting set in progress: {hitting_set}\n")
        remaining_subsets = [subset for subset in remaining_subsets if max_cover_element not in subset]
        f.write(f"Remaining subsets: {remaining_subsets}\n")
        universe.discard(max_cover_element)
        f.write(f"Remaining universe: {universe}\n")
    f.write(f"Greedy Hitting Set found: {hitting_set}\n")
    return hitting_set

budget = int(input("Enter integer budget: "))
f.write(f"Inputted budget is: {budget}\n")
input_file = "input.csv"

with open(input_file, 'r') as file:
    lines = file.readlines()
            
    # Separate edges and isolated vertices
    edges = []
    vertices = set()       
    for line in lines:
        nodes = list(map(int, line.strip().split(',')))
        if len(nodes) == 2:
            edges.append(tuple(nodes))  # Add as an edge
        elif len(nodes) == 1:
            vertices.add(nodes[0])  # Add as an isolated vertex

g = nx.Graph()
g.add_nodes_from(vertices)
g.add_edges_from(edges)

print("Graph nodes:", g.nodes(),"\n")
print("Graph edges:", g.edges(), "\n")

# Transform input 
# Step 1: Define the universe (vertices)
universe = set(g.nodes())
min_universe = universe.copy()

print("Universe:", universe, "\n")

# Step 2: Define the subsets (edges)
# Convert edges to subsets
subsets = [set(edge) for edge in edges]
print("Subsets (edges):", subsets, "\n")

# step 3: the budget for hitting set is the same as the budget given for vertex_cover (print this)
print("Brute force Vertex Cover result: \n")
min_vertex_cover = minimum_vertex_cover_search(g, budget)

# print("Greedy Vertex Cover result: \n")
# vertex_cover = find_vertex_cover(g, budget)
# if (is_vertex_cover(g, vertex_cover) == False):
#     print ("the set: ", vertex_cover, "is not a vertex cover")

visualize_graph(g, "Brute Force Vertex Cover Graph", "Brute_Force_Vertex_cover.png", min_vertex_cover)

# print("Greedy Htting set result: \n")
# greedy_hitting_set = find_greedy_hitting_set(universe, subsets)
# print("Greedy Hitting Set:", greedy_hitting_set)
# if (is_hitting_set(subsets, greedy_hitting_set)== False):
#     print ("the set: ", greedy_hitting_set, "is not a hitting_set")

# if(is_vertex_cover(g, greedy_hitting_set) == False):
#     print ("the set: ", greedy_hitting_set, "is not a vertex cover")

print("Brute Force Hitting Set result: \n")
optimal_hitting_set = brute_force_hitting_set(min_universe, subsets, budget)
if(is_vertex_cover(g, optimal_hitting_set) == False):
    print ("the set: ", optimal_hitting_set, "is not a vertex cover")
visualize_graph(g, "Brute Force Hitting Set Graph", "Brute_Force_Hitting_set.png", optimal_hitting_set)

# write out to a log the prints statements for vertex cover and hitting set
f.close()