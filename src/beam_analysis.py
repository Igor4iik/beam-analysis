import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from scipy import integrate

# Les éléments rectangulaires élémentaires composant la surface en mm
# Rect = [[x1,y1,x2,y2],[x1,y1,x2,y2]]
Rect = [[0,0,60,20],[20,20,40,60],[0,60,60,80]]

E = 200E9 # le module de Young ex: 200E9 Pa pour l'acier
L = 10 # la longueur de la poutre en metres

# La position des efforts extérieurs en newton sauf celle des supports
# F = [[force 1, position 1],[force 2, position 2], ...]
Fy = [[-20.0, 5.0], [-10.0, 2.0], [40.0, 8.0]]
Fx = [[10.0, 5.0]]

# La position et le type des supports
# attention, le système doit rester isostatique
Pos_supp = [[1,'pin'], [7,'roller']]



figure1, ax1 = plt.subplots(3,1)
figure2, ax2 = plt.subplots(3,1)

for coord in Rect:
    for i in range(4):
        coord[i] = coord[i]*0.001
      
def surface(x1,y1,x2,y2):
    h = abs(y2-y1)
    l = abs(x2-x1)
    return h*l

def cdg_mini(x1,y1,x2,y2):
    xg = (x1 + x2)/2
    yg = (y1 + y2)/2
    return xg, yg

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


def Rect_draw(Rect):
    for i in range(len(Rect)):
        x1 = Rect[i][0]
        y1 = Rect[i][1]
        x2 = Rect[i][2]
        y2 = Rect[i][3]
        
        l = abs(x2-x1)
        h = abs(y2-y1)
        
        rect = patches.Rectangle((min(x1,x2), min(y1,y2)), l, h, edgecolor = 'black', linewidth = 1.5)
        ax1[0].add_patch(rect)

def Arrow_draw(L, Fx, Fy, color = 'red'):
    ax1[1].plot([0,L], [0,0], linewidth = 4)
    
    Fx_max = abs(Fx[0][0])
    for force in Fx:
        if abs(force[0]) > Fx_max:
            Fx_max = abs(force[0])
            
    Fy_max = abs(Fy[0][0])
    for force in Fy:
        if abs(force[0]) > Fy_max:
            Fy_max = abs(force[0])
            
    scale = 2

    for force in Fx:
        ax1[1].annotate(f"{force[0]}N", xy = (force[1],0), xytext= (force[1] - 1*( force[0]/Fx_max),0), arrowprops = dict(facecolor=color))
    for force in Fy:
        ax1[1].annotate(f"{force[0]}N", xy = (force[1],0), xytext= (force[1], -1*scale*(force[0]/Fy_max)), arrowprops = dict(facecolor=color)) 
        
    
    ax1[0].set_aspect('equal')
    ax1[0].autoscale_view()
    ax1[0].set_title('La section')
    ax1[0].set_xlabel('x (m)')
    ax1[0].set_ylabel('y (m)')
    
    ax1[1].set_xlim(-1, L + 1)
    ax1[1].set_ylim(-2, 2)
    ax1[1].autoscale_view()
    ax1[1].set_title('La position des efforts')
    ax1[1].set_xlabel('x (m)')
    

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


#
# Calcul des réactions d'appui
#

def resSupport(Pos_supp, Fx, Fy):
    Pos_inconnu = []
    for support in Pos_supp:
        if support[1] == 'pin':
            Pos_inconnu.append([support[0], 'Fx'])
            Pos_inconnu.append([support[0], 'Fy'])
        elif support[1] == 'roller':
            Pos_inconnu.append([support[0], 'Fy'])
        else:
            raise ValueError(f"'{support[1]}' : Support inconnu, choisir parmis ['roller', 'pin']")
        
    TRS_x = []
    TRS_y = []
    TMS_z = []
    for inconnu in Pos_inconnu:
        if inconnu[1] == 'Fx':
            TRS_x.append(1)
            TRS_y.append(0)
            TMS_z.append(0)

        elif inconnu[1] == 'Fy':
            TRS_y.append(1)
            TRS_x.append(0)
            TMS_z.append(inconnu[0])
    
    a = np.array([TRS_x, TRS_y, TMS_z])
    known_Fy = 0
    known_Fx = 0
    known_Mz = 0
    for force in Fy:
        known_Fy += (-1)*force[0]
    for force in Fx:
        known_Fx += (-1)*force[0]
    for force in Fy:
        known_Mz += (-1)*force[0]*force[1]
    
    b = np.array([known_Fx, known_Fy, known_Mz])
    
    n_unknowns = len(Pos_inconnu)
    if np.linalg.matrix_rank(a) < n_unknowns: #si il y a + de inconnus que d'equations, on ne peut pas resoudre
        raise ValueError('Le systeme doit rester isostatique!')
    
    F_support = np.linalg.solve(a, b)
    #print(F_support)
    
    return [F_support[0], Pos_inconnu[0][0]], [F_support[1], Pos_inconnu[1][0]], [F_support[2], Pos_inconnu[2][0]]
    
    
