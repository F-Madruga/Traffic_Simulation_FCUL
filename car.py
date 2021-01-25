import pygame
import random
import constants
from actormodel.actor import Actor
from actormodel.message import Message
from pygame.math import Vector2
from math import sin, cos, radians


class Car(Actor):
    count = 0
    def __init__(self, x, y, angle, current_block_id, velocity=Vector2(0.0, 0.2), radius=constants.SIZE):
        self.id = Car.count
        self.current_block_id = current_block_id
        Car.count += 1
        self.radius = radius
        self.position = Vector2(x, y)
        self.velocity = velocity
        self.angle = angle
        self.next_step = []
        super().__init__()
    
    def __str__(self):
     return "Car={id=" + str(self.id) + ", position=" + str(self.position) + ", velocity=" + str(self.velocity) + ", radius=" + str(self.radius) + "}"

    def display(self, screen):
        pygame.draw.circle(screen, constants.RED , self.position, self.radius)

    def move_left(self):
        if self.angle - 90 < 0:
            self.angle = 270
        else:
            self.angle -= 90
    
    def move_right(self):
        if self.angle + 90 >= 360:
            self.angle = 0
        else:
            self.angle += 90

    def move(self, blocks):
        # front_blocks = [left, left_front, front, right_front, right]
        if len(self.next_step) != 0 or blocks[1][1][0] != self.current_block_id:
            front_blocks = self.get_front_blocks(blocks)
            possible_directions = []
            for i in range(0, len(front_blocks), 2):
                if front_blocks[i][2] != constants.BLACK:
                    possible_directions.append(i)
            if len(self.next_step) != 0:
                self.execute_step(blocks, front_blocks, possible_directions)
            elif blocks[1][1][0] != self.current_block_id:
                self.current_block_id = blocks[1][1][0]
                self.decide_direction(blocks, front_blocks, possible_directions)
        self.position += self.velocity.rotate(self.angle)

    def execute_step(self, blocks, front_blocks, possible_directions):
        if len(possible_directions) > 1:
            self.handle_intersect(blocks, front_blocks, possible_directions)
        decision = self.next_step[0]
        if self.next_step[1](self.position[0], self.position[1]):
            if decision == 0: # Turn left
                self.move_left()
            elif decision == len(front_blocks) - 1: # Turn right
                self.move_right()
            self.next_step = []
    
    def handle_intersect(self, blocks, front_blocks, possible_directions):
        intersect_blocks = [front_blocks[possible_direction] for possible_direction in possible_directions]
        intersect_blocks.append(blocks[1][1])
        self.address(Message("Pára crl", messageType="stop"))
        for block in intersect_blocks:
            for car in block[3]:
                if car.id != self.id:
                    print(car.id)
                    print(self.id)
                    print(block[0])
                    if block[0] == blocks[1][1][0]:
                        car.address(Message("Pára crl", messageType="stop"))
    
    def decide_direction(self, blocks, front_blocks, possible_directions):
        decision = random.choice(possible_directions)
        self.next_step.append(decision)
        if decision == 0: # Turn left
            if self.angle == 0: # Down
                self.next_step.append(lambda x, y: y >= blocks[1][1][1].y + ((3 * blocks[1][1][1].height) / 4))
            elif self.angle == 180: # Up
                self.next_step.append(lambda x, y: y <= blocks[1][1][1].y + (blocks[1][1][1].height / 4))
            elif self.angle == 90: # Left
                self.next_step.append(lambda x, y: x <= blocks[1][1][1].x + (blocks[1][1][1].width / 4))
            else: # Right
                self.next_step.append(lambda x, y: x >= blocks[1][1][1].x + ((3 * blocks[1][1][1].width) / 4))
        elif decision == len(front_blocks) - 1: # Turn right
            if self.angle == 0: # Down
                self.next_step.append(lambda x, y: y >= blocks[1][1][1].y + (blocks[1][1][1].height / 4))
            elif self.angle == 180: # Up
                self.next_step.append(lambda x, y: y <= blocks[1][1][1].y + ((3 * blocks[1][1][1].height) / 4))
            elif self.angle == 90: # Left
                self.next_step.append(lambda x, y: x <= blocks[1][1][1].x + ((3 * blocks[1][1][1].width) / 4))
            else: # Right
                self.next_step.append(lambda x, y: x >= blocks[1][1][1].x + (blocks[1][1][1].width / 4))
        else:
            self.next_step = []
    
    def get_front_blocks(self, blocks):
        front_blocks = []
        if self.angle == 0: # Down
            front_blocks.append(blocks[1][2])
            front_blocks += blocks[2][::-1]
            front_blocks.append(blocks[1][0])
        elif self.angle == 180: # Up
            front_blocks.append(blocks[1][0])
            front_blocks += blocks[0]
            front_blocks.append(blocks[1][2])
        elif self.angle == 90: # Left
            front_blocks += blocks[2][0:2][::-1]
            front_blocks.append(blocks[1][0])
            front_blocks += blocks[0][0:2]
        else: # Right
            front_blocks += blocks[0][1:]
            front_blocks.append(blocks[1][2])
            front_blocks += blocks[2][1:][::-1]
        return front_blocks

    def handle_message(self, message):
        if message.messageType == "stop":
            self.velocity = Vector2(0.0, 0.0)
        if message.messageType == "go":
            self.velocity = Vector2(0.0, 0.2)