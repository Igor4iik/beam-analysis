import turtle as trt

#L = [[x1,y1,x2,y2],[x1,y1,x2,y2]]
L = [[0,0,6,2],[2,2,4,6],[0,6,6,8]]

print(L)

def surface(x1,y1,x2,y2):
    h = abs(y2-y1)
    l = abs(x2-x1)
    return h*l

def cdg_mini(x1,y1,x2,y2):
    xg = x1 + abs(x1-x2)/2
    yg = y1 + abs(y1-y2)/2
    #print("cdg intermediaire est: ",xg," ", yg )
    return xg, yg

def draw(L):
    trt.color("black", "orange")
    trt.begin_fill()
    zoom = 10
    for i in range(len(L)):
        trt.setheading(0)
        
        x1 = L[i][0]
        y1 = L[i][1]
        x2 = L[i][2]
        y2 = L[i][3]
        
        l = abs(x2-x1)
        h = abs(y2-y1)
        trt.teleport(x1*zoom,y1*zoom)
        #print("x1= ",x1,"y1= ",y1)
        
        for i in range(2):
            trt.forward(l*zoom)
            trt.left(90)
            trt.forward(h*zoom)
            trt.left(90)
    trt.end_fill()
        
draw(L)



def cdg(L):
    sum_cov_x = 0
    sum_cov_y = 0
    surf = 0
    for i in range(len(L)):
        xg, yg = cdg_mini(*L[i])
        
        sum_cov_x += xg*surface(*L[i])
        sum_cov_y += yg*surface(*L[i])
        
        surf += surface(*L[i])
        cdg_x = sum_cov_x/surf
        cdg_y = sum_cov_y/surf 
    return cdg_x, cdg_y

cdg_x, cdg_y = cdg(L)


print("le centre de gravite est: x=", cdg_x, " y=" ,cdg_y)

#
# Calcul du moment quadratique
#

def moment_quadratique_mini(x1,y1,x2,y2):
    h = abs(y2-y1)
    l = abs(x2-x1)
    Igx = (h**3*l)/12
    Igy = (h*l**3)/12
    return Igx, Igy

def moment_quadratique_tot(L):
    Igx_tot = 0
    Igy_tot = 0
    for i in range(len(L)):
        xg, yg = cdg_mini(*L[i])
        Igx, Igy = moment_quadratique_mini(*L[i])
        Igx_tot += Igx + (cdg_x - xg)**2 * surface(*L[i])
        Igy_tot += Igy + (cdg_y - yg)**2 * surface(*L[i])
    return Igx_tot, Igy_tot

Igx_tot, Igy_tot = moment_quadratique_tot(L)

print("le moment quadratique est: Igx= ", Igx_tot, " Igy= " ,Igy_tot)


