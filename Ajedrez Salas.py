# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 14:29:43 2014
Salaschess
@author: JuanLuis
"""
Nivel = 2
ProfundidadEnAtaques = -2
InstruccionesSalir = ("salir", "exit", "terminar", "quit", "s", "q")
InstruccionesNueva = ("nueva", "n", "new", "empezar", "start", "borrar")
InstruccionesRectificar = ("r", "atrás", "atras", "back", "rectificar", "jugada", "deshacer")
Valor = {' ' : 0.0, 'P' : 20.0, 'A' : 60.0, 'C' : 60.0, 'T' : 100.0, 'Q' : 160.0, 'R' : 9999.9} # Valor de cada tipo de pieza
ValorAvanzarPeon = 1.5
ValorEnroque = 30
ValorCasilla = ((0,0,0,0,0,0,0,0),
                (0,1,1,1,1,1,1,0),
                (0,1,2,2,2,2,1,0),
                (0,1,2,3,3,2,1,0),
                (0,1,2,3,3,2,1,0),
                (0,1,2,2,2,2,1,0),
                (0,1,1,1,1,1,1,0),
                (0,0,0,0,0,0,0,0))
CoeficienteDeReduccion = 0.95
abc = "abcdefgh12345678"
ValorTotalJugador = {'B' : 0, 'N' : 0}
contador = 0
pausas = False

DireccionesAlfil = {(i,j) for i in (-1,1) for j in (-1,1)}
DireccionesTorre = {(i,0) for i in (-1,1)} | {(0,j) for j in (-1,1)}
DireccionesRey = DireccionesReina = DireccionesAlfil | DireccionesTorre
DireccionesCaballo = {(i,j) for i in (-1,1) for j in (-2,2)} | {(i,j) for i in (-2,2) for j in (-1,1)} 
Tablero, ListaJugadas, PilaJugadas, ListaTableros = [], [], [], []
CasillaVacia = ' '*2
Turno = 'B'
import random

def nueva_partida():
    global Tablero, Turno, ValorTotalJugador, PilaJugadas
    Tablero = [['TN','CN','AN','QN','RN','AN','CN','TN'],
               ['PN','PN','PN','PN','PN','PN','PN','PN'], 
               ['  ','  ','  ','  ','  ','  ','  ','  '], 
               ['  ','  ','  ','  ','  ','  ','  ','  '], 
               ['  ','  ','  ','  ','  ','  ','  ','  '], 
               ['  ','  ','  ','  ','  ','  ','  ','  '], 
               ['PB','PB','PB','PB','PB','PB','PB','PB'], 
               ['TB','CB','AB','QB','RB','AB','CB','TB']]
    Turno = 'B'
    ValorTotalJugador['B'], ValorTotalJugador['N'] = ValorTotalFichas('B'), ValorTotalFichas('N')
    PilaJugadas = []
    #if DireccionTablero: Tablero = list(fila[::-1] for fila in Tablero[::-1])
    #ver_tablero()

empaquetar = lambda Tablero: tuple(tuple(fila) for fila in Tablero) 
       
def ver_ficha(F):
    if F[1] == 'N': return F[0].lower()
    elif F[1] == 'B': return F[0].upper()
    else: return ' '
               
sumar = lambda a, b: (a[0]+b[0], a[1]+b[1])
coordOk = lambda i, j: (0 <= i <= 7) and (0 <= j <= 7)

def ver_tablero(marco = False):
    global Tablero, abc
    print '   ', list(abc[:8].upper())
    if marco: print("   " + "*"*40)
    for i in range(8):
        print abc[15-i], " |  " + " |  ".join(list(ver_ficha(Tablero[i][j]) for j in range(8))), "| ", abc[15-i]
        print "   " + "-"*40
    if marco: print("   " + "*"*40)
    print '   ', list(abc[:8].upper())

def ver_listaJugadas(color):
    LJ = Jugadas(color)
    Fichas = []
    for jugada in LJ: 
        if not (jugada[0] in Fichas): 
            Fichas.append(jugada[0])
    for ficha in Fichas:
        print(tipoFicha(ficha), ficha)
        print(list(jugada[1] for jugada in LJ if jugada[0] == ficha))       

def Jugadas_1casilla(c, direcciones):
    global Tablero
    LJ = []    
    i, j = c
    color = Tablero[i][j][1]
    for d in direcciones:
        i, j = sumar(c, d)        
        if coordOk(i,j) and colorFicha(i,j) != color: LJ += [(c, (i,j))]
    return LJ # Devuelve la lista de todas las posibles jugadas que se pueden hacer desde la posición c del tablero a distancia de una casilla en las direcciones dadas
    
def Jugadas_ncasillas(c, direcciones):
    global Tablero, CasillaVacia
    LJ = []    
    i, j = c
    color = colorFicha(i,j)
    for d in direcciones:
        i, j = sumar(c, d)    
        while coordOk(i,j) and Tablero[i][j] == CasillaVacia:
            LJ += [(c, (i,j))]
            i, j = sumar((i,j), d)
        if coordOk(i,j) and colorFicha(i,j) != color: LJ += [(c, (i,j))]
    return LJ # Devuelve lo mismo que Jugadas_1casilla, pero pudiendo desplazarse más de una casilla en cada una de las direcciones dadas
    
def Jugadas_peon(i,j):
    global Tablero, CasillaVacia    
    LJ = []
    UnPaso = 1
    Oponente = 'B'
    if colorFicha(i, j) == 'B': 
        UnPaso = -1
        Oponente = 'N'
    if coordOk(i+UnPaso,j) and Tablero[i+UnPaso][j] == CasillaVacia: 
        LJ += [((i,j), (i+UnPaso,j))]
        if (i==1 or i==6) and coordOk(i+2*UnPaso,j) and Tablero[i+2*UnPaso][j] == CasillaVacia:
            LJ += [((i,j), (i+2*UnPaso,j))]
    for k in (-1, 1):
        if coordOk(i+UnPaso,j+k) and colorFicha(i+UnPaso,j+k) == Oponente:
            LJ += [((i,j), (i+UnPaso,j+k))]
    return LJ # Dadas las coordenadas de un peón, devuelve todas las posibles jugadas que puede realizar. Falta considerar comer al paso
    
def Jugadas_enroque(i,j):
    global Tablero, CasillaVacia
    LJ = []
    if (i,j) == (7,4) or (i,j) == (0,4):
        if tipoFicha(i,0) == 'T' and (
            Tablero[i][1] == Tablero[i][2] == Tablero[i][3] == CasillaVacia) and (
            colorFicha(i,4) == colorFicha(i,0)):
            LJ += [((i,4), (i,2))]
        if tipoFicha(i,7) == 'T' and (
            Tablero[i][6] == Tablero[i][5] == CasillaVacia) and (
            colorFicha(i,4) == colorFicha(i,7)):
            LJ += [((i,4), (i,6))]
    
    return LJ # Dadas las coordenadas de un rey, devuelve aquellos enroques que puede realizar. Falta considerar algunas restricciones para poder hacer el enroque

def colorFicha(i,j='None'):
    if type(i) == type(" "): return i[1]
    elif type(i) == tuple or type(i) == list: return Tablero[i[0]][i[1]][1]  
    else: return Tablero[i][j][1]

def tipoFicha(i,j='None'):
    if type(i) == type(" "): return i[0]
    elif type(i) == tuple or type(i) == list: return Tablero[i[0]][i[1]][0]  
    else: return Tablero[i][j][0]
     
def Jugadas(color):
    LJ = []
    for i in range(8):
        for j in range(8):
            if colorFicha(i,j) == color:
                if tipoFicha(i,j) == "P": 
                    LJ += Jugadas_peon(i,j)
                elif tipoFicha(i,j) == "T": 
                    LJ += Jugadas_ncasillas((i,j), DireccionesTorre)
                elif tipoFicha(i,j) == "C":
                    LJ += Jugadas_1casilla((i,j), DireccionesCaballo)
                elif tipoFicha(i,j) == "A":
                    LJ += Jugadas_ncasillas((i,j), DireccionesAlfil)
                elif tipoFicha(i,j) == "R":
                    LJ += Jugadas_1casilla((i,j), DireccionesRey)
                    LJ += Jugadas_enroque(i,j)
                elif tipoFicha(i,j) == "Q":
                    LJ += Jugadas_ncasillas((i,j), DireccionesReina)
    return LJ # Devuelve la lista de todas las posibles jugadas que puede hacer un jugador en una situación de partida

def mover(jugada):
    global Tablero, PilaJugadas, CasillaVacia
    ((i0,j0), (i1,j1)) = jugada
    PilaJugadas.append((jugada, Tablero[i0][j0], Tablero[i1][j1]),)
    Tablero[i0][j0], Tablero[i1][j1] = CasillaVacia, Tablero[i0][j0]
    if (i1 == 7 or i1 == 0) and tipoFicha(i1, j1) == 'P': Tablero[i1][j1] = 'Q'+colorFicha(i1,j1) # peón se hace reina
    if tipoFicha(i1, j1) == 'R' and abs(j0-j1) == 2: # enroque
        if j1 == 2: 
            Tablero[i1][0], Tablero[i1][3] = CasillaVacia, 'T'+colorFicha(i1,j1)
        elif j1 == 6:
            Tablero[i1][7], Tablero[i1][5] = CasillaVacia, 'T'+colorFicha(i1,j1)

def rectificar():
    global Tablero, PilaJugadas, CasillaVacia
    J, PilaJugadas = PilaJugadas[-1], PilaJugadas[:-1]
    ((i0,j0), (i1,j1)), FichaA, FichaB = J
    Tablero[i0][j0], Tablero[i1][j1] = FichaA, FichaB
    if FichaA[0] == 'R' and abs(j1-j0) == 2: #enroque
        if j1 == 2:
            Tablero[i1][0], Tablero[i1][3] = 'T'+colorFicha(FichaA), CasillaVacia
        elif j1 == 6:
            Tablero[i1][7], Tablero[i1][5] = 'T'+colorFicha(FichaA), CasillaVacia   

def traducir(c): # Traduce una coordenada tipo alfanumérica a coordenada numéricas
    global abc
    x = abc.find(c)
    r = x if (0 <= x <= 7) else 15-x
    return r

def escribir(jugada): # Traduce una jugada escrita en coordenadas numéricas a coordenadas alfanuméricas
    global abc   
    if jugada == 0: return "ninguna jugada"
    (i0,j0), (i1,j1) = jugada
    return "".join((abc[j0], abc[15-i0], abc[j1], abc[15-i1]))
    
contrario = lambda T: 'N' if T == 'B' else 'B'

def ValorTotalFichas(color):
    global Tablero, Valor   
    V = 0    
    for i in range(8):
        for j in range(8):
            if Tablero[i][j][1] == color:
                V += Valor[Tablero[i][j][0]]
    return V
    
def valorarJugada(jugada, FichaA, n_, T_):
    global Valor, ValorTotalJugador, ValorAvanzarPeon, ValorCasilla, CasillaVacia, CoeficienteDeReduccion, ProfundidadEnAtaques
    n, T = n_, T_
    (i0,j0), (i1,j1) = jugada
    FichaB = Tablero[i1][j1]
    #Valor de la pieza comida:
    V = Valor[FichaB[0]] * ValorTotalJugador[T]/ValorTotalJugador[contrario(T)] # El valor de una ficha se modifica en función de la superioridad numérica de uno u otro jugador
    if FichaB == CasillaVacia:
        V += ValorCasilla[i1][j1] - ValorCasilla[i0][j0]
    else:
        V += 2*ValorCasilla[i1][j1] - ValorCasilla[i0][j0]        
    if FichaA[0] == 'P':      
        if i1 == 0 or i1 == 7: V += Valor['Q'] - Valor['P']
        else: V += ValorAvanzarPeon
    if FichaA[0] == 'R' and abs(j1-j0) == 2: V += ValorEnroque
    if n > 0 or (Tablero[i1][j1] != CasillaVacia and n > ProfundidadEnAtaques):
        mover(jugada)
        T = contrario(T)
        n -= 1
        LJ = Jugadas(T)
        if len(LJ) > 0:
            j = LJ[0]
            M = valorarJugada(j, Tablero[j[0][0]][j[0][1]], n, T)*CoeficienteDeReduccion
            if len(LJ) > 1: 
                for j in LJ[1:]: M = max(M, valorarJugada(j, Tablero[j[0][0]][j[0][1]], n, T))
            V -= M
        rectificar()
        #if V > Valor['R']/2: V = Valor['R']
        #elif V < -Valor['R']/2: V = -Valor['R']
    return V

def elegirJugada(n, T):
    global Tablero
    LJ = Jugadas(T)
    Jugada = 0
    if len(LJ) > 0: 
        j = LJ[0]
        M = valorarJugada(j, Tablero[j[0][0]][j[0][1]], n, T)
        LMJ = LJ[0:1] # LMJ = lista de las mejores jugadas
        for j in LJ[1:]: 
            m = valorarJugada(j, Tablero[j[0][0]][j[0][1]], n, T)
            if m > M: M, LMJ = m, [j]
            elif m == M: LMJ.append(j)
        if M < -Valor['R']/2: Jugada = 0
        else: Jugada = random.choice(LMJ)
    return Jugada

Jugador = {'B' : "Computador", 'N' : "Computador"}    
    
def main():
    global Tablero, Turno, contador, pausas, ListaTableros, abc
    global InstruccionesSalir, InstruccionesNueva, InstruccionesRectificar, Valor
    PausarComputer = False 
    nueva_partida()
    print ("""  *** WELCOME TO EL AJEDREZ DE SALAS ***
    
    Instrucciones:
        "NUEVA" -> NUEVA PARTIDA
        "ABRIR" -> ABRIR PARTIDA
        "GUARDAR" -> GUARDAR PARTIDA
        "ATRÁS" -> RECTIFICAR JUGADA
        Jugadas, como: "c8xe6" o "c8e6"
        "SALIR" -> "SALIR DEL JUEGO"
        "N 4" -> "NIVEL 4" """)
    salir = False
    while not salir:  
        ver_tablero(marco = True)
        if Jugador[Turno] == "Humano": print "\n - SALIR - ", " - NUEVA - ", " - RECTIFICAR - ", " - d2d4 - ", "\n"
        if Turno == 'B': 
            print "Jugada:", contador/2, "Turno: 'B' (BLANCAS)", "Valor =", (ValorTotalJugador['B'] - Valor['R'])/20.0
        else: print "Jugada:", contador/2, "Turno: 'N' (NEGRAS)", "Valor =", (ValorTotalJugador['N'] - Valor['R'])/20.0
        if Jugador[Turno] == "Computador":
            jugada = elegirJugada(Nivel, Turno)
            print "El computador quiere jugar", escribir(jugada)
            if PausarComputer and raw_input("Continuar? S/N ").upper() == "N": salir = True
            else:
                if jugada == 0:
                    print "Tablas!!", "El jugador", Jugador[Turno], "se ha quedado encerrado"
                    salir = True
                else:
                    mover(jugada)
                    Turno = contrario(Turno)
        else:
            instruc = raw_input("ESCRIBA COMANDO: ").lower()       
            if any (instruc.find(palabra) >= 0 for palabra in InstruccionesSalir): salir = True
            elif any (instruc.find(palabra) >= 0 for palabra in InstruccionesNueva): nueva_partida()        
            elif any (instruc.find(palabra) >= 0 for palabra in InstruccionesRectificar): 
                rectificar()
                Turno = contrario(Turno)
            elif len(instruc) == 4: 
                print(instruc)
                instruc = list(traducir(c) for c in instruc if c in abc)
                jugada = ((instruc[1], instruc[0]), (instruc[3], instruc[2]))
                LJ = Jugadas(Turno)     
                if jugada in LJ: 
                    mover(jugada)
                    Turno = contrario(Turno)
                else: 
                    if len(LJ) == 0: 
                        print "Tablas!!", "El jugador", Jugador[Turno], Turno, "se ha quedado encerrado"
                        salir = True
                    else: print("Jugada ilegal!")
            else: print("Instrucción desconocida")
        ValorTotalJugador['B'], ValorTotalJugador['N'] = ValorTotalFichas('B'), ValorTotalFichas('N')
        for j in 'BN':
            if ValorTotalJugador[j] < Valor['R']/20:
                print "El jugador", Jugador[j], "(", j, ")", "ha perdido"
                salir = True
        contador += 1
        if pausas: 
            if contador%10 == 0: raw_input("Pulse intro para continuar...")
        if empaquetar(Tablero) in ListaTableros:
            print "Tablas!! Jugada repetida"
            salir = True
        else:
            ListaTableros.append(empaquetar(Tablero))
    print("Hasta la vista, baby!")
    
main()






