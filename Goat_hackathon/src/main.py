import pygame
import time
from models.nav_graph import NavGraph
from models.robot import Robot
from controllers.fleet_manager import FleetManager
from controllers.traffic_manager import TrafficManager
from utils.alert import ShowAlert

# Initialize pygame and font settings
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 24)

# Load navigation graph from file
graph = NavGraph(["nav_graph_1.json"])

# Create a fleet of robots and define task positions
robots = [Robot(f"R{i}", (0, 0), (10, 10)) for i in range(5)]
task_positions = [(x, y) for x, y, _, is_charger in graph.get_vertices() if not is_charger]

# Initialize traffic and fleet managers
traffic_manager = TrafficManager(graph)
fleet_manager = FleetManager(robots)

# Assign initial tasks to robots
fleet_manager.assign_tasks(task_positions[:len(robots)])

# Set up the Pygame window
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Robot Fleet Management System")

# Define color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Track the selected robot (if any)
selected_robot = None

# Helper function to convert world coordinates to screen coordinates
def transform(x, y):
    screen_x = int(x * 50 + SCREEN_WIDTH // 2)
    screen_y = int(-y * 50 + SCREEN_HEIGHT // 2)
    return max(10, min(screen_x, SCREEN_WIDTH - 10)), max(10, min(screen_y, SCREEN_HEIGHT - 10))

# Draw the navigation graph with nodes and edges
def draw_nav_graph(screen, graph):
    draw_grid(screen)

    edges = graph.get_lanes()  # List of connections between nodes
    vertices = graph.get_vertices()

    # Draw edges (lanes)
    for x1, y1, x2, y2 in edges:
        pygame.draw.line(screen, BLACK, transform(x1, y1), transform(x2, y2), 3)

    # Draw nodes (vertices)
    for x, y, _, _ in vertices:
        pygame.draw.circle(screen, BLUE, transform(x, y), 6)

# Draw robots on the screen along with their labels and paths
def draw_robots(screen, robots, font):
    for robot in robots:
        x, y = transform(robot.position[0], robot.position[1])
        pygame.draw.circle(screen, RED if robot != selected_robot else GREEN, (x, y), 10)

        # Display robot ID
        label = font.render(robot.robot_id, True, BLACK)
        screen.blit(label, (x + 12, y - 15))

        # Draw predicted path if the robot is moving
        if robot.is_moving and robot.task and not robot.reached_destination():
            task_x, task_y = transform(robot.task[0], robot.task[1])
            draw_dashed_line(screen, (x, y), (task_x, task_y), GRAY)

# Draw a dashed line to indicate the robot's path
def draw_dashed_line(screen, start_pos, end_pos, color):
    num_dashes = 10
    for i in range(num_dashes):
        segment_start = (
            start_pos[0] + (end_pos[0] - start_pos[0]) * i / num_dashes,
            start_pos[1] + (end_pos[1] - start_pos[1]) * i / num_dashes,
        )
        segment_end = (
            start_pos[0] + (end_pos[0] - start_pos[0]) * (i + 0.5) / num_dashes,
            start_pos[1] + (end_pos[1] - start_pos[1]) * (i + 0.5) / num_dashes,
        )
        pygame.draw.line(screen, color, segment_start, segment_end, 2)

# Display a status bar showing the movement state of each robot
def draw_status_bar(screen, robots, font):
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, 30))  # Background
    status_text = " | ".join([ 
        f"{robot.robot_id}: {'Moving' if robot.is_moving else 'Completed' if robot.reached_destination() else 'Waiting'}"
        for robot in robots
    ])
    text_surface = font.render(status_text, True, BLACK)
    screen.blit(text_surface, (10, 5))

# Draw grid lines to make visualization clearer
def draw_grid(screen):
    for x in range(0, SCREEN_WIDTH, 50):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))  # Vertical grid lines
    for y in range(0, SCREEN_HEIGHT, 50):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))  # Horizontal grid lines

# Handle mouse click events to select robots or assign tasks
def handle_mouse_click(pos):
    global selected_robot
    click_x, click_y = pos

    # Check if a robot is clicked
    for robot in robots:
        robot_x, robot_y = transform(robot.position[0], robot.position[1])
        if abs(click_x - robot_x) < 12 and abs(click_y - robot_y) < 12:
            selected_robot = robot
            print(f"Selected {robot.robot_id}")
            return  

    # Assign a new task to the selected robot
    if selected_robot:
        world_x = (click_x - SCREEN_WIDTH // 2) / 50
        world_y = -(click_y - SCREEN_HEIGHT // 2) / 50
        selected_robot.assign_task((world_x, world_y))
        print(f"{selected_robot.robot_id} assigned to {world_x, world_y}")
        selected_robot = None  

# Update robot positions with a slight delay
def slow_update():
    fleet_manager.update_positions()
    
    # Check for collisions between robots
    if traffic_manager.check_collision(robots):
        ShowAlert.show("Alert!", "Robots have crashed!")  

    time.sleep(0.5)  # Slow down updates for better visualization

# Show a welcome message at startup
def show_start_message():
    screen.fill(WHITE)
    welcome_text = font.render("Welcome to the Robot Fleet Management System!", True, BLUE)
    screen.blit(welcome_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
    pygame.display.update()
    time.sleep(2)  # Display message for 2 seconds
    screen.fill(WHITE)  # Clear screen after message

# Run the main simulation loop
running = True
clock = pygame.time.Clock()

# Display the welcome message before starting the simulation
show_start_message()

while running:
    screen.fill(WHITE)

    # Handle user input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click(event.pos)

    # Update positions with a delay
    slow_update()

    # Draw navigation graph, robots, and status bar
    draw_nav_graph(screen, graph)
    draw_robots(screen, robots, font)
    draw_status_bar(screen, robots, font)

    # Update display
    pygame.display.update()
    clock.tick(30)  # Control frame rate

# Properly exit pygame
pygame.quit()
