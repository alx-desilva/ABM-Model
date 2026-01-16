import pygame
import numpy as np
import math
import time

pygame.init()

clock = pygame.time.Clock()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
ticks = 120
tick = 0

HIT_RADIUS = 1.0 

running = True

#Scales the model (5 distance = 1 px)
scale = 5

def radar_detection(radar, targets,tolerance):
    t_list = []
    c_hit_list = []

    for target in targets:
        rel_dist = target.pos - radar.pos
        dist = np.linalg.norm(rel_dist)

        if dist > radar.max_range:
            continue

        angle_to_target = math.atan2(rel_dist[1],rel_dist[0])
        

        if abs(angle_to_target - radar.angle) <= tolerance:
            if target not in radar.current_hits:
                
                t_list.append(target)
            radar.current_hits.add(target)
        else:
            radar.current_hits.discard(target)

    return t_list
    

def world_to_screen(pos):
    x = int(pos[0] *scale)
    y = HEIGHT - int(pos[1] *scale)
    return x, y

def check_collision(interceptor, target, radius):
    dist = np.linalg.norm(interceptor.pos - target.pos)
    return dist <= radius


def calculate_tragectory(Target,Interceptor):
    Targetx = Target.pos[0]
    Targety = Target.pos[1]
    Velx = Target.vel[0]
    Vely = Target.vel[1]

    Interceptorx = Interceptor.pos[0]
    Interceptory = Interceptor.pos[1]
    speed = Interceptor.speed

    dx = Targetx-Interceptorx
    dy = Targety-Interceptory

    #I got a quadratic from distance n time

    aCoff = (Velx**2 + Vely**2) - speed**2 #Targets Velocity* -speed of interceptor
    bCoff = 2 * (dx * Velx + dy*Vely) #
    cCoff = dx**2 + dy**2

    #Plug into quadratic formula to attempt to find discrimanate, to see if the intercept is possible
    discriminate = bCoff**2 - 4*aCoff*cCoff
    t1 = (-bCoff + math.sqrt(discriminate)) / (2*aCoff)
    t2 = (-bCoff - math.sqrt(discriminate)) / (2*aCoff)

    tList = [t1, t2]

    t = 0

    for tval in tList:
        if tval > 0:
            t = tval
            #print(f'Quadratic {tval} is possible')
        else:
            pass
            #print(f"Quadratic {tval} is not possible")

    #This should return the point of contact
    PocX = Targetx + Velx*t
    PocY = Targety + Vely*t

    return PocX,PocY

class Target:
    def __init__(self,pos,vel):
        self.pos = np.array(pos,dtype=np.float64)
        self.vel = np.array(vel,dtype=np.float64)

    def update(self, dt):
        #print(type(self.pos[0]))
        #print(type(self.vel[0]))
        #print(type(dt))
        self.pos += self.vel * dt
    
    def draw(self):
        pygame.draw.circle(screen, (0,255,0),(world_to_screen(self.pos)),5)

class Interceptor:
    def __init__(self,pos,speed):
        self.pos = np.array(pos,dtype=np.float64)
        self.speed = speed
        self.vel = np.zeros(2,dtype=np.float64)
        self.target = None

    def guide_twards(self):
        if self.target != None:
            poc = calculate_tragectory(self.target, self)
            intercept_point = np.array(poc)

            direction = intercept_point - self.pos
            dist = np.linalg.norm(direction)

            if dist >0:
                self.vel = (direction/dist) * self.speed
    
    def update(self, dt):
        self.pos += self.vel* dt
    
    def draw(self):
        pygame.draw.circle(screen, (255,0,0),(world_to_screen(self.pos)),5)
    
class radar_station:
    def __init__(self,pos,beam_speed,max_range,beam_width):
        self.pos = np.array(pos, dtype=float)
        self.beam_speed = beam_speed
        self.max_range = max_range
        self.beam_width = beam_width
        self.angle = 0
        self.dirrection = 1 # 1 for left, -1 for right

        self.current_hits = set()  
    
    def update(self,dt):
        self.angle += self.beam_speed * self.dirrection * dt

        if self.angle > math.pi: # this means its passed the left(below) of the point of pie on the unit circle
            self.angle = math.pi
            self.dirrection = -1
        if self.angle < 0: #This means its passed on the right(below) of the point of 0 on the unit circle
            self.dirrection = 1
            self.angle = 0

    def draw_station(self,screen):
        x,y = world_to_screen(self.pos)
        pygame.draw.rect(screen, (0,255,0),(x-4,y-4,8,8))

    def draw_beam(self,screen):
        orgin = world_to_screen(self.pos)

        endpoint = self.pos+self.max_range*np.array([math.cos(self.angle), math.sin(self.angle)])
        endpointw = world_to_screen(endpoint)
        
        pygame.draw.line(screen, (0,255,0),(orgin),(endpointw),2)
    

    def draw(self,screen):
        self.draw_station(screen)
        self.draw_beam(screen)





Targets = []
Interceptors = []
radar_stations = []
def run_main():
    Target1 = Target((56,55),(1,-2))
    Target2 = Target((50,70),(1,-2))
    Targets.append(Target1)
    Targets.append(Target2)
    Interceptor1 = Interceptor((40,0),4)
    Interceptor2 = Interceptor((40,0),4)
    Interceptors.append(Interceptor1)
    Interceptors.append(Interceptor2)
    RadarStation1 = radar_station((70,0),4,50,2)
    RadarStation2 = radar_station((140,0),4,50,2)
    radar_stations.append(RadarStation1)
    radar_stations.append(RadarStation2)
    


run_main()

cur_assigned_targets = []
#main pygame loop
while tick < ticks and running == True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    dt = clock.tick(60)/1000

    for target in Targets:
        target.update(dt)
    
    for radar in radar_stations:
        radar.update(dt)

    detected = []

    for radar in radar_stations:
        detected.extend(radar_detection(radar,Targets,0.05))
    
    detected = list(set(detected))
    if detected:
        for interceptor in Interceptors:
            for target in detected:
                if interceptor.target == None and target not in cur_assigned_targets:
                    interceptor.target = target
                    cur_assigned_targets.append(target)

    
    for interceptor in Interceptors:
        interceptor.guide_twards()
        interceptor.update(dt)

    to_remove_targets = []
    to_remove_interceptors = []

    for interceptor in Interceptors:
        if interceptor.target is None:
            continue

        target = interceptor.target

        if check_collision(interceptor, target, HIT_RADIUS):

            to_remove_targets.append(target)
            to_remove_interceptors.append(interceptor)

            if target in cur_assigned_targets:
                cur_assigned_targets.remove(target)

    
    for target in to_remove_targets:
        if target in Targets:
            Targets.remove(target)

    for interceptor in to_remove_interceptors:
        if interceptor in Interceptors:
            Interceptors.remove(interceptor)
    
    for interceptor in Interceptors:
        if interceptor.target in to_remove_targets:
            interceptor.target = None


    for radar in radar_stations:
        radar.draw(screen)

    for target in Targets:
        target.draw()

    for interceptor in Interceptors:
        interceptor.draw()

    #print(Interceptor1.pos[0],Interceptor1.pos[1])
    #time.sleep(1)
    pygame.display.update()

