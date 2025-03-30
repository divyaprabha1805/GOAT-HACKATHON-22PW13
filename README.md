How to run:Inside src,"python main.py"
VIDEO DEMO LINK:https://www.loom.com/share/3b7464c9331a45aa9a2c1efc18ff4b70?sid=1003f88d-078c-4075-9171-69556ef1f427
### Robot Fleet Management System - Explanation 

This system is designed to manage a fleet of robots, assigning them tasks and guiding them to their respective destinations using a navigation graph. Below is a step-by-step explanation of how the system works:  

---

### 1. Assigning Initial Tasks to Robots 
- When the program starts, a **navigation graph** is loaded, which consists of nodes (representing positions) and lanes (representing paths).  
- A set of **robots** is created, each assigned a unique ID.  
- The fleet manager assigns each robot an **initial task**, which is a target position in the navigation graph.  

---

### 2. Robots Move to the Navigation Lane
- Once a robot receives a task, it first moves toward the **nearest lane** in the navigation graph.  
- The traffic manager ensures that robots navigate efficiently while avoiding **collisions** with other robots.  
- The movement of each robot is displayed visually on the screen using **Pygame**, where robots appear as red circles and lanes as black lines.  

---

### 3. Navigating Toward the Assigned Destination
- After reaching a lane, the robot follows the shortest possible path to reach its assigned **task position**.  
- A **dashed path** is drawn from the robot’s current location to its destination, helping visualize its movement.  
- The status bar at the top of the screen displays whether each robot is **Moving, Waiting, or Task Completed**.  

---

### 4. Selecting Robots and Assigning New Tasks
- Users can **click** on a robot to select it. The selected robot is highlighted in **green**.  
- After selecting a robot, clicking on any other location assigns a **new task** to that robot.  
- The robot then re-routes and moves toward the newly assigned position.  

---

### 5. Handling Collisions and Alerts  
- The traffic manager continuously **monitors** the movement of robots to detect any **collisions**.  
- If two robots are predicted to collide, an **alert message** is triggered to warn the user.  
- The system slows down movements to ensure better **control and visualization**.  

---

### 6. Ending the Simulation  
- The simulation continues until the user **closes the window**.  
- Once the program is exited, Pygame shuts down properly.  

---

### Conclusion
This project showcases **fleet management, path planning, and real-time monitoring** of autonomous robots in a simulated environment. It helps visualize how a group of robots can be efficiently controlled to complete assigned tasks while avoiding collisions.  

![screenshot1](https://github.com/divyaprabha1805/GOAT-HACKATHON-22PW13/blob/main/screenshot/Screenshot%202025-03-30%20223638.png)
![2](https://github.com/divyaprabha1805/GOAT-HACKATHON-22PW13/blob/main/screenshot/Screenshot%202025-03-30%20224025.png)
![3](https://github.com/divyaprabha1805/GOAT-HACKATHON-22PW13/blob/main/screenshot/Screenshot%202025-03-30%20224119.png)
![4](https://github.com/divyaprabha1805/GOAT-HACKATHON-22PW13/blob/main/screenshot/Screenshot%202025-03-30%20224213.png)
![6](https://github.com/divyaprabha1805/GOAT-HACKATHON-22PW13/blob/main/screenshot/Screenshot%202025-03-30%20224355.png)