#
# Calculs N , T et Mf
#

def bending_moment(Fy, L):
    B_len = np.linspace(0,L,100)
    Mf = np.zeros(len(B_len))
    
    #on calcule Mf   
    for i in range(len(Mf)):
        m = 0    
        for force in Fy:
            if force[1] < B_len[i]:
                m = m + force[0]*(B_len[i] - force[1])
        Mf[i] = m
                
    #print(F)
    #print(Mf)
    return Mf, B_len

def shear_force(Fy, L):
    B_len = np.linspace(0,L,100)
    Ty = np.zeros(len(B_len))
    for i in range(len(Ty)):
        f = 0    
        for force in Fy:
            if force[1] <= B_len[i]:
                f = f + force[0]
        Ty[i] = f
    return Ty

def normal_force(Fx, L):
    B_len = np.linspace(0,L,100)
    Tx = np.zeros(len(B_len))
    for i in range(len(Tx)):
        f = 0    
        for force in Fx:
            if force[1] <= B_len[i]:
                f = f + force[0]
        Tx[i] = f
    return Tx


# Integration pour trouver la déformée

def deformee(Mf, B_len, Moment_quadratique, Pos_supp, E):
    courbure = Mf/(E*Moment_quadratique)
    
    #première intégration
    angles = integrate.cumulative_trapezoid(courbure, B_len, initial=0)
    
    #deuxième intégration
    y1 = integrate.cumulative_trapezoid(angles, B_len, initial=0)
    
    #trouvons les constantes
    xA = Pos_supp[0][0]
    xB = Pos_supp[1][0]
    
    y1_A = np.interp(xA, B_len, y1)
    y1_B = np.interp(xB, B_len, y1)

    C1 = (y1_B- y1_A) / (xA - xB)
    C2 = -y1_B - C1*xB
    
    #calcul final
    y = np.zeros(len(Mf))
    for i in range(len(y)):
        y[i] = y1[i] + C1*B_len[i] + C2
        
    print(f"La flèche maximale est : {round(np.max(abs(y)), 5)} m ")
    return y

Arrow_draw(L, Fx, Fy, 'red')

cdg_x, cdg_y = cdg(Rect)
print(f"le centre de gravité est: x= {cdg_x}m, y= {cdg_y}m")

Igx_tot, Igy_tot = moment_quadratique_tot(Rect)
print(f"le moment quadratique est: Igx= {round(Igx_tot, 3)}m^4, Igy= {round(Igy_tot, 3)}m^4")

f1, f2, f3 = resSupport(Pos_supp, Fx, Fy)
Fx.append(f1)
Fy.append(f2)
Fy.append(f3)
Arrow_draw(L, [f1], [f2, f3], 'blue')

Mf_values, B_len = bending_moment(Fy, L)
Ty_values = shear_force(Fy, L)
Tx_values = normal_force(Fx, L)

Rect_draw(Rect)

figure1.subplots_adjust(hspace=0.8)
figure2.subplots_adjust(hspace=0.8)

ax2[0].set_title('Moment fléchissant')
ax2[0].set_xlabel('Position selon x (m)')
ax2[0].set_ylabel('Mf (N.m)')
ax2[0].stem(B_len, Mf_values, markerfmt="")
ax2[0].plot(B_len, Mf_values)

ax2[1].set_title('Force tranchante Y')
ax2[1].set_xlabel('Position selon x (m)')
ax2[1].set_ylabel('Ty (N)')
ax2[1].stem(B_len, Ty_values, markerfmt="")
ax2[1].plot(B_len, Ty_values)

ax2[2].set_title('Effort normal N')
ax2[2].set_xlabel('Position selon x (m)')
ax2[2].set_ylabel('Tx (N)')
ax2[2].stem(B_len, Tx_values, markerfmt="")
ax2[2].plot(B_len, Tx_values)

ax1[2].set_title('La flèche')
ax1[2].set_xlabel('Position selon x (m)')
ax1[2].set_ylabel('Flèche (m)')
ax1[2].plot([0,L], [0,0], '--', linewidth = 1)
ax1[2].plot(B_len, deformee(Mf_values, B_len, Igx_tot, Pos_supp, E))

plt.show()