import pygame
pygame.init()
import random

height = 700
width = 1500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Golf Game")

clock = pygame.time.Clock()

bar_rect = pygame.Rect(1400, 100, 50, 450)
button_rect = pygame.Rect(1400, 515, 50, 35)
launch_but_rect = pygame.Rect(1400, 580, 50, 50)
restart_but_rect = pygame.Rect(10, 10, 60, 60)
background_img = pygame.image.load("Background.png")


class background:
    def __init__(self, img, scroll_x, y):
        self.scroll_x = scroll_x
        self.img = pygame.transform.scale(img, (1000, 700))
        self.y = y
        self.scroll_speed = 0
        self.bgk_width = self.img.get_width()
        self.width = 1500

    def scrolling_background(self):
        self.scroll_x -= self.scroll_speed

        if self.scroll_x <= -self.bgk_width:
            self.scroll_x = 0

        for i in range(self.bgk_width//self.width + 4):
            screen.blit(self.img, (self.scroll_x + i * self.bgk_width, 0))
        

background_stats = background(background_img, 0, 0)


ball_stats_x = 60
ball_stats_y = 500

power = 100
vel = 20
vel_resistance = 1
air_resistance = 0.8

random_width_list = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000]
random_width = random.choice(random_width_list)
floor2_x = random_width + 500

tracking_system = False

def tracking():
    mouse_pos = pygame.mouse.get_pos()
    button_rect.y = mouse_pos[1]-15


launching = False

class stats():
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.edge = self.x + self.width
        self.int_x = x
        self.int_y = y
        self.edge_int = 1500 - self.width
        self.colour = colour

    def draw(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))

    def init(self):
        self.x = self.int_x
        self.y = self.int_y
        self.edge = self.x + self.width

class circle():
    def __init__(self, x, y, rad):
        self.x = x
        self.y = y
        self.rad = rad
        self.power = 0
        self.int_power = 0
        self.air_resistance = 0.5
        self.vel = 0
        self.int_vel = 0
        self.vel_resistance = 1
        self.launching = False
        self.has_bounce = False
        self.int_x = x
        self.int_y = y
        self.down = False
        self.tries_execute = False
        self.switch = False

    def draw(self):
        pygame.draw.circle(screen, "purple", (self.x, self.y), self.rad)

    def insert(self, meter_bar_onrun):
        self.power = meter_bar_onrun
        self.int_power = meter_bar_onrun
        self.vel = meter_bar_onrun/2
        self.int_vel = meter_bar_onrun/2

    def init(self):
        self.x = self.int_x
        self.y = self.int_y
        self.power = 0
        self.vel = 0
        self.int_power = 0
        self.int_vel = 0
        self.vel_resistance = 1
        self.air_resistance = 0.5
        self.int_power = 0
        self.int_vel = 0

    def init2(self):
        self.x = self.int_x
        self.y = self.int_y

    def trajectory(self):
        self.x += self.power
        floor2.edge -= self.power
        self.power -= self.air_resistance
        
        if self.power > 0:
            self.launching = True
        if self.power < 0:
            self.air_resistance = 0
            self.power = 0
        if floor2.x < floor2.edge_int:
            self.switch = True
            floor2.x = floor2.edge_int
            floor1.x = floor1_edge_int
            for i in range(len(flags)):
                flags[i].x = edge_int_flag[i]
            background_stats.scroll_speed = 0
            
        if self.switch == False:
            if self.x >= 750:
                floor2.edge -= self.power
                floor1.edge -= self.power
                floor1.x -= self.power
                floor2.x -= self.power
                hole.x -= self.power
                self.x = 750
                for i in range(len(flags)):
                    flags[i].x -= self.power
                background_stats.scroll_speed = self.power
            
        self.y -= self.vel
        self.vel -= self.vel_resistance
        if self.y > 590 and self.x > floor2.x or self.y > 590 and self.x < floor1.edge and self.x > floor1.x:
            if self.has_bounce == False:
                self.int_vel /= 1.2
                self.int_power /= 1.3
                self.has_bounce = True
                self.vel = self.int_vel
                self.vel_resistance = 0.5
                self.power = self.int_power
                self.air_resistance = 0.3
            else:
                self.has_bounce = False
            
            #goal
            if self.int_vel < 1:
                if self.y > 590 and self.x < floor2.x and self.x > floor1.edge:
                    self.power = 0
                    self.vel = 0
                    self.air_resistance = 0
                    self.vel_resistance = 0
                    self.x = 750
                    self.y = 690
                    self.has_bounce = False
                    self.down = True
                    if self.tries_execute == False:
                        player1.num_tries += 1
                        self.tries_execute = True
                    
                    if player1.num_tries == 1:
                        player1.score_color1 = "green"
                    elif player1.num_tries == 2:
                        player1.score_color2 = "green"
                    elif player1.num_tries == 3:
                        player1.score_color3 = "green"
                else:
                    self.y = 590
                    self.vel = 0
                    self.vel_resistance = 0
                    self.has_bounce = False
                    self.down = True
                    self.power = 0
                    self.air_resistance = 0
                    player1.num_tries += 1
        #goal
        elif self.y > 590 and self.x < floor2.x and self.x > floor1.edge:
            self.power = 0
            self.vel = 0
            self.air_resistance = 0
            self.vel_resistance = 0
            self.x = 750
            self.y = 690
            self.down = True
            if self.tries_execute == False:
                player1.num_tries += 1
                self.tries_execute = True
            
            if player1.num_tries == 1:
                player1.score_color1 = "green"
            elif player1.num_tries == 2:
                player1.score_color2 = "green"
            elif player1.num_tries == 3:
                player1.score_color3 = "green"
        

