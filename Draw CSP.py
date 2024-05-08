import networkx as nx 
import matplotlib.pyplot as plt 

# Function to read input from the user
def input_read(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    N_V = int(lines.pop(0).strip())
    variables = lines.pop(0).strip().split()

    domains = {}
    for var in variables:
        domain = lines.pop(0).strip()
        domains[var] = list(map(int, domain.split()))

    N_UC = int(lines.pop(0).strip())
    unary_constraints = [lines.pop(0).strip() for _ in range(N_UC)]

    N_BC = int(lines.pop(0).strip())
    binary_constraints = [lines.pop(0).strip() for _ in range(N_BC)]

    return variables, domains, unary_constraints, binary_constraints

# Function to adjust domains based on unary constraints
def unary_adjust(variables, domains, unary_constraints):
    for constraint in unary_constraints:
        var, op, constant = constraint.split()
        constant = int(constant)
        if op == '<':
            domains[var] = [val for val in domains[var] if val < constant]
        elif op == '>':
            domains[var] = [val for val in domains[var] if val > constant]
        elif op == '=':
            domains[var] = [val for val in domains[var] if val == constant]

# Function to adjust domains based on binary constraints
def binary_adjust(variables, domains, binary_constraints):
    for constraint in binary_constraints:
        var1, arith_op, var2, op, constant = constraint.split()
        constant = int(constant)
        if arith_op == '+':
            if op == '>':
                domains[var1] = [val for val in domains[var1] if any(val > constant - val2 for val2 in domains[var2])]
            elif op == '<':
                domains[var1] = [val for val in domains[var1] if any(val < constant - val2  for val2 in domains[var2])]
        elif arith_op == '-':
            if op == '>':
                domains[var1] = [val for val in domains[var1] if any(val > val2 + constant for val2 in domains[var2])]
            elif op == '<':
                domains[var1] = [val for val in domains[var1] if any(val < val2 + constant for val2 in domains[var2])]

# Function to draw the constraint graph
def graph_draw(variables, domains, binary_constraints):
    G = nx.Graph()
    # Adding nodes (variables) to the graph with their domain values as labels
    for var, domain_values in domains.items():
        node_label = f"{var}\n{domain_values}"  # Combine variable name and domain values
        G.add_node(var, label=node_label)
    # Adding edges (binary constraints) to the graph with constraints as edge labels
    for constraint in binary_constraints:
        var1, op, var2, arith_op, constant = constraint.split()
        edge_label = f"{var1} {op} {var2} {arith_op} {constant}"  # Construct edge label from constraint
        G.add_edge(var1, var2, label=edge_label)
    # Layout algorithm to position the nodes
    pos = nx.spring_layout(G)
    # Drawing the graph with labels
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=12, font_weight='bold')
    # Adding node labels
    node_labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    # Adding edge labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()

# Main function
def main():
    variables, domains, unary_constraints, binary_constraints = input_read("D:/Syed Anser/AI/input.txt")
    print("Variables:", variables)
    print("Domains:", domains)
    print("Unary Constraints:", unary_constraints)
    print("Binary Constraints:", binary_constraints)

    # Adjusting domains based on unary constraints
    unary_adjust(variables, domains, unary_constraints)
    print("post unary adjustment:", domains)

    #pre binary adjustment graph
    graph_draw(variables, domains, binary_constraints)

    # Adjusting domains based on binary constraints
    binary_adjust(variables, domains, binary_constraints)
    print("post binary adjustment:", domains)

    # Post binary adjustment constraint graph
    graph_draw(variables, domains, binary_constraints)

if __name__ == "__main__":
    main()
