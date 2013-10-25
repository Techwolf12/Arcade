import sys
import os
os.environ['ARCADEROOT'] = '/home/techinc/arcade'
from subprocess import call
#import and init pygame
import pygame
from pygame.locals import * 
onrow = 6
def rel(path):
   return os.path.join(os.path.dirname(__file__),path)

config = open(rel('gamelist.conf'), 'r').read()
data = eval(config)

pygame.init() 
current = 0
startrow = 0
#create the screen
window = pygame.display.set_mode((1280, 1024),FULLSCREEN) 

pygame.mouse.set_visible(False)

def drawBox(window,x1,y1,x2,y2,color = (255, 255, 255)):   
   pygame.draw.line(window, color, (x1,y1), (x1,y2),4)
   pygame.draw.line(window, color, (x1,y1), (x2,y1),4)
   pygame.draw.line(window, color, (x2,y2), (x1,y2),4)
   pygame.draw.line(window, color, (x2,y2), (x2, y1),4)



def handelKey(event):
   global current
   global data
   global window
   global startrow
   global onrow
   if event.key == pygame.K_ESCAPE:
      sys.exit(0)
   if event.key == pygame.K_UP or event.key == pygame.K_w:
      current -= onrow
   if event.key == pygame.K_DOWN or event.key == pygame.K_s:
      current += onrow
   if event.key == pygame.K_LEFT or event.key == pygame.K_a:
      current -= 1
   if event.key == pygame.K_RIGHT or event.key == pygame.K_s:
      current += 1
   if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
      pygame.display.quit()
      call(data[current]['cmd'],shell=True)
      pygame.display.init()
      window = pygame.display.set_mode((1280, 1024),FULLSCREEN) 
      config = open(rel('gamelist.conf'), 'r').read()
      data = eval(config)
   if event.key == pygame.K_DELETE:
      del data[current]
      data =map(str,data)
      f = open(rel("gamelist.conf"),"w")
      f.write("[\n  ")
      f.write(",\n  ".join(data))
      f.write("\n]")
      f.close()
   if current < 0:
      current = 0
   if current >= len(data):
      current = len(data)-1 
   if startrow*onrow>current:
      startrow = current/onrow
   if startrow*onrow<current-onrow*4:
      startrow = (current-onrow*4)/onrow
   drawGames()



def drawGames():
   global window
   global data
   global current
   window.fill((0,0,0))
   x,y=0,0
   i = startrow * onrow
   while i < startrow+onrow*4 and i < len(data):
      if i == current:
         xc,yc = x,y
      else:
         drawBox(window,x,y,x+200,y+200)
      img = pygame.image.load(rel(data[i]['img']))        
      img = pygame.transform.smoothscale(img,(196,196))
      window.blit(img,(x+4,y+4))
      x+=200
      if x>200*(onrow-1):
         y+=200
         x = 0
      i+=1
   drawBox(window,0,800,1276,1020)
   drawBox(window,xc,yc,xc+200,yc+200,color=(255,0,0))
   desc = data[current]['disc']

   myfont = pygame.font.SysFont("monospace", 40)
   label = myfont.render( data[current]['title'], 1, (0,200,200))
   window.blit(label, (25,825))

   myfont = pygame.font.SysFont("monospace", 25)
   label = myfont.render(desc, 1, (255,255,0))
   window.blit(label, (25,880))
   pygame.display.flip() 

drawGames()
#input handling (somewhat boilerplate code):
while True: 
   for event in pygame.event.get(): 
      if event.type == pygame.QUIT: 
          sys.exit(0) 
      elif event.type == pygame.KEYDOWN:
         handelKey(event)
