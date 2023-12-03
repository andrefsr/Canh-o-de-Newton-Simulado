from vpython import *
#Web VPython 3.2
from vpython import *

### Cena
scene.background = vector(0.8784313725490196,0.8274509803921568,0.6705882352941176)
scene.userzoom = True
scene.userpan = True
scene.userspin = False

### Botões
executar = False
def lancar(d):
    global executar
    executar = True
    c = 1
    d.text = 'Continuar'
    b.start()
button(text='Lançar!',bind = lancar)

def pausar():
    global executar
    if executar == True:
        executar = not executar
        b.stop()
button(text='Pausar',bind = pausar)

def limpartrail():
    global executar
    if executar == False:
        b.clear()
button(text='Limpar trajetória',bind=limpartrail)

### Dados 
G = 6.67e-11 ### Constante [m^3/kg*s^2]
Me = 5.97e24 ### Massa da Terra [Kg]
ms = 43#742.20126    ### Massa do Satelite [kg]
Re = 6.37e6  ### Raio da Terra [m]
rp = 0.25 # [m]
A = 3.1415*rp*rp #[m^2]
C = 0.002 # [1]
g = 9.8 # [m/s^2]
R = 287.54 # [J/(kg*K)]
M = 0.0289
angulo = pi/2

### Objetos
Terra = sphere(pos=vector(0,0,0), radius=Re,)
Terra.opacity = 0
Terra.m = Me

seta = arrow(pos = vector(0,6000+Re,0), axis = vector(-1,0,0),length = 4*0.05*Re,color = color.red,shaftwidth = 0.2*2*0.05*Re)
textura = box(pos=vector(0, 0, 0), size=vector(2*Re, 2*Re, 1000), texture = 'https://i.imgur.com/dZlXnyw.png',shininess=0)

Satelite = sphere(pos=vector(0,6000+Re,0), radius=0.05*Re, shininess = 0, color=color.black)#, make_trail=True,trail_type="points",interval=10)
b = attach_trail(Satelite)
b.color = color.black
b.trail_type = 'points'
b.interval = 1000000000000
Satelite.m = ms
Satelite.v = vector(0.1,0.1,0)

def altura(S):
    if executar == False:
        Satelite.pos.y = S.value
        seta.pos.y = S.value
        altura_caption.text = 'Altura = '+'{:1.0f}'.format(h.value-Re)+' m'+'\n\n'
h = slider(bind=altura,min=6000+Re,max=(47000+Re),value=0) ##calibrar value
altura_caption = wtext(text = 'Altura = '+'{:1.0f}'.format((h.value-Re)) + ' m'+'\n\n')

#l = 0
hini = Satelite.pos.y
#def reset():
    #global executar
    #if executar == False:
        #Satelite.pos = vector(0,hini,0) ### Resolver
        #seta.opacity = 1
        #b.stop()
        #Satelite.v = vector(0.1,0.1,0)
        #l = 1
#button(text='Reset',bind=reset)

def dirseta(ang):
    angle = theta.value
    rot = vector(-0.05*Re*cos(ang.value),0.05*Re*sin(ang.value),0)
    seta.axis = rot
    seta.length = 4*0.05*Re

def angini(O):
    if executar == False:
        angulo = O.value
        theta_caption.text = 'Ângulo de lançamento = '+'{:1.0f}'.format(theta.value*180/pi)+' °'+'\n\n'
        dirseta(theta)
theta = slider(bind=angini,min=0,max=pi/2,value=0)
theta_caption = wtext(text = 'Ângulo de lançamento = '+'{:1.0f}'.format(theta.value*180/pi)+' °'+'\n\n')

def velini(A,angulo): 
    if executar == False:
        anglanc = theta.value
        Satelite.v = vector(-A.value*cos(anglanc),A.value*sin(anglanc),0)
        vel_caption.text = 'Velocidade inicial = '+'{:2.0f}'.format(vel.value)+' m/s'+'\n\n'
        Satelite.p = Satelite.m*Satelite.v
vel = slider(bind=velini,min=0.1,max=10000,value=0) ##calibrar value
vel_caption = wtext(text = 'Velocidade inicial = '+'{:2.0f}'.format(vel.value)+' m/s'+'\n\n')

Legenda = wtext(text='Posição da câmera: ')
def cameraS():
    global cameraS
    scene.camera.follow(Satelite)
button(text='Satelite',bind = cameraS)

def cameraT():
    global cameraT
    scene.camera.follow(Terra)
button(text='Terra',bind = cameraT)

