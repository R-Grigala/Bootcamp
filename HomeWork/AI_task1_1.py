class Node:
    def __init__(self, state, action=None, parent=None):
        self.state = state  # მიმდინარე მდგომარეობა
        self.action = action  # მოქმედება
        self.parent = parent  # მშობელი წვერო
        self.family_tree = self._build_family_tree()  # გენეოლოგიური ხე

    def _build_family_tree(self):
        """გენეოლოგიური ხის აგება მშობელთა კავშირებით"""
        tree = []
        current_node = self
        while current_node:
            tree.append(current_node.state)  # წვეროს დამატება ხეში
            current_node = current_node.parent  # მშობელ წვეროზე გადასვლა
        return tree[::-1]  # ხის შემობრუნება

# Stack-based search space (LIFO)
class StackSpace:
    def __init__(self):
        self.stack = []  # სტექის ინიციალიზაცია

    def add(self, node):
        """წვეროს დამატება stack-ში"""
        self.stack.append(node)

    def remove(self):
        """stack-დან ბოლო ელემენტის ამოღება"""
        return self.stack.pop()

    def is_empty(self):
        """ამოწმებს, ცარიელია თუ არა stack"""
        return len(self.stack) == 0
    
    def contains_state(self, state):
        """შეამოწმებს, არის თუ არა მითითებული მდგომარეობა stack-ში"""
        return any(node.state == state for node in self.stack)

# Queue-based search space (FIFO)
class QueueSpace:
    def __init__(self):
        self.queue = []  # რიგის ინიციალიზაცია

    def add(self, node):
        """წვეროს დამატება queue-ში"""
        self.queue.append(node)

    def remove(self):
        """queue-დან პირველი ელემენტის ამოღება"""
        return self.queue.pop(0)

    def is_empty(self):
        """ამოწმებს, ცარიელია თუ არა queue"""
        return len(self.queue) == 0
    
    def contains_state(self, state):
        """შეამოწმებს, არის თუ არა მითითებული მდგომარეობა queue-ში"""
        return any(node.state == state for node in self.queue)

# Priority Queue-based search space
class PriorityQueueSpace:
    def __init__(self):
        self.priority_queue = [] # პრიორიტეტული რიგის ინიციალიზაცია

    def add(self, item):
        """წვეროს დამატება priority_queue-ში"""
        inserted = False
        for i in range(len(self.priority_queue)):
            if item[0] < self.priority_queue[i][0]:
                self.priority_queue.insert(i, item)
                inserted = True
                break
        if not inserted:
            self.priority_queue.append(item)

    def remove(self):
        """priority_queue-დან პირველი ელემენტის ამოღება"""
        if self.priority_queue:
            return self.priority_queue.pop(0)
        else:
            return None

    def is_empty(self):
        """ამოწმებს, ცარიელია თუ არა priority_queue"""
        return len(self.priority_queue) == 0
    
    def contains_state(self, state):
        """შეამოწმებს, არის თუ არა მითითებული მდგომარეობა priority queue-ში"""
        return any(item[1] == state for item in self.priority_queue)


# გრაფის მაგალითი
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['B'],
    'E': ['B', 'H'],
    'F': ['C', 'H'],
    'G': ['C'],
    'H': ['E', 'F']
}

# Search algorithms using the Node and Space classes

def depth_first_search(start, goal):
    stack_space = StackSpace()  # StackSpace კლასის ინიციალიზაცია
    stack_space.add(Node(state=start))  # საწყისი მდგომარეობის დამატება

    while not stack_space.is_empty():
        node = stack_space.remove()  # ბოლო წვეროს ამოღება
        print(f"Visiting Node: {node.state}, Path: {node.family_tree}")  # მონახულებული წვერო და გზა
        
        if node.state == goal:
            return node.family_tree  # გზის დაბეჭდვა
        
        for action in graph[node.state]:
            child_node = Node(state=action, action=action, parent=node)
            stack_space.add(child_node)

    return None