class players:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.score = 0
        self.score_color1 = "grey"
        self.score_color2 = "grey"
        self.score_color3 = "grey"
        self.score_rad = 30
        self.score_x = 600
        self.score_y = 100
        self.num_tries = 0
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def draw_scores(self):
        pygame.draw.circle(screen, self.score_color1, (self.score_x, self.score_y), self.score_rad)
        pygame.draw.circle(screen, self.score_color2, (self.score_x + 150, self.score_y), self.score_rad)
        pygame.draw.circle(screen, self.score_color3, (self.score_x + 300, self.score_y), self.score_rad)

    
            
player1 = players(0, 500, 50, 100, "red")
ball = circle(ball_stats_x, ball_stats_y, 10)
floor1 = stats(0, 600, random_width, 100, "white")
floor2 = stats(floor2_x, 600, 5000, 100, "white")
floor1_edge_int = floor2.edge_int - floor1.width - 500
hole = stats(floor1.edge, 600, (floor2.x - floor1.edge), 100, "black")
ball_down = False
ball_launching = False

switch = False

def tracking2(distance1, distance2, distance3):
    if ball.launching == True:
        return
    
    mouse_pos = pygame.mouse.get_pos()
    for i in range(len(flags)):
        flags[i].x = mouse_pos[0] - flag_distance[i]
    floor1.x = mouse_pos[0] - distance1
    floor2.x = mouse_pos[0] - distance2
    hole.x = mouse_pos[0] - distance3
    floor2.edge = floor2.x + floor2.width
    ball.x = mouse_pos[0] - ball_distance


flags = []
flag_x = []
flag_distance = []
int_flag_x = []
edge_int_flag = []

for i in range(1, 41):
    flag_subject = pygame.Rect(100 * (i * 4.9999) + 490, 500, 10, 100)
    flags.append(flag_subject)

for i in range(len(flags)):
    flag_x.append(flags[i].x)
    int_flag_x.append(flags[i].x)

for i in range(len(flags)):
    edge_int_flag.append(flags[i].x + floor1_edge_int)

the_end = False


switch_launch = False

loop = True
while loop:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                tracking_system = True
            elif bar_rect.collidepoint(mouse_pos):
                switch = False
            elif launch_but_rect.collidepoint(mouse_pos):
                if ball_launching == False:
                    meter_bar_onrun = ((button_rect.y-515) * -1)/6
                    print(button_rect.y)
                    print(meter_bar_onrun)
                    ball.insert(meter_bar_onrun)
                    ball.init2()
                    floor1.init()
                    floor2.init()
                    hole.init()
                    for i in range(len(flags)):
                        flags[i].x = int_flag_x[i]
                    switch_launch = True
                    ball_launching = True
            elif restart_but_rect.collidepoint(mouse_pos):
                ball_down = True
            else:
                for i in range(len(flags)):
                    flag_distance.append(mouse_pos[0] - flags[i].x)
                distance1 = mouse_pos[0] - floor1.x
                distance2 = mouse_pos[0] - floor2.x
                distance3 = mouse_pos[0] - hole.x
                ball_distance = mouse_pos[0] - ball.x
                switch = True
        if event.type == pygame.MOUSEBUTTONUP:
            flag_distance.clear()
            tracking_system = False
            switch = False
    
    

    if switch:
        tracking2(distance1, distance2, distance3)
        if floor1.x > 0:
            floor1.x = 0
            floor2.x = floor2_x
            hole.x = floor1.edge
            ball.x = 60
            for i in range(len(flags)):
                flags[i].x = flag_x[i]
        elif floor2.edge < 1500:
            floor2.x = floor2.edge_int
            floor1.x = floor1_edge_int
            hole.x = floor2.x - hole.width
            for i in range(len(flags)):
                flags[i].x = edge_int_flag[i]


    if tracking_system:
        tracking()
        if button_rect.y < 100:
            button_rect.y = 100
        elif button_rect.y > 515:
            button_rect.y = 515
    
    
    if switch_launch:
        ball.trajectory()

    screen.fill("black")
    # screen.blit(background, (10, 10))
    background_stats.scrolling_background()
    floor1.draw()
    floor2.draw()
    hole.draw()

    for flag in flags:
        pygame.draw.rect(screen, "green", (flag))

    ball.draw()

    # player1.draw()
    player1.draw_scores()
   
    bar = pygame.draw.rect(screen, "blue", (bar_rect))
    button = pygame.draw.rect(screen, "red", (button_rect))
    launch_but = pygame.draw.rect(screen, "purple", (launch_but_rect))

    if ball.down == True:
        restart_but = pygame.draw.rect(screen, "orange", (restart_but_rect))
    else:
        ball_down = False

    if ball_down == True and ball.down == True:
        ball.init()
        floor1.init()
        floor2.init()
        hole.init()
        background_stats.scroll_x = 0
        for i in range(len(flags)):
            flags[i].x = int_flag_x[i]
        switch_launch = False
        tracking_system = False
        button_rect.y = 515
        ball.down = False
        ball_down = False
        ball.tries_execute = False
        ball.launching = False
        ball_launching = False
        if player1.num_tries == 3:
            the_end = True
        ball.switch = False
        background_stats.scroll_speed = 0
        print(background_stats.scroll_speed)

    if the_end:
        screen.fill("blue")

    

    pygame.display.update()
pygame.quit


