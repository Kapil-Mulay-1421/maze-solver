import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time
import math
from sensor_msgs.msg import LaserScan


class RosSimulator(Node):
    """
    Handles communication with Gazebo via ROS 2 for robot actions and feedback.
    """

    def __init__(self):
        super().__init__('maze_solver_simulator')
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.feedback = None
        self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.timer_period = 0.005  # seconds
        self.tof_front_distance = 0
        self.tof_left_distance = 0
        self.tof_right_distance = 0
        self.tof_front_sub = self.create_subscription(
            LaserScan,
            '/tof_front',
            self.tof_front_callback,
            20
        )
        self.tof_left_sub = self.create_subscription(
            LaserScan,
            '/tof_left',
            self.tof_left_callback,
            20
        )
        self.tof_right_sub = self.create_subscription(
            LaserScan,
            '/tof_right',
            self.tof_right_callback,
            20
        )

    def odom_callback(self, msg):
        """
        Callback to receive odometry feedback from Gazebo.
        """
        self.feedback = msg

    def wait_for_feedback(self):
        while self.feedback is None and rclpy.ok():
            rclpy.spin_once(self)

    def move_forward(self, distance=0.25, speed=0.25):
        print("Moving forward: distance = {}, speed = {}".format(distance, speed))
        """
        Publishes a forward movement command and waits for feedback.
        Args:
            distance (float): Distance to move forward in meters.
            speed (float): Linear speed in m/s.
        Returns:
            Odometry: The feedback after movement.
        """
        self.wait_for_feedback()
        start = self.feedback.pose.pose.position

        move_cmd = Twist()
        move_cmd.linear.x = speed
        move_cmd.angular.z = 0.0

        moved = 0.0
        while rclpy.ok():
            rclpy.spin_once(self)
            current = self.feedback.pose.pose.position
            moved = ((current.x - start.x) ** 2 + (current.y - start.y) ** 2) ** 0.5

            if moved >= distance:
                break

            self.cmd_vel_pub.publish(move_cmd)
            time.sleep(self.timer_period)

        # Stop the robot
        print("Moved forward: started at {} moved = {} and new position = {}".format(start.x, moved, current.x))
        self.cmd_vel_pub.publish(Twist())
        return self.feedback

    def quaternion_to_yaw(self, q):
        """Extract yaw from quaternion (w, x, y, z)."""
        # ROS gives quaternion as (x, y, z, w)
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        return math.atan2(siny_cosp, cosy_cosp)

    def normalize_angle(self, angle):
        """Normalize angle to [-pi, pi]."""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

    def shortest_angular_distance(self, from_angle, to_angle):
        """Compute the minimal angular difference (with direction)."""
        return self.normalize_angle(to_angle - from_angle)

    def turn(self, angle_deg=90, angular_speed=0.25):
        """
        Turns the robot in-place using odometry-based yaw.
        Args:
            angle_deg (float): Target angle in degrees.
            angular_speed (float): Angular speed in radians/sec.
        """
        target_angle = math.radians(angle_deg)
        move_cmd = Twist()
        move_cmd.linear.x = 0.0
        move_cmd.linear.y = 0.0
        move_cmd.linear.z = 0.0
        move_cmd.angular.z = math.copysign(angular_speed, target_angle)

        # Wait until odometry data is available
        while self.feedback is None and rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.1)

        start_q = self.feedback.pose.pose.orientation
        start_yaw = self.quaternion_to_yaw(start_q)
        turned = 0.0

        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.05)
            current_q = self.feedback.pose.pose.orientation
            current_yaw = self.quaternion_to_yaw(current_q)
            turned = self.shortest_angular_distance(start_yaw, current_yaw)

            if abs(turned) >= abs(target_angle):
                break

            self.cmd_vel_pub.publish(move_cmd)
            time.sleep(self.timer_period)

        self.cmd_vel_pub.publish(Twist())  # stop
        return self.feedback

    def turn_left(self, angle=90, angular_speed=0.25):
        return self.turn(angle_deg=angle, angular_speed=angular_speed)

    def turn_right(self, angle=90, angular_speed=0.25):
        return self.turn(angle_deg=-angle, angular_speed=angular_speed)

    def get_feedback(self):
        return self.feedback
    
    def tof_front_callback(self, msg):
    # msg.ranges is a list, for 1-sample ray sensor it will have one value
        if msg.ranges:
            self.tof_front_distance = msg.ranges[0]

    def tof_left_callback(self, msg):
    # msg.ranges is a list, for 1-sample ray sensor it will have one value
        if msg.ranges:
            self.tof_left_distance = msg.ranges[0]

    def tof_right_callback(self, msg):
    # msg.ranges is a list, for 1-sample ray sensor it will have one value
        if msg.ranges:
            self.tof_right_distance = msg.ranges[0]

    def get_tof_front_distance(self):
        return self.tof_front_distance
    
    def get_tof_left_distance(self):
        return self.tof_left_distance

    def get_tof_right_distance(self):
        return self.tof_right_distance
    
    



def main():
    rclpy.init()
    simulator = RosSimulator()

    try:
        # Example usage:
        simulator.move_forward()
        print(simulator.feedback.pos.pos.position.x)
        simulator.move_forward()
        print(simulator.feedback.pos.pos.position.x)
    except KeyboardInterrupt:
        pass
    finally:
        simulator.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
