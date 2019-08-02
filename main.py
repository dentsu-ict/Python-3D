import pygame
from pygame.locals import *
import math
import sys
import random
import numpy as np
import functools

screen=0
SCREEN_SIZE=(640,480)

def SetScreen(x,y):
    scn=np.array([x,y])
    return scn

def SetVector(x,y,z):
    vec=np.array([x,y,z])
    return vec

def Normalize(vec):
    x,y,z=vec[0],vec[1],vec[2]
    vec/=distance(x,y,z)
    return vec

def distance(x,y,z):
    dist=math.sqrt(x*x+y*y+z*z)
    return dist

def ModelView(vec,matrix):
    vec=np.append(vec,1.0)
    pos=np.dot(vec,matrix)
    if pos[3]==0:
        pos[3]=0.5
    pos=pos/pos[3]
    return SetScreen(pos[0],pos[1])

def ViewPort(w,h):
    w2=w/2.0
    h2=h/2.0
    matrix=np.eye(4)
    matrix[0 , 0]= w2
    matrix[1 , 1]=-1.0 * h2
    matrix[3 , 0]= w2
    matrix[3 , 1] = h2
    return matrix

def Perspective(fovy,aspect,znear,zfar):
    radian=3.141592*fovy/180.0
    t = 1.0 / math.tan(radian/2.0)
    matrix=np.eye(4)
    matrix[0,0]=t / aspect
    matrix[1,1]=t
    matrix[2,2]=zfar / (zfar-znear)
    matrix[2,3]=1.0
    matrix[3,2]=(-1.0 * zfar * znear) / (zfar - znear)
    matrix[3, 3] = 0.0
    return matrix


def LookAt(eye, center, up):

    z = Normalize(center-eye)
    x = Normalize(np.cross(up, z))
    y = np.cross(z, x);

    eye2=SetVector(np.dot(eye, x),np.dot(eye, y),np.dot(eye, z))
    matrix=np.eye(4)
    matrix[0,0],matrix[0,1],matrix[0,2]=x[0],y[0],z[0]
    matrix[1,0],matrix[1,1],matrix[1,2]=x[1],y[1],z[1]
    matrix[2,0],matrix[2,1],matrix[2,2]=x[2],y[2],z[2]
    matrix[3,0],matrix[3,1],matrix[3,2]=-1.0*eye2[0],-1.0*eye2[1],-1.0*eye2[2]
    return matrix

def move(vec,matrix):
    vec[2]-=10
    if vec[2]<0:
        vec[2]+=1000
    src = ModelView(vec,matrix)
    if(src[0]>0 and src[0]<640 and src[1]>0 and src[1]<480):
        pygame.draw.rect(screen,(255,255,255),Rect(src[0],src[1],2,2))
    return vec

def Event_Processing(event):
    if event.type==QUIT:
        sys.exit()

def main():
    global screen
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("3D")
    fps = pygame.time.Clock()
    star=[np.array([random.randint(0,640)-320,random.randint(0,480)-240,random.randint(0,1000)]) for i in range(1000)]
    eye = SetVector(0.0, 0.0, -20.0)
    center = SetVector(0.0, 0.0, 0.0)
    up = SetVector(0.0, 1.0, 0.0)
    mat = np.eye(4)
    matrix = ViewPort(640.0, 480.0)
    mat = np.dot(matrix, mat)
    matrix = Perspective(45.0, 640.0 / 480, 1.0, 100.0)
    mat = np.dot(matrix, mat)
    matrix = LookAt(eye, center, up)
    mat = np.dot(matrix, mat)
    while True:
        fps.tick(60)
        screen.fill((0, 0, 0))
        star=list(map(functools.partial(move,matrix=mat),star))
        pygame.display.update()
        list(map(Event_Processing, pygame.event.get()))

if __name__=='__main__':
	main()
