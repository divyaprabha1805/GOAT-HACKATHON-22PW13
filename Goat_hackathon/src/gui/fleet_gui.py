import pygame
from models.nav_graph import NavGraph
from models.robot import Robot
from controllers.fleet_manager import FleetManager
from controllers.traffic_manager import TrafficManager

# Step 1: Load the navigation graph
graph = NavGraph(["nav_graph_1.json"])

# Step 2: Create robots at random positions to avoid overlap
robots = [Robot(f"R{i}", (0, 0), (10, 10)) for i in range(5)]

# Step 3: Assign tasks, avoiding charging stations
task_positions = [(x, y) for x, y, _, is_charger in graph.get_vertices() if not is_charger]

# Step 4: Initialize the traffic manager
traffic_manager = TrafficManager(graph)

# Step 5: Initialize the fleet manager
fleet_manager = FleetManager(robots)

# Step 6: Assign tasks to robots
fleet_manager.assign_tasks(task_positions[:len(robots)])

# Step 7: Initialize Pygame for visualization
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Robot Fleet Management System")
font = pygame.font.Font(None, 24)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Adjust scaling to fit the graph on the screen
SCALE_X = SCREEN_WIDTH / 20
SCALE_Y = SCREEN_HEIGHT / 20

# Convert world coordinates to screen coordinates
def transform(x, y):
    screen_x = int(x * 50 + SCREEN_WIDTH // 2)
    screen_y = int(-y * 50 + SCREEN_HEIGHT // 2)
    # Keep coordinates within the screen boundaries
    screen_x = max(0, min(screen_x, SCREEN_WIDTH))
    screen_y = max(0, min(screen_y, SCREEN_HEIGHT))
    return screen_x, screen_y

# Step 8: Run the simulation loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update robot positions and manage traffic
    fleet_manager.update_positions()
    traffic_manager.check_collision(robots)

    # Draw the navigation graph (nodes and connections)
    for x, y, neighbors, _ in graph.get_vertices():
        pygame.draw.circle(screen, BLACK, transform(x, y), 5)  # Draw nodes

        for neighbor_idx in neighbors:
            if isinstance(neighbor_idx, int):  # Ensure it's a valid index
                nx, ny, _, _ = graph.get_vertices()[neighbor_idx]
                pygame.draw.line(screen, BLACK, transform(x, y), transform(nx, ny), 1)

    # Draw robots
    for robot in robots:
        rx, ry = robot.position
        pygame.draw.circle(screen, RED, transform(rx, ry), 8)  # Draw robot
        text = font.render(robot.robot_id, True, BLACK)  # Display robot ID
        screen.blit(text, (transform(rx, ry)[0] + 10, transform(rx, ry)[1] - 10))

    # Update the display
    pygame.display.flip()
    clock.tick(2)  # Adjust speed (frames per second)

pygame.quit()
