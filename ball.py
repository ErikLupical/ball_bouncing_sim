import turtle
import random
import math


class Ball:
    def __init__(self, canvas_width, canvas_height, ball_radius, num_balls):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.ball_radius = ball_radius
        xpos, ypos, vx, vy, ball_color = [], [], [], [], []
        for i in range(num_balls):
            xpos.append(random.randint(-1 * canvas_width + ball_radius, canvas_width - ball_radius))
            ypos.append(random.randint(-1 * canvas_height + ball_radius, canvas_height - ball_radius))
            vx.append(random.randint(1, 0.01 * canvas_width))
            vy.append(random.randint(1, 0.01 * canvas_height))
            ball_color.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.xpos = xpos
        self.ypos = ypos
        self.vx = vx
        self.vy = vy
        self.ball_color = ball_color

    def draw_circle(self, i):
        # draw a circle of radius equals to size at x, y coordinates and paint it with color
        turtle.penup()
        turtle.color(self.ball_color[i])
        turtle.fillcolor(self.ball_color[i])
        turtle.goto(self.xpos[i], self.ypos[i])
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(self.ball_radius)
        turtle.end_fill()

    def move_circle(self, i):
        # update the x, y coordinates of ball i with velocity in the x (vx) and y (vy) components
        self.xpos[i] += self.vx[i]
        self.ypos[i] += self.vy[i]

        # if the ball hits the side walls, reverse the vx velocity
        if abs(self.xpos[i] + self.vx[i]) > (self.canvas_width - self.ball_radius):
            self.vx[i] = -self.vx[i]

        # if the ball hits the ceiling or the floor, reverse the vy velocity
        if abs(self.ypos[i] + self.vy[i]) > (self.canvas_height - self.ball_radius):
            self.vy[i] = -self.vy[i]

        # check for collisions with other balls
        for j in range(i+1, len(self.xpos)):
            dx = self.xpos[j] - self.xpos[i]
            dy = self.ypos[j] - self.ypos[i]
            distance = math.sqrt(dx**2 + dy**2)

            # if the distance between the centers of the balls is less than or equal to the sum of their radii, they are colliding
            if distance <= 2*self.ball_radius:
                angle = math.atan2(dy, dx)
                magnitude_1 = math.sqrt(self.vx[i]**2 + self.vy[i]**2)
                magnitude_2 = math.sqrt(self.vx[j]**2 + self.vy[j]**2)
                direction_1 = math.atan2(self.vy[i], self.vx[i])
                direction_2 = math.atan2(self.vy[j], self.vx[j])
                new_vx_1 = magnitude_1 * math.cos(direction_1 - angle)
                new_vy_1 = magnitude_1 * math.sin(direction_1 - angle)
                new_vx_2 = magnitude_2 * math.cos(direction_2 - angle)
                new_vy_2 = magnitude_2 * math.sin(direction_2 - angle)
                final_vx_1 = ((self.ball_radius - self.ball_radius) * new_vx_1 + (self.ball_radius + self.ball_radius) * new_vx_2) / (self.ball_radius + self.ball_radius)
                final_vx_2 = ((self.ball_radius + self.ball_radius) * new_vx_1 - (self.ball_radius - self.ball_radius) * new_vx_2) / (self.ball_radius + self.ball_radius)
                final_vy_1 = new_vy_1
                final_vy_2 = new_vy_2
                self.vx[i] = math.cos(angle) * final_vx_1 + math.cos(angle + math.pi/2) * final_vy_1
                self.vy[i] = math.sin(angle) * final_vx_1 + math.sin(angle + math.pi/2) * final_vy_1
                self.vx[j] = math.cos(angle) * final_vx_2 + math.cos(angle + math.pi/2) * final_vy_2
                self.vy[j] = math.sin(angle) * final_vx_2 + math.sin(angle + math.pi/2) * final_vy_2
