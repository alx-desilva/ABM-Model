from matplotlib import pyplot as plt
import numpy as np
import math



def preset():
    global Velx, Vely, speed
    Targetx = 0
    Targety = 0
    startPointT = (Targetx,Targety)
    Velx = 1
    Vely = 2
    velSlope = Vely/Velx

    Interceptorx = 7
    Interceptory = 0
    startPointI = (Interceptorx,Interceptory)
    speed = 4

    return startPointT, startPointI, velSlope

def setup():
    global Velx, Vely, speed

    Targetx = int(input("Target Starting Pos X"))
    Targety = int(input("Target Starting Pos Y"))
    startPointT = (Targetx,Targety)
    Velx = int(input("Target Velocity X"))
    Vely = int(input("Target Velocity Y"))
    velSlope = Vely/Velx

    Interceptorx = int(input("Interceptor Starting Pos X"))
    Interceptory = int(input("Interceptor Starting Pos Y"))
    startPointI = (Interceptorx,Interceptory)
    speed = int(input("Interceptor Speed"))

    return startPointT, startPointI, velSlope




def calculate_tragectory(Targetx,Targety,Interceptorx,Interceptory):
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
            print(f'Quadratic {tval} is possible')
        else:
            print(f"Quadratic {tval} is not possible")

    #This should return the point of contact
    PocX = Targetx + Velx*t
    PocY = Targety + Vely*t

    return PocX,PocY

#Angle to point of contact
#dirX = PocX - Interceptorx
#dirY = PocY - Interceptory

#angle_rad = math.atan2(dirX,dirY)
#angle_degrees = math.degrees(angle_rad)



def graph(PocX,PocY,startPointT,startPointI,slope):
    I_slope = (PocY - startPointI[1])/ (PocX - startPointI[0])
    I_endPoint = (PocX,PocY)
    plt.scatter(PocX,PocY, color="r", label="Interceptor Point of Contact w target")
    plt.scatter(startPointI[0], startPointT[1],color="grey",label="Interceptor Starting Pos")
    plt.scatter(startPointT[0],startPointT[1],color="black", label="Target Starting Point")
    plt.axline(xy1=startPointT,slope=slope,label="Target Tragectory")
    plt.axline(xy1=startPointI, xy2=I_endPoint, label="Interceptor Tragectory",linestyle="--") #slope=I_slope

    plt.legend()
    plt.show()

def main():
    #At some point at a "load" function to do a preset one for testing
    LorC = input("Load, Custom, or break?")
    print(LorC.lower())
    if LorC.lower() == "load":
        TargetPos, InterceptorPos, velSlope = preset()
    elif LorC.lower() == "custom":
        TargetPos, InterceptorPos, velSlope = setup()
    elif LorC.lower() == "break":
        return False

    POCx, POCy = calculate_tragectory(TargetPos[0],TargetPos[1],InterceptorPos[0],InterceptorPos[1])
    graph(POCx,POCy,TargetPos,InterceptorPos,velSlope)


while True:
    print("Tragectory Calculator")
    print("----------------------")
    out = main()
    if out == False:
        break