#!/usr/bin/env python3
import rclpy, math
from rclpy.node import Node
from my_robot_pkg.srv import ComputeDistance
 
class DistanceServer(Node):
    def __init__(self):
        super().__init__('dist_server')
        self.srv = self.create_service(ComputeDistance, 'compute_dist', self.handle_req)
        self.get_logger().info("server started")

    def haversine(self, lat1, lon1, lat2, lon2, radius=6371.0):
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = radius * c
        return distance
 
    def handle_req(self, req, resp):
        # dx = req.x2 - req.x1
        # dy = req.y2 - req.y1
        # resp.distance = math.sqrt(dx**2 + dy**2)
        self.get_logger().info("got a message. Try to find haversine metric")
        resp.distance = self.haversine(req.lat1, req.lon1, req.lat2, req.lon2)
        return resp

def main(args=None):
    rclpy.init(args=args)
    node = DistanceServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()