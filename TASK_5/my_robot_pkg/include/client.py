#!/usr/bin/env python3
import time
import random
import rclpy
from rclpy.node import Node
from task_5_turtle.srv import SpawnTurtle, KillTurtle
import math

class Client(Node):
    AMPLITUDE = 11.0
    REQUEST_HZ = 2.0
    REQUEST_COUNT = 20
    counter = 1
    names = []

    def __init__(self):
        super().__init__('client')
        period = 1.0 / self.REQUEST_HZ
        self.cli_spawn = self.create_client(SpawnTurtle, 'spawn_turtle')
        self.cli_kill = self.create_client(KillTurtle, 'kill_turtle')
        self.cli_spawn.wait_for_service()
        self.cli_kill.wait_for_service()
        self.send_spawn_requests()
        time.sleep(2)
        self.send_kill_requests()


    def send_spawn_requests(self):
        self.start_time = self.get_clock().now()
        for i in range(self.REQUEST_COUNT):
            req = SpawnTurtle.Request()
            req.name = f'tutel_{self.counter}'

            current_time = self.get_clock().now()
            dt = (current_time - self.start_time).nanoseconds / 1e9
            omega = 2 * math.sin(10 * dt)

            if (omega == 0):
                omega = math.sin(math.cos(math.sin(current_time)))
            req.x = 2 / omega
            req.y = 2 * omega
            # req.x, req.y = random.uniform(0.0, self.AMPLITUDE), random.uniform(0.0, self.AMPLITUDE)
    


            self.get_logger().info(f'requested spawn: name: {req.name}, x: {req.x:.1f}, y: {req.y:.1f}')
            future = self.cli_spawn.call_async(req)
            rclpy.spin_until_future_complete(self, future)
            self.get_logger().info(f'spawn {req.name}: success: {future.result().success}, message: {future.result().message}')
            if (future.result().success):
                self.names.append(req.name)
                self.counter += 1
            time.sleep(0.1)

    def send_kill_requests(self):
        for name in self.names:
            req = KillTurtle.Request()
            req.name = name
            self.get_logger().info(f'requested kill: name: {name}')
            future = self.cli_kill.call_async(req)
            rclpy.spin_until_future_complete(self, future)
            self.get_logger().info(f'kill {name}: success: {future.result().success}, message: {future.result().message}')
            time.sleep(0.1)
        for name in self.names:
            self.names.remove(name)

def main(args = None):
    rclpy.init(args = args)
    node = Client()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()