import matplotlib.pyplot as plt
import matplotlib.patches as mpath
import numpy as np

figure1, ax1 = plt.subplots(2,1)
figure2, ax2 = plt.subplots(3,1)

#L = [[x1,y1,x2,y2],[x1,y1,x2,y2]]
Rect = [[0,0,6,2],[2,2,4,6],[0,6,6,8]]
print(Rect)

def surface(x1,y1,x2,y2):
    h = abs(y2-y1)
    l = abs(x2-x1)
    return h*l

def cdg_mini(x1,y1,x2,y2):
    xg = x1 + abs(x1-x2)/2
    yg = y1 + abs(y1-y2)/2
    #print("cdg intermediaire est: ",xg," ", yg )
    return xg, yg

def draw(Rect, L, Fx, Fy):
    for i in range(len(Rect)):
        x1 = Rect[i][0]
        y1 = Rect[i][1]
        x2 = Rect[i][2]
        y2 = Rect[i][3]
        
        l = abs(x2-x1)
        h = abs(y2-y1)
        
        rect = mpath.Rectangle((x1, y1), l, h, edgecolor = 'black', linewidth = 1.5)
        ax1[0].add_patch(rect)
        
        rect_vc = mpath.Rectangle((0, y1), L, h, edgecolor = 'black', linewidth = 1.5)
        ax1[1].add_patch(rect_vc)
    
    ax1[0].set_aspect('equal')
    ax1[0].autoscale_view()
    
    ax1[1].set_aspect('equal')
    ax1[1].autoscale_view()

def cdg(Rect):
    sum_cov_x = 0
    sum_cov_y = 0
    surf = 0
    for i in range(len(Rect)):
        xg, yg = cdg_mini(*Rect[i])
        
        sum_cov_x += xg*surface(*Rect[i])
        sum_cov_y += yg*surface(*Rect[i])
        
        surf += surface(*Rect[i])
        cdg_x = sum_cov_x/surf
        cdg_y = sum_cov_y/surf 
    return cdg_x, cdg_y

cdg_x, cdg_y = cdg(Rect)


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

def moment_quadratique_tot(Rect):
    Igx_tot = 0
    Igy_tot = 0
    for i in range(len(Rect)):
        xg, yg = cdg_mini(*Rect[i])
        Igx, Igy = moment_quadratique_mini(*Rect[i])
        Igx_tot += Igx + (cdg_x - xg)**2 * surface(*Rect[i])
        Igy_tot += Igy + (cdg_y - yg)**2 * surface(*Rect[i])
    return Igx_tot, Igy_tot

Igx_tot, Igy_tot = moment_quadratique_tot(Rect)

print("le moment quadratique est: Igx= ", Igx_tot, " Igy= " ,Igy_tot)


#
# Calculs N , T et Mf
#
"""
def acquisition():
    L = input("La longeur de la poutre (m) ? .... ")
    Fx=[]
    Fy=[]
    while 1 != 0:
        fx=[]
        fy=[]
        a = input("Axe de la force : ")
        if a != '':
            if a.lower() == "x":
                fx.append(float(input('La valeur de la force (N) selon X : ')))
                fx.append(float(input('la position de la force (m) : ')))
                Fx.append(fx)
            elif a.lower() == "y":
                fy.append(float(input('La valeur de la force selon Y (N) : ')))
                fy.append(float(input('la position de la force (m) : ')))
                Fy.append(fy)
            else:
                print("Erreur")
        else:
            break               
    print (Fx, Fy)
    return Fx, Fy , L
        
Fx, Fy, L = acquisition()
"""



def Mf(Fy, L):
    B_len = np.linspace(0,L,100)
    Mf = np.zeros(len(B_len))
    
    """
    #on trie Fy en fonction de la distance
    F = []
    while len(Fy) != 0:
        i_mini = 0
        for i in range(len(Fy)):
            if Fy[i][1] < Fy[i_mini][1]:
                i_mini = i
        F.append(Fy.pop(i_mini))
    """
    
    #on caclule Mf   
    for i in range(len(Mf)):
        m = 0    
        for force in Fy:
            if force[1] < B_len[i]:
                m = m + force[0]*(B_len[i] - force[1])
        Mf[i] = m
                
    #print(F)
    #print(Mf)
    return Mf, B_len

def Ty(Fy, L):
    B_len = np.linspace(0,L,100)
    Ty = np.zeros(len(B_len))
    for i in range(len(Ty)):
        f = 0    
        for force in Fy:
            if force[1] <= B_len[i]:
                f = f + force[0]
        Ty[i] = f
    return Ty

def Tx(Fx, L):
    B_len = np.linspace(0,L,100)
    Tx = np.zeros(len(B_len))
    for i in range(len(Tx)):
        f = 0    
        for force in Fx:
            if force[1] <= B_len[i]:
                f = f + force[0]
        Tx[i] = f
    return Tx


Mf, B_len = Mf([[10.0, 0.0], [-20.0, 5.0], [10.0, 10.0]], 10)
Ty = Ty([[10.0, 0.0], [-20.0, 5.0], [10.0, 10.0]], 10)
Tx = Tx([[-20.0, 0.0], [10.0, 5.0], [10.0, 10.0]], 10)

draw(Rect, 10, Tx, Ty)

figure2.subplots_adjust(hspace=0.8)

ax2[0].set_title('Moment fléchissant')
ax2[0].set_xlabel('Position selon x (m)')
ax2[0].set_ylabel('Mf (N.m)')
ax2[0].stem(B_len, Mf, markerfmt="")
ax2[0].plot(B_len, Mf)


ax2[1].set_title('Force tranchante Y')
ax2[1].set_xlabel('Position selon x (m)')
ax2[1].set_ylabel('Ty (N)')
ax2[1].stem(B_len, Ty, markerfmt="")
ax2[1].plot(B_len, Ty)

ax2[2].set_title('Force tranchante X')
ax2[2].set_xlabel('Position selon x (m)')
ax2[2].set_ylabel('Tx (N)')
ax2[2].stem(B_len, Tx, markerfmt="")
ax2[2].plot(B_len, Tx)

plt.show()