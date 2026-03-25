#!/usr/bin/env python3

import rclpy

from rclpy.node import Node
from my_robot_pkg.srv import ComputeDistance

class DistanceClient(Node):
    def __init__(self):
        super().__init__('dist_client')

        self.cli = self.create_client(ComputeDistance, 'compute_dist')
        self.cli.wait_for_service()
        
        req = ComputeDistance.Request()
        # req.x1, req.y1 = 0.0, 0.0
        # req.x2, req.y2 = 3.0, 4.0

        req.lat1 = 35.9874
        req.lon1 = 9.848291

        req.lat2 = 13.4884
        req.lon2 = 102.31313

        future = self.cli.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        self.get_logger().info(
            f'Current geographical distance(haversine metric) =  {future.result().distance:.6f} km'
        )

def main(args = None):
    rclpy.init(args = args)
    node = DistanceClient()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
