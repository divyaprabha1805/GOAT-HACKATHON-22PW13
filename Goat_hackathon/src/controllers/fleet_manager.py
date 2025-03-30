from models.robot import Robot

class FleetManager:
    def __init__(self, robots):
        self.robots = robots  
        self.completed_tasks = set() 
    def assign_tasks(self, tasks):
        """Assigns each robot a task from the available positions."""
        for robot, task in zip(self.robots, tasks):
            if robot.reached_destination():
                self.completed_tasks.add(robot.task) 
                continue  

            robot.assign_task(task)

    def update_positions(self):
        """Moves robots toward their assigned tasks."""
        for robot in self.robots:
            robot.update_position(self)
