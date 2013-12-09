 
import pygame as py
from pygame.locals import *
from random import randrange

class Rect(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
	def Update(self, x, y):
		self.x = x
		self.y = y
		
class Brick(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 40
		self.height = 20
		self.alive = False
		self.rect = Rect(self.x, self.y, self.width, self.height)
		
		
	def Render(self, screen):
		self.color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
		py.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
		py.draw.rect(screen, (randrange(0, 255), randrange(0, 255), randrange(0, 255)), (self.x, self.y, self.width, self.height), 1)
		
class Player(object):
	def __init__(self):
		self.x = (800-80)/2
		self.y = 600-50
		self.width = 80
		self.height = 10
		self.vx = 0
		self.speed = 5
		self.rect = Rect(self.x, self.y, self.width, self.height)
		
	def Render(self, screen):
		py.draw.rect(screen, (randrange(0, 255), randrange(0, 255), randrange(0, 255)), (self.x, self.y, self.width, self.height))
		
	def Update(self):
		key = py.key.get_pressed()
		if key[K_RIGHT]:
			self.vx = self.speed
		elif key[K_LEFT]:
			self.vx = -self.speed
		else:
			self.vx = 0
			
		self.x += self.vx
		if self.x + self.width > 800:
			self.x = 800 - self.width
		if self.x < 0:
			self.x = 0
		self.rect.Update(self.x, self.y)
			
class Ball(object):
	def __init__(self):
		self.x = 395
		self.y = 600-100
		self.vx = 4
		self.vy = 4
		self.radius = 5
		self.rect = Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)
		
	def Render(self, screen):
		py.draw.circle(screen, (randrange(0, 255), randrange(0, 255), randrange(0, 255)), (self.x, self.y), self.radius)
		
	def Update(self):
		self.x += self.vx
		self.y += self.vy
		
		if self.x < 0 or self.x + 5 > 800:
			self.vx *= -1
		if self.y < 0:
			self.vy *= -1
		self.rect.Update(self.x - self.radius, self.y - self.radius)
			
			

class BrickManager(object):
	def __init__(self):
		self.bricks = []
		self.Generate()
		
	def Render(self, screen):
		for brick in self.bricks:
			brick.Render(screen)
		
		for i in range(1, 20):
                        py.draw.line(screen, (randrange(0, 255), randrange(0, 255), randrange(0, 255)), (randrange(0, 800), randrange(0, 600)), (randrange(0, 800), randrange(0, 600)))
		
	def Generate(self):
		for i in range(0, 800/40):
			for j in range(0, 200/20):
				self.bricks.append(Brick(i*40, j*20))

class Collision(object):
	def __init__(self):
		pass
	
	def Check(self, rect1, rect2):
		if (rect1.x > rect2.x + rect2.width or
		rect1.y > rect2.y + rect2.height or
		rect1.x + rect1.width < rect2.x or
		rect1.y + rect1.height < rect2.y):
			return False
		else:
			return True
def main():
	py.init()
	screen = py.display.set_mode((800, 600))
	py.display.set_caption("Brains Destroyer by Albertitoloren")
	
	clock = py.time.Clock()
	exit = False
	clear = (0, 0, 0)
	
	ball = Ball()
	player = Player()
	bM = BrickManager()
	coll = Collision()
	
	while not exit:
		for event in py.event.get():
			if event.type == QUIT:
				exit = True
				
		screen.fill((randrange(0, 255), randrange(0, 255), randrange(0, 255)))
		player.Render(screen)
		bM.Render(screen)
		ball.Render(screen)
		player.Update()
		ball.Update()
		if coll.Check(player.rect, ball.rect):
			ball.vy *= -1
		for brick in bM.bricks:
			if coll.Check(brick.rect, ball.rect):
				ball.vy *= -1
				bM.bricks.remove(brick)
		py.display.update()
		clock.tick(60)
	return 0
		
if __name__ == "__main__":
	main()
