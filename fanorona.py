import turtle
from math import sqrt

turtle.setup(700,700)
pen=turtle.Turtle()
s=0
t=[]
XX=[]
YY=[]
count=0
head = turtle.Turtle()
X=[-300,0,300]
Y=[-300,0,300]
u=0

id=0
def tracelign():
    pen.color("black")
    pen.goto(-300,0)
    pen.goto(-300,300)
    #pen.goto(-300,600)
    pen.goto(300,300)
    pen.goto(300,-300)
    pen.goto(-300,-300)
    pen.goto(300,300)
    pen.goto(-300,300)
    pen.goto(300,-300)
    pen.goto(0,-300)
    pen.goto(0,300)
    pen.goto(-300,300)
    pen.goto(-300,0)
    pen.goto(300,0)
    pen.goto(-300,0)
    pen.goto(-300,-300)

def point(a,b,c):
    t.append(turtle.Turtle())
    t[c].shape("circle")
    t[c].color("green")
    t[c].goto(a,b)
    XX.append(a)
    YY.append(b)
    print(XX,YY)
    head.clear()    
    

def click(x,y):
    global id,s,count,u
    l,c = int(x), int(y)
    id = 0
    for i in range(3):
        if l<X[i]+10 and l>X[i]-10:
            print("x = ",X[i])
            x=i
            for j in range(3):
                if c<Y[j]+10 and c>Y[j]-10:
                    print("y = ",Y[j])
                    y=j
                    id=1
    print(id)
    if id ==1:
        if s<3:
            print("goto",X[x],",",Y[y])
            point(X[x],Y[y],s)
            s=s+1
        else :
            if count==0:
                for i in range (3):
                    if X[x]==XX[i] and Y[y]==YY[i]:
                        print("dans le point.peut deplacer au deuxieme click pour ",(t[i]))
                        count = 1
                        u=i
                        continue
            elif count==1:
                t[u].goto(X[x],Y[y])
                XX[u]=X[x]
                YY[u]=Y[y] 
                count=0
    print("count : ",count) 
    id=0
    

tracelign()

turtle.onscreenclick(click,1)
turtle.listen()
turtle.mainloop()
