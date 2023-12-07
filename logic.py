import gradio as gr

class DecisionTreeNode:
    def __init__(self, name, probability, parent=None, gain=None):
        self.name = name
        self.probability = probability
        self.gain = gain
        self.children = []
        self.parent = parent

def build_decision_tree():
    root = DecisionTreeNode("Raiz", 1.0)

    def build_branch(node):
        num_branches_slider = gr.Slider(minimum=1, maximum=5, label=f"Cantidad de ramas para '{node.name}'")
        num_branches = num_branches_slider.value

        if num_branches == 0:
            branch_gain_slider = gr.Slider(minimum=0.0, maximum=1.0, label="Ganancia de la hoja")
            branch_gain = branch_gain_slider.value
            root.gain = branch_gain
            return  # Salir si no hay más ramas

        for _ in range(num_branches):
            all_parents = get_all_parents(node)
            branch_name_textbox = gr.Textbox(f"Nombre de la rama {node.name}/{'/'.join(all_parents)}")
            branch_probability_slider = gr.Slider(minimum=0.0, maximum=1.0, label="Probabilidad de la rama")
            branch_probability = branch_probability_slider.value
            if branch_probability == 0:
                branch_probability = 1.0

            branch_gain = 0.0

            branch_node = DecisionTreeNode(branch_name_textbox.value, branch_probability, parent=node, gain=branch_gain)
            node.children.append(branch_node)

            # Recursivamente construir las subramas
            build_branch(branch_node)

    build_branch(root)
    return root

def find_optimal_decision(node, parent_probability=1.0):
    if not node.children:
        total_probability = node.probability * parent_probability
        return node, total_probability + (node.gain or 0)  # Sumar la ganancia si está presente

    optimal_child = max(node.children, key=lambda x: x.probability)
    return find_optimal_decision(optimal_child, parent_probability=node.probability * parent_probability)

def get_all_parents(node):
    parents = []
    current_node = node
    while current_node.parent:
        parents.append(current_node.parent.name)
        current_node = current_node.parent
    return parents

# Construir el árbol de decisiones
decision_tree = build_decision_tree()

# Encontrar la opción más óptima
optimal_node, total_probability = find_optimal_decision(decision_tree)

# Obtener y mostrar todos los padres del nodo más óptimo
all_parents = get_all_parents(optimal_node)

print(f"La opción más óptima es: {optimal_node.name}/{'/'.join(all_parents)} con probabilidad {total_probability}")
