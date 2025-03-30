import json
import os
import pygame

class NavGraph:
    def __init__(self, json_files):
        self.vertices = {}  # Stores vertices from each file as {filename: [(x, y, name, is_charger)]}
        self.lanes = []  # Stores lane connections as [(start_pos, end_pos)]
        self.vertex_dict = {}  # Maps vertex index to (x, y) coordinates
        self.load_graphs(json_files)

    def load_graphs(self, json_files):
        """Loads navigation graphs from multiple JSON files."""
        base_path = os.path.join(os.path.dirname(__file__), "../../data/")

        for json_file in json_files:
            file_path = os.path.abspath(os.path.join(base_path, json_file))
            print(f"Attempting to open: {file_path}")  # Debugging output

            if not os.path.exists(file_path):
                print(f"Warning: {file_path} not found!")
                continue
            
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            level_data = data.get("levels", {}).get("level1", {})

            # Extract vertices
            vertices = []
            for index, vertex in enumerate(level_data.get("vertices", [])):
                if not isinstance(vertex, list) or len(vertex) < 3 or not isinstance(vertex[2], dict):
                    print(f"Error: Unexpected vertex format {vertex}, skipping.")
                    continue

                x, y, properties = vertex
                name = properties.get("name", f"V{index}")
                is_charger = properties.get("is_charger", False)
                vertices.append((x, y, name, is_charger))
                self.vertex_dict[index] = (x, y)  # Stores index-to-coordinate mapping
            
            # Extract lanes and store actual positions
            for lane in level_data.get("lanes", []):
                if isinstance(lane, list) and len(lane) >= 2:
                    start, end = lane[:2]
                    if start in self.vertex_dict and end in self.vertex_dict:
                        x1, y1 = self.vertex_dict[start]
                        x2, y2 = self.vertex_dict[end]
                        self.lanes.append((x1, y1, x2, y2))  # Store as a tuple for easy drawing
                    else:
                        print(f"Error: Lane {lane} refers to invalid vertices, skipping.")
                else:
                    print(f"Error: Unexpected lane format {lane}, skipping.")
            
            # Store vertices data per file
            self.vertices[json_file] = vertices

    def get_vertex_position(self, vertex_id):
        """Retrieves the (x, y) position for a given vertex ID."""
        return self.vertex_dict.get(vertex_id, None)  # Direct dictionary lookup
    
    def get_vertices(self):
        """Returns all vertices as a flat list."""
        return [vertex for vertices in self.vertices.values() for vertex in vertices]

    def get_vertex_dict(self):
        """Returns a mapping of {index: (x, y)} for quick access."""
        return self.vertex_dict

    def get_lanes(self):
        """Returns the list of lanes with (start_x, start_y, end_x, end_y)."""
        return self.lanes

    def display_graphs(self):
        """Prints all navigation graph data in a readable format."""
        print("\nNavigation Graph Summary")
        
        for file, vertices in self.vertices.items():
            print(f"\nGraph from `{file}`:")
            
            if not vertices:
                print("   No vertices found.")
            else:
                print("   Vertices (Format: Name [Charger] @ (x, y)):")
                for i, (x, y, name, is_charger) in enumerate(vertices):
                    charger_status = "Charger" if is_charger else ""
                    print(f"     {i + 1}. {name} {charger_status} @ ({x:.2f}, {y:.2f})")

        if not self.lanes:
            print("\n   No lanes found.")
        else:
            print("\n   Lanes (Connections between vertices):")
            for i, (x1, y1, x2, y2) in enumerate(self.lanes):
                print(f"     {i + 1}. ({x1:.2f}, {y1:.2f}) <--> ({x2:.2f}, {y2:.2f})")

        print("\nFinished displaying graphs!\n")


# Function to Draw Graph (Outside Class)
def draw_nav_graph(screen, graph):
    """Draws the navigation graph with lanes as lines and nodes as circles."""
    screen.fill((255, 255, 255))  # White background
    
    # Get lanes (edges) and vertices
    lanes = graph.get_lanes()
    vertices = graph.get_vertices()

    # Define colors
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)

    # Transform function to fit display (assumes transform exists)
    def transform(x, y):
        return int(x * 50 + 300), int(y * 50 + 300)  # Adjust scale and center

    # Draw lanes (edges)
    for x1, y1, x2, y2 in lanes:
        pygame.draw.line(screen, BLACK, transform(x1, y1), transform(x2, y2), 3)  # Thicker lane lines

    # Draw nodes (vertices)
    for x, y, _, is_charger in vertices:
        color = (255, 0, 0) if is_charger else BLUE  # Red for chargers, blue otherwise
        pygame.draw.circle(screen, color, transform(x, y), 6)  # Draw circle for each vertex

    pygame.display.flip()  # Update display


# Example Usage
if __name__ == "__main__":
    graph = NavGraph(["nav_graph_1.json"])
    graph.display_graphs()
    
    # Pygame visualization
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    draw_nav_graph(screen, graph)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
