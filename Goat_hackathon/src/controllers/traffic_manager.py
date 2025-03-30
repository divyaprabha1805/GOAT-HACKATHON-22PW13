import math

class TrafficManager:
    def __init__(self, graph):
        self.graph = graph
        self.occupied_lanes = {}  # Tracks which lanes are currently in use

    def check_collision(self, robots):
        """
        Manages lane assignments to prevent collisions.
        Ensures fair allocation and reroutes robots when necessary.
        """
        lane_requests = {}  # Stores which robots want to use which lanes

        # Identify which robots want to use specific lanes
        for robot in robots:
            if not robot.is_moving or robot.waiting:
                continue  # Skip robots that are waiting or not moving

            # Check if the robot is currently using any lane
            for lane in self.graph.lanes:
                if len(lane) != 2:
                    continue  # Ignore invalid lane definitions

                start_id, end_id = lane
                start_pos = self.graph.get_vertex_position(start_id)
                end_pos = self.graph.get_vertex_position(end_id)

                if start_pos is None or end_pos is None:
                    continue  # Skip lanes with missing position data

                if self.is_robot_in_lane(robot.position, start_pos, end_pos):
                    lane_requests.setdefault(lane, []).append(robot)

        # Assign lanes fairly among robots
        for lane, robots_in_lane in lane_requests.items():
            if lane in self.occupied_lanes:
                occupying_robot = self.occupied_lanes[lane]
                print(f"Lane {lane} is occupied by {occupying_robot}")

                # Allow one robot to wait while others must reroute
                for robot in robots_in_lane:
                    if robot.robot_id == occupying_robot:
                        continue  # The robot already using the lane keeps it
                    elif not robot.waiting:
                        print(f"{robot.robot_id} is waiting as the lane is occupied.")
                        robot.wait()
                    else:
                        print(f"{robot.robot_id} is rerouting due to lane occupancy.")
                        robot.reroute()
            else:
                # Assign the first robot in queue to the lane
                robot = robots_in_lane[0]
                self.occupied_lanes[lane] = robot.robot_id
                print(f"{robot.robot_id} is now using lane {lane}")

        # Release lanes when robots reach their destinations
        for robot in robots:
            if robot.reached_destination():
                self.clear_lanes(robot.robot_id)
                
    def assign_lane(self, robot):
        """Assigns an available lane to the robot if possible."""
        available_lanes = [lane for lane in self.graph.lanes if lane not in self.occupied_lanes]
        
        if available_lanes:
            best_lane = min(available_lanes, key=lambda l: self.estimate_travel_time(l, robot))
            self.occupied_lanes[best_lane] = robot.robot_id
            print(f"{robot.robot_id} is now using lane {best_lane}")
        else:
            print(f"No available lanes for {robot.robot_id}. The robot will wait.")
            robot.wait()

    def clear_lanes(self, robot_id):
        """Clears any lanes occupied by the given robot."""
        cleared_lanes = [lane for lane, r_id in self.occupied_lanes.items() if r_id == robot_id]
        for lane in cleared_lanes:
            del self.occupied_lanes[lane]
            print(f"{robot_id} has cleared lane {lane}")

    def is_robot_in_lane(self, position, start, end):
        """
        Determines whether a robot is within a lane by calculating its distance
        from the line segment representing the lane.
        """
        x, y = position
        start_x, start_y = start
        end_x, end_y = end

        def distance_to_segment(px, py, ax, ay, bx, by):
            segment_length = math.dist((ax, ay), (bx, by))
            if segment_length == 0:
                return math.dist((px, py), (ax, ay))

            # Project point onto the line segment
            t = max(0, min(1, ((px - ax) * (bx - ax) + (py - ay) * (by - ay)) / (segment_length ** 2)))
            proj_x = ax + t * (bx - ax)
            proj_y = ay + t * (by - ay)

            return math.dist((px, py), (proj_x, proj_y))

        return distance_to_segment(x, y, start_x, start_y, end_x, end_y) < 1.0  # Adjust threshold as needed
