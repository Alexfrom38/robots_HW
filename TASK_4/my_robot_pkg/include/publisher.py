import rclpy
import random
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math
 
class Publisher(Node):

    def __init__(self):
        super().__init__('publisher')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.timer = self.create_timer(0.1, self.callback)

        self.linear_speed = 2.0
        self.angular_amplitude = 2.0
        self.angular_frequency = 0.8
        self.start_time = self.get_clock().now()

    def callback(self):
        # msg = Twist()

        current_time = self.get_clock().now()
        dt = (current_time - self.start_time).nanoseconds / 1e9
        omega = self.angular_amplitude * math.sin(self.angular_frequency * dt)
        msg = Twist()
        msg.linear.x = self.linear_speed
        msg.angular.z = omega
        self.pub.publish(msg)
        self.get_logger().info(f'Moving: linear={self.linear_speed:.2f}, angular={omega:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()