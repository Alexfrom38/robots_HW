#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn, Kill
from task_5_turtle.srv import SpawnTurtle, KillTurtle
 
class Server(Node):
    def __init__(self):
        super().__init__('server')
        self.srv_spawn = self.create_service(SpawnTurtle, 'spawn_turtle', self.handle_spawn_request)
        self.srv_kill = self.create_service(KillTurtle, 'kill_turtle', self.handle_kill_request)
        self.cli_spawn = self.create_client(Spawn, '/spawn')
        self.cli_kill = self.create_client(Kill, '/kill')
        self.get_logger().info("server started")
        self.start_time = self.get_clock().now()
 
    def handle_spawn_request(self, req, resp):
        if not (0 <= req.x <= 11 and 0 <= req.y <= 11):
            resp.success, resp.message = False, 'Coords out of range'
            return resp
        spawn_req = Spawn.Request()
        spawn_req.name = req.name
        spawn_req.x, spawn_req.y = req.x, req.y
        future = self.cli_spawn.call_async(spawn_req)
        resp.success, resp.message = True, 'Empty'
        return resp
 
    def handle_kill_request(self, req, resp):
        kill_req = Kill.Request()
        kill_req.name = req.name
        future = self.cli_kill.call_async(kill_req)
        resp.success, resp.message = True, 'Empty'
        return resp

def main(args=None):
    rclpy.init(args=args)
    node = Server()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()