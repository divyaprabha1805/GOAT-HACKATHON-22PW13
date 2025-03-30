import math
import random
from utils.alert import ShowAlert  # Import the alert class

class Robot:
    def __init__(self, robot_id, position, destination):
        self.robot_id = robot_id
        self.position = position
        self.destination = destination
        self.is_moving = True
        self.waiting = False
        self.task = None
        self.speed = 1.0
        self.wait_time = 0
        self.previous_positions = []

    def log(self, message):
        """Logs robot actions to 'fleet_logs.txt' with UTF-8 encoding."""
        with open("fleet_logs.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{message}\n")
        print(message)

    def show_alert(self, message):
        """Displays an alert when a path is blocked."""
        ShowAlert.show_warning("Blocked Path", message)

    def update_position(self, fleet_manager):
        """Moves the robot towards its destination while avoiding collisions."""
        if not self.is_moving:
            return

        occupied_positions = {robot.position for robot in fleet_manager.robots if robot.robot_id != self.robot_id}
        x, y = self.position
        dest_x, dest_y = self.destination
        distance = math.dist(self.position, self.destination)

        if distance < 0.1:
            self.position = self.destination
            self.is_moving = False
            self.log(f"{self.robot_id} reached its destination at {self.position}")
        else:
            direction_x = (dest_x - x) / distance
            direction_y = (dest_y - y) / distance
            step = min(self.speed, distance)
            new_position = (round(x + direction_x * step, 4), round(y + direction_y * step, 4))

            if new_position in occupied_positions:
                self.wait()
            else:
                self.position = new_position
                self.log(f"{self.robot_id} moved to {self.position}")

    def assign_task(self, task):
        """Assigns a task to the robot and sets it as the destination."""
        self.task = task
        self.destination = task
        self.is_moving = True
        self.log(f"{self.robot_id} assigned a task at {task}")

    def resume(self):
        """Resumes movement if the robot was waiting."""
        self.waiting = False
        self.is_moving = True
        self.log(f"{self.robot_id} resumed movement.")

    def reroute(self):
        """Attempts to find an alternative path if blocked."""
        self.log(f"{self.robot_id} is trying to reroute to avoid congestion.")

        max_attempts = 5  
        attempts = 0
        while attempts < max_attempts:
            offset = random.uniform(1, 3)
            new_x = round(self.position[0] + random.choice([-offset, offset]), 4)
            new_y = round(self.position[1] + random.choice([-offset, offset]), 4)

            if (new_x, new_y) not in self.previous_positions:
                self.destination = (new_x, new_y)
                self.previous_positions.append(self.destination)
                self.log(f"{self.robot_id} chose a new temporary path to {self.destination}")
                self.is_moving = True
                return

            attempts += 1

        self.log(f"{self.robot_id} could not find an alternate path after {max_attempts} attempts. Waiting...")
        self.is_moving = False
        self.waiting = True

    def reached_destination(self):
        """Returns True if the robot has reached its destination accurately."""
        return round(math.dist(self.position, self.destination), 4) < 0.1
