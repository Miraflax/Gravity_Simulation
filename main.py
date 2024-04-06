import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1400, 850
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect")

PLANET_MASS = 1000
SHIP_MASS = 5
G = 6  # gravitational constant
FPS = 60
PLANET_SIZE = 100 #radius
OBJ_SIZE = 5
VEL_SCALE = 100

# import images to later draw them#

BG = pygame.transform.scale(pygame.image.load("space.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("jupiter2.png"), (PLANET_SIZE * 2, PLANET_SIZE * 2))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        win.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))


class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (G * self.mass * planet.mass) / distance**2
        angle = math.atan2(planet.y - self.y, planet.x - self.x)
        acceleration = force / self.mass
        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)
        self.vel_x += acceleration_x
        self.vel_y += acceleration_y
        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)

def create_ship(Location, mouse):
    t_x, t_y = Location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)
    return obj

def main():
    running = True
    clock = pygame.time.Clock()

    # stores position of objects we haven't yet launched
    # stores obj start location, direction and velocity, and mode
    objects = []
    temp_obj_pos = None
    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    
    while running:
        #regulates the speed of the loop
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    t_x, t_y = temp_obj_pos
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj) 
                    temp_obj_pos = None
                else: 
                    temp_obj_pos = mouse_pos
                
                
        #drawing the image. draws over everythig
        win.blit(BG, (0, 0))

        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)
            
        for obj in objects[:]:
            obj.draw()
            obj.move(planet)
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_SIZE
            if off_screen or collided:
                objects.remove(obj)

        # all of the drawing operations, then update
        # must update every time the display changes
        
        planet.draw()
        
        pygame.display.update() 
              
    pygame.quit()

#only calls function if we run it directly
#rather than code being inputted from another file
if __name__ == "__main__":
    main()