def breadth_first_search(start, goal):
    queue_space = QueueSpace()  # QueueSpace კლასის ინიციალიზაცია
    queue_space.add(Node(state=start))  # საწყისი მდგომარეობის დამატება

    while not queue_space.is_empty():
        node = queue_space.remove()  # პირველი წვეროს ამოღება
        print(f"Visiting Node: {node.state}, Path: {node.family_tree}")  # მონახულებული წვერო და გზა
        
        if node.state == goal:
            return node.family_tree  # გზის დაბეჭდვა
        
        for action in graph[node.state]:
            child_node = Node(state=action, action=action, parent=node)
            queue_space.add(child_node)

    return None

def a_stark_search(graph, start, goal, heuristic):
    frontier = PriorityQueueSpace()
    frontier.add((0, start))
    visited = set()
    parent = {start: None}  # Dictionary to keep track of the path
    path_cost = {start: 0}  # Dictionary to keep track of the cost of the path to each node

    while not frontier.is_empty():
        # Fetch the priority-node tuple and extract the node part
        priority_node_tuple = frontier.remove()
        current = priority_node_tuple[1]

        if current == goal:
            # Reconstruct the path from start to goal
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Return reversed path
        
        # If the node is already visited, skip it
        if current in visited:
            continue

        visited.add(current)

        for neighbor in graph[current]:
            # Update the path cost for the neighbor, in this case, path cost is always 1
            new_cost = path_cost[current] + 1
            if neighbor not in visited or new_cost < path_cost.get(neighbor, float('inf')):
                path_cost[neighbor] = new_cost
                total_cost = new_cost + heuristic.get(neighbor, 0)
                # print(total_cost)
                frontier.add((total_cost, neighbor))
                parent[neighbor] = current

    return None  # If the goal is not reachable


# DFS მაგალითი
print("DFS Path from A to G:")
dfs_path = depth_first_search('A', 'G')
print(f"DFS Result: {dfs_path}")  # DFS შედეგი

# BFS მაგალითი
print("\nBFS Path from A to G:")
bfs_path = breadth_first_search('A', 'G')
print(f"BFS Result: {bfs_path}")  # BFS შედეგი

# A* მაგალითი
# Example heuristic function values for each node to the goal (assuming goal is 'H')
heuristic = {
    'A': 3,
    'B': 2,
    'C': 2,
    'D': 3,
    'E': 1,
    'F': 3,
    'G': 3,
    'H': 0
}

print("\nA* Path from A to H:")
a_star = a_stark_search(graph, 'A', 'H', heuristic)
print(f"A* Result: {bfs_path}")  # A* შედეგი



"""
1. Stack (LIFO - Last In, First Out) სტრუქტურა განკუთვნილია იმ ალგორითმებისთვის,
სადაც უკანასკნელი შესული ცვლადი გამოდის პირველი - Last In, First Out. 
Stack გამოიყენება სიღრმიში ძებნის ალგგორითმში (Depth-First Search, DFS), სადაც ალგორითმი ჯერ ერთი მიმართულებით მოძრაობს, 
სანამ გრაფის ბოლოში არ მივა, შემდეგ უკან ბრუნდება და სხვა არა მონაულებულ გზას გადის.

2. Queue (FIFO - First In, First Out) სტრუქტურა განკუთვნილია იმ ალგორითმებისთვის,
სადაც პირველი დამატებული ცვლადი არის რიგში პირველი - First In, First Out
Queue სტრუქტურა განკუთვნილია სიგანეში ძებნისთვის (Breadth-First Search, BFS), 
ალგორითმი თანაბრად იკვლევს ყველა შესაძლო გზას, სანამ მიზანს არ მიაღწევს.

3. Priority Queue (პრიორიტეტული რიგი)
Priority Queue საშუალებას იძლევა, რომ წვეროებს მიენიჭოს პრიორიტეტი — ანუ წვეროები უფრო სწრაფად გადაიხედება, 
თუ ისინი უფრო "პერსპექტიულია". ეს სტრუქტურა ხშირად გამოიყენება A* -ის ალგორითმში, 
სადაც კვანძებს მინიჭებული აქვთ ფასი და ეურისტიკული შეფასებები.
"""