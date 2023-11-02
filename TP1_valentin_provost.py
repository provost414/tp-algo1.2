import random
import os
from colorama import Fore, init
init(autoreset=True)

PALITO_ROJO = Fore.RED + "|"
PALITO_BLANCO  = Fore.WHITE + "|"
PALITO_FREEZE = Fore.BLUE + "|"

CONTINUAR = '''
---------------------------------------------------------\n
             PRESIONE ENTER PARA CONTINUAR               \n
---------------------------------------------------------\n
            '''

BIENVENIDO = '''
            *******************************************\n
            ¡ BIENVENIDO A ESTOS PALITOS SON UN CHINO !\n
            *******************************************\n
            '''

TIRAR_DADO = '''
----+----+----+----+----+----+----+----+----+----+----+--\n
           PRESIONE ENTER PARA TIRAR EL DADO             \n
----+----+----+----+----+----+----+----+----+----+----+--\n

            '''



def evento6():
    
    print("¡ El juego continua !")


def evento5(nro_jugadores: int):
     guardar_palitos_por_filas, cant_filas = crear_piramide_inicial(nro_jugadores)

     return guardar_palitos_por_filas, cant_filas


def evento4(cant_filas: int, guardar_palitos_por_filas: list[list]):

    mostrar_piramide(cant_filas, guardar_palitos_por_filas)
    print("\n")
    fila_a_eliminar =int(input("Elige la fila que deseas eliminar: "))
    guardar_palitos_por_filas.pop(fila_a_eliminar - 1)
    cant_filas = cant_filas - 1
           
    
    return guardar_palitos_por_filas, cant_filas


     
def eventos(nro_jugadores: int, guardar_palitos_por_filas: list[list[str]], cant_filas: int):


    print("\n""¡ATENCION EVENTO!""\n")
    print(TIRAR_DADO)
    input(" ")
    limpiar_terminal()
    dado = random.randint(1,6)
    print(f"HA TOCADO {dado}")
    print("\n")

    seguir = True
    while seguir:
        if dado == 1:
            print("PIERDE UN TURNO")
            
            seguir = False
        elif dado == 2:
            print("AGREGAR PALITOS !")
            
            seguir = False

        elif dado == 3:
            print(" ! PALITOS CONGELADOS !\n")
          
            seguir = False

        elif dado == 4:
            print("\n¡ ELIMINAR FILA !\n")
            guardar_palitos_por_filas, cant_filas = evento4(cant_filas, guardar_palitos_por_filas)
            seguir = False

        elif dado == 5:
            print("NUEVA PIRAMIDE\n")
            guardar_palitos_por_filas, cant_filas = evento5(nro_jugadores)
            mostrar_piramide(cant_filas, guardar_palitos_por_filas)
            
            seguir = False

        elif dado == 6:
            evento6()
    
            seguir = False

    return guardar_palitos_por_filas, cant_filas


def contador_palitos_sacados(nro_jugadores: int)-> dict and list[int]:
         
    jugadores_lista, nombre_jugador = jugadores_del_juego(nro_jugadores)
    contador_palitos_jugadores: list[int] = list()
    contador_palitos_bots: dict = {}

    for jugadores_del_juego in jugadores_lista:
        
        if jugadores_del_juego != nombre_jugador:
            contador_palitos_bots[jugadores_del_juego] = 0
            
    return contador_palitos_bots, contador_palitos_jugadores


