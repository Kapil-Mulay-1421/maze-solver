import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
import tf.transformations
import math

class RosSimulator:
    """
    Handles communication with Gazebo via ROS for robot actions and feedback.
    Supports both odometry (for linear movement) and IMU (for rotation).
    """

    def __init__(self):
        rospy.init_node('maze_solver_simulator', anonymous=True)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.odom_feedback = None
        self.imu_feedback = None
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.imu_sub = rospy.Subscriber('/imu', Imu, self.imu_callback)
        self.rate = rospy.Rate(10)  # 10 Hz

    def odom_callback(self, msg):
        """
        Callback to receive odometry feedback from Gazebo.
        """
        self.odom_feedback = msg

    def imu_callback(self, msg):
        """
        Callback to receive IMU feedback from Gazebo.
        """
        self.imu_feedback = msg

    def get_yaw(self):
        """
        Extracts yaw (in radians) from the latest IMU message.
        """
        if self.imu_feedback is None:
            return None
        orientation_q = self.imu_feedback.orientation
        quaternion = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        euler = tf.transformations.euler_from_quaternion(quaternion)
        return euler[2]  # Yaw

    def move_forward(self, distance=0.2, speed=0.1):
        """
        Publishes a forward movement command and waits for odometry feedback.
        Args:
            distance (float): Distance to move forward in meters.
            speed (float): Linear speed in m/s.
        Returns:
            Odometry: The feedback after movement.
        """
        move_cmd = Twist()
        move_cmd.linear.x = speed
        move_cmd.angular.z = 0.0

        while self.odom_feedback is None and not rospy.is_shutdown():
            rospy.sleep(0.1)
        start = self.odom_feedback.pose.pose.position

        moved = 0.0
        while moved < distance and not rospy.is_shutdown():
            self.cmd_vel_pub.publish(move_cmd)
            self.rate.sleep()
            current = self.odom_feedback.pose.pose.position
            moved = ((current.x - start.x) ** 2 + (current.y - start.y) ** 2) ** 0.5

        # Stop the robot
        stop_cmd = Twist()
        self.cmd_vel_pub.publish(stop_cmd)
        return self.odom_feedback

    def turn_left(self, angle=90, angular_speed=0.5):
        """
        Publishes a left turn command and waits for IMU feedback.
        Args:
            angle (float): Angle to turn in degrees.
            angular_speed (float): Angular speed in rad/s.
        Returns:
            float: The final yaw after turning.
        """
        move_cmd = Twist()
        move_cmd.linear.x = 0.0
        move_cmd.angular.z = angular_speed

        # Wait for IMU data
        while self.imu_feedback is None and not rospy.is_shutdown():
            rospy.sleep(0.1)
        start_yaw = self.get_yaw()
        target_angle = math.radians(angle)
        turned = 0.0

        def shortest_angular_distance(a, b):
            d = a - b
            while d > math.pi:
                d -= 2 * math.pi
            while d < -math.pi:
                d += 2 * math.pi
            return d

        while abs(turned) < abs(target_angle) and not rospy.is_shutdown():
            self.cmd_vel_pub.publish(move_cmd)
            self.rate.sleep()
            current_yaw = self.get_yaw()
            turned = shortest_angular_distance(current_yaw, start_yaw)

        # Stop the robot
        stop_cmd = Twist()
        self.cmd_vel_pub.publish(stop_cmd)
        return self.get_yaw()

    def turn_right(self, angle=90, angular_speed=0.5):
        """
        Publishes a right turn command and waits for IMU feedback.
        Args:
            angle (float): Angle to turn in degrees.
            angular_speed (float): Angular speed in rad/s.
        Returns:
            float: The final yaw after turning.
        """
        move_cmd = Twist()
        move_cmd.linear.x = 0.0
        move_cmd.angular.z = -angular_speed

        # Wait for IMU data
        while self.imu_feedback is None and not rospy.is_shutdown():
            rospy.sleep(0.1)
        start_yaw = self.get_yaw()
        target_angle = -math.radians(angle)
        turned = 0.0

        def shortest_angular_distance(a, b):
            d = a - b
            while d > math.pi:
                d -= 2 * math.pi
            while d < -math.pi:
                d += 2 * math.pi
            return d

        while abs(turned) < abs(target_angle) and not rospy.is_shutdown():
            self.cmd_vel_pub.publish(move_cmd)
            self.rate.sleep()
            current_yaw = self.get_yaw()
            turned = shortest_angular_distance(current_yaw, start_yaw)

        # Stop the robot
        stop_cmd = Twist()
        self.cmd_vel_pub.publish(stop_cmd)
        return self.get_yaw()

    def get_odom_feedback(self):
        """
        Returns the latest odometry feedback.
        """
        return self.odom_feedback

    def get_imu_feedback(self):
        """
        Returns the latest IMU feedback.
        """
        return self.imu_feedback