### Calculo da velocidade de escape
def velscape(wi):
    hin = float(wi.text)
    hvscape = Re + hin
    def f(v):
        fg = (G*ms*Me)/(hvscape**2)
        func = (G*ms*Me)/(hvscape**2)  - (ms*v**2)/hvscape  # 0.5*rho1*C*(A/ms)*(v)**2
        return func
    dh = 0.00001
    def cd(x):
        dcd = (f(x+dh)-f(x-dh))/(2*dh)
        return dcd
    prec = 10**(-7)
    x0 = 5000
    n = 0
    while n<1000:
        x = x0 - (f(x0)/cd(x0))
        if abs(x-x0) < prec:
            break
        else:
            x0 = x
        n += 1
    if hin <= 11000:
        tal = -6.5*10**(-3)
        To = 288
        rho0 = 1.225
        T = To + tal*hin
        rho1 = rho0*(T/To)**(-((g/(R*tal))+1))
        Fdrag = 0.5*rho1*C*(A/ms)*(x**2)
        Fc = 3.53*Fdrag+121.46
    else:
        if hin <= 25000:
            rho0 = 0.3629
            T = 216.5
            rho1 = rho0*exp((-g*(hin-11000))/(R*T))
            Fdrag = 0.5*rho1*C*(A/ms)*(x**2)
            Fc = 3.93*Fdrag+83.23
        else:
            if hin <= 47000: 
                tal = 0.003
                To = 216.5
                rho0 = 0.0399
                T = To+tal*(hin-25000)
                rho1 = rho0*(T/To)**(-((g/(R*tal))-1))
                Fdrag = 0.5*rho1*C*(A/ms)*(x**2)
                Fc = 9.93*Fdrag+17.98
    velscape = x+Fc
    def arredondar(numero):
        resto = numero % 10
        arredondamento = 10 - resto
        if resto >= 5:
            resultado = numero + arredondamento
        else:
            resultado = numero - resto
        return resultado
    if hin < 6000 or hin > 47000:
        print('Digite um valor entre 6000 e 47000 metros!!')
    else:
        print('A velocidade de escape para a altura de', '{:1.0f}'.format(hin) ,'m é','{:1.0f}'.format(arredondar(velscape)),'m/s')
wtext(text = '\n\nCalculadora de velocidade de escape: ')
alturaI_input = winput(text = 'Altura desejada',bind=velscape,width=105)

### Execução
t = 0
dt = 0.008
k = 0
e = 0
cont = 0
cont1 = 0
tt = 0
Satelite.p = Satelite.v*Satelite.m
while True:
    rate(100)
    if executar:
        seta.opacity = 0
        ### Vetor r
        rv = Satelite.pos - Terra.pos
        h = mag(rv) - Re
        vr = Satelite.p/Satelite.m
        if mag(vr)/310 <= 1: ### Velocidade menor que Mach 1
            C = 0.47
        if h <= 100:
            h = 0
            executar = False
        ### Forca sobre o satelite
        if h <= 11000: ### Troposfera
            ### Parametros de entrada
            tal = -6.5*10**(-3)
            To = 288
            Po = 101325
            rho0 = 1.225
            #Parametros de saida
            T = To + tal*h
            P = Po*(T/To)**(-(g/(R*tal)))
            rho = rho0*(T/To)**(-((g/(R*tal))+1))
            #print(rho)
        else:
            if h <= 25000: ### Baixa estratosfera
                ### Parametros de entrada
                Po = 22552
                rho0 = 0.3629
                ### Parametros de saída
                T = 216.5
                P = Po*exp((-g*(h-11000))/(R*T))
                rho = rho0*exp((-g*(h-11000))/(R*T))
            else:
                if h <= 47000: ### Alta estratosfera
                    ### Parametros de saída
                    tal = 0.003
                    To = 216.5
                    Po = 2481
                    rho0 = 0.0399
                    ### Parametros de saída
                    T = To+tal*(h-25000)
                    P = Po*(T/To)**(-(g/(R*tal)))
                    rho = rho0*(T/To)**(-((g/(R*tal))-1))
                else:
                    rho = 0
        Fd = -0.5*rho*C*(A/ms)*(mag(vr)**2)*norm(vr)
        Fg = ((-G*Terra.m*Satelite.m)/(((mag(rv)**2))))*norm(rv)
        Fres = Fg + Fd 
        ### Momento linear do satelite
        Satelite.p = Satelite.p + (Fres*t)
        ### Posicao do satelite
        sx0 = Satelite.pos.x
        sy0 = Satelite.pos.y
        Satelite.pos = Satelite.pos + (Satelite.p/Satelite.m)*t
        if k == 0:
            if Satelite.pos.x > sx0:
                Xmax = sx0
                c = (mag(rv)**2-Xmax**2)**0.5
                a = c+hini
                e = c/a
                k = 1
        print('\n\n\n\n\n','Altura:','{:1.0f}'.format(h/1000),'km',' Velocidade:','{:1.0f}'.format(mag(vr)/3.6),'km/h')
        if k == 1:
            if Satelite.pos.y <= sy0:
                if Satelite.pos.x <= sx0:
                    cont = 1
        if cont1 == 0:
            TT = tt
        if cont == 1:
            print(' Período da órbita:','{:1.2f}'.format(TT/3600),'h',' excentricidade:',e)
            cont1 = 1
        t += dt
        tt+=t