def partida(nro_jugadores: int, contador_palitos_bots: dict, contador_palitos_jugadores: list[int]):

    jugadores_lista, nombre_jugador = jugadores_del_juego(nro_jugadores)
    guardar_palitos_por_filas, cant_filas = crear_piramide_inicial(nro_jugadores)

    limpiar_terminal()

    print(f"\n¡ {nombre_jugador} que empieze el juego!\n")
    
    print("\n")

    seguir = True
    perder_turno = False
    turno_actual: int = 0
    cantidad: int = 0
    contador_palitos_freeze: int = 0

    while seguir:

        jugando = jugadores_lista[turno_actual]

        if jugando == nombre_jugador:

            if not perder_turno:
                mostrar_piramide(cant_filas, guardar_palitos_por_filas)
                print("\n")
                lista_palitos = sacar_palitos_jugador(guardar_palitos_por_filas, contador_palitos_jugadores, nro_jugadores, cant_filas)
                guardar_palitos_por_filas = reacomodar_piramide(cant_filas, lista_palitos)
                print("\n")
                limpiar_terminal()
                mostrar_piramide(cant_filas, guardar_palitos_por_filas)
                print(CONTINUAR)
                input(" ")
                limpiar_terminal()
            else: 
                print("pierdes tu turno")
          
        else:
            print(f"el {jugadores_lista[turno_actual]} hizo los siguientes movimientos: \n")
            lista_palitos = sacar_palitos_bot(guardar_palitos_por_filas,contador_palitos_bots, turno_actual, nro_jugadores, cant_filas)
            guardar_palitos_por_filas = reacomodar_piramide(cant_filas, lista_palitos)
            print("\n")
            mostrar_piramide(cant_filas, guardar_palitos_por_filas)
            print(CONTINUAR)
            input(" ")
            limpiar_terminal()
        
        if len(guardar_palitos_por_filas) == 1 and len(guardar_palitos_por_filas[0]) == 1:
                    seguir = False

        if turno_actual == len(jugadores_lista) - 1:

            turno_actual = 0
        else:
            turno_actual += 1


    print(f"Jugador que perdio -> {jugadores_lista[turno_actual]}")
    print("\n")
    
    for elemento in contador_palitos_jugadores:
        cantidad += elemento 
        
    print(f"has sacado {cantidad} palitos en total")
    print("\n")

    for clave, valor in contador_palitos_bots.items():
        print(f"el bot {clave} saco {valor} palitos en total\n")

    print("¡ GRACIAS POR JUGAR !")


def sacar_palitos_bot(guardar_palitos_por_filas: list[list[str]], contador_palitos_bots: dict, jugador_actual: str, nro_jugadores: int, cant_filas: int) -> list:

    contador_palitos_rojos_bot: int = 0

    if len(guardar_palitos_por_filas) == 1:
        palitos_a_retirar = 1
    else:
        palitos_a_retirar = random.randint(1, 3)

    while palitos_a_retirar > 0:


        saca_fila_bot: int = random.randint(0, len(guardar_palitos_por_filas) - 1)
        

        if guardar_palitos_por_filas[saca_fila_bot]:
            saca_columna_bot: int = random.randint(0, len(guardar_palitos_por_filas[saca_fila_bot]) - 1)
            
            if guardar_palitos_por_filas[saca_fila_bot][saca_columna_bot] == PALITO_ROJO:

                palitos_a_retirar = palitos_a_retirar - 1
                guardar_palitos_por_filas[saca_fila_bot][saca_columna_bot] = 'r'
                contador_palitos_rojos_bot += 1
                print(f"fila: {saca_fila_bot+1} , Columna: {saca_columna_bot+1}")

                if jugador_actual in contador_palitos_bots:
                    contador_palitos_bots[jugador_actual] += 1
                else:
                    contador_palitos_bots[jugador_actual] = 1

            elif guardar_palitos_por_filas[saca_fila_bot][saca_columna_bot] == PALITO_BLANCO:

                guardar_palitos_por_filas[saca_fila_bot][saca_columna_bot] = 'x'
                palitos_a_retirar = palitos_a_retirar - 1
                print(f"fila: {saca_fila_bot+1} , Columna: {saca_columna_bot+1}")


                if jugador_actual in contador_palitos_bots:
                    contador_palitos_bots[jugador_actual] += 1
                else:
                    contador_palitos_bots[jugador_actual] = 1

    nuevos_palitos = list()

    for listas in guardar_palitos_por_filas:
        while 'x' in listas:
            listas.remove('x')
        while 'r' in listas:
            listas.remove('r')
     
    if contador_palitos_rojos_bot >= 1:
         eventos(nro_jugadores, guardar_palitos_por_filas, cant_filas)

    for fila in guardar_palitos_por_filas:
            for elemento in fila:
                nuevos_palitos.append(elemento)
                
    return nuevos_palitos


   
def sacar_palitos_jugador(guardar_palitos_por_filas: list[list[str]], contador_palitos_jugadores: list[int], nro_jugadores: int, cant_filas: int) -> list:
   
    contador_palitos_rojos: int = 0
    contador_quitar: int = 0
    contador_palitos: int = 0
    maximo_a_quitar: int = 3
    seguir_quitando = True

    while contador_quitar < maximo_a_quitar:

        while seguir_quitando and contador_quitar < maximo_a_quitar:

            saca_fila: int = int(input("Ingrese la fila del palito que quiere retirar: "))
            saca_fila -= 1

            if 0 <= saca_fila < len(guardar_palitos_por_filas):

                saca_columna: int = int(input("Ingrese la columna del palito que quiere retirar: "))
                saca_columna -=1

                if 0 <= saca_columna < len(guardar_palitos_por_filas[saca_fila]):

                    if guardar_palitos_por_filas[saca_fila][saca_columna] == PALITO_ROJO:
                       
                        guardar_palitos_por_filas[saca_fila][saca_columna] = 'r'
                        contador_palitos_rojos += 1

                    else:
                        guardar_palitos_por_filas[saca_fila][saca_columna] = 'x'


                    contador_quitar += 1
                    contador_palitos +=1

            if contador_quitar < maximo_a_quitar:
                
                continuar = input("Quieres seguir quitando palitos? (s/n): ").lower()

                if continuar == "n":
                    seguir_quitando = False
                    contador_quitar = maximo_a_quitar

        
        contador_palitos_jugadores.append(contador_palitos)
        
        nuevos_palitos = []

        for listas in guardar_palitos_por_filas:
            while 'x' in listas:
                listas.remove('x')
            while 'r' in listas:
                listas.remove('r')
        
        if contador_palitos_rojos >= 1:
              eventos(nro_jugadores, guardar_palitos_por_filas, cant_filas)
              
        for fila in guardar_palitos_por_filas:
            for elemento in fila:
                nuevos_palitos.append(elemento)

    if contador_palitos_rojos >= 1:
        contador_palitos_rojos = 0

    return nuevos_palitos

      
def jugadores_del_juego(nro_jugadores: int) -> list[str] and str:

    jugadores_lista: list[str] = list()
    print("\n")
    nombre_jugador: str = input("Ingrese el nombre con el que va a jugar: ")
    jugadores_lista.append(nombre_jugador)

    for i in range(nro_jugadores - 1):
        jugadores_lista.append("bot " + str(i + 1))

    return jugadores_lista, nombre_jugador


def reacomodar_piramide(filas, palitos) -> list[list[str]]:

    guardar_palitos_por_filas_bis = []

    for i in range(0, filas+1):
        fila = palitos[:i]
        guardar_palitos_por_filas_bis.append(fila)
        palitos = palitos[i:]
    
    guardar_palitos_por_filas_bis = [fila for fila in guardar_palitos_por_filas_bis if fila != []]

    if len(guardar_palitos_por_filas_bis) > 1:

        ultima_fila = len(guardar_palitos_por_filas_bis)-1

        if len(guardar_palitos_por_filas_bis[ultima_fila]) <= len(guardar_palitos_por_filas_bis[ultima_fila-1]):
            i = 0
            
            while len(guardar_palitos_por_filas_bis[ultima_fila]) > 0:
                guardar_palitos_por_filas_bis[i].append(guardar_palitos_por_filas_bis[ultima_fila].pop())
                i = i + 1
            guardar_palitos_por_filas_bis.pop()

    return guardar_palitos_por_filas_bis


def crear_piramide_inicial(nro_jugadores: int) -> list[list[str]] and int:

    jugador_random: int = random.randint (nro_jugadores, 10)
    cant_filas: int = jugador_random + 2
    cant_palitos_totales: int = ((jugador_random + 2) * (jugador_random + 3)) // 2
    cant_palitos_rojos: int = random.randint(round(cant_palitos_totales * 0.2), round(cant_palitos_totales * 0.3))
    guardar_palitos_totales: list[str] = list()

    for i in range(cant_palitos_rojos):
        guardar_palitos_totales.append(PALITO_ROJO)

    for i in range(cant_palitos_totales - cant_palitos_rojos):
        guardar_palitos_totales.append(PALITO_BLANCO)

    random.shuffle(guardar_palitos_totales)

    guardar_palitos_por_filas: list[list[str]] = list()

    for i in range(1, cant_filas + 1):
        fila: list[str] = guardar_palitos_totales[:i]
        guardar_palitos_por_filas.append(fila)
        guardar_palitos_totales: list[str] = guardar_palitos_totales[i:]

    return guardar_palitos_por_filas, cant_filas


def mostrar_piramide(cant_filas: int, guardar_piramide: list[list[str]]):

    for fila in guardar_piramide:
        espacios: int = (cant_filas - len(fila))
        fila_piramide: str = '  ' * espacios + '   '.join(fila) 
        print(fila_piramide)
        print()


def limpiar_terminal():

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def main():

    contador_palitos_bots: dict = {}
    contador_palitos_jugadores: list = []

    print("\n")
    print(BIENVENIDO)

    nro_jugadores = int(input("Por favor ingrese el número de jugadores_del_juego que van a jugar: "))

    limpiar_terminal()
    partida(nro_jugadores, contador_palitos_bots, contador_palitos_jugadores)

main()