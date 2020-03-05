import random
import math
import simpy

Semilla = 30
ram = 100
T_min = 1
T_max = 100
T_process = 10
Totalordenes = 25

te = 0.0
dt = 0.0
fin = 0.0

RAM = 100 
memoria = 0
def new(proceso):
    global dt
    global ram
    global memoria 
    R = random.random()
    tiempo = T_max - T_min
    tiempoproceso = T_min + (tiempo*R)
    yield env.timeout(tiempoproceso)
    print("Proceso %s estara listo en %.2f minutos" % (proceso, tiempoproceso))
    dt = dt + tiempoproceso
    memoria = random.random()
    ram = ram - memoria
    return ram
    
def ready(memory):
    global RAM
    global memoria 
    memoria = random.random()
    if (RAM <= memoria):
        RAM = RAM - memoria
        return RAM
        
    
    
def running(env, name, turno):
    global te
    global fin
    inicio = env.now
    print("inicio el proceso %s en %.2f" % (name, inicio))
    with turno.request() as request:
        yield request
        pasa = env.now
        espera = pasa - inicio
        te = te + espera
        print("inicia proceso %s en minuto %.2f con una espera realizada de %.2f" % (name, pasa, espera))
        yield env.process(new(name))
        deja = env.now
        print ("termina proceso %s en minuto %.2f" % (name, deja))
        fin =  deja
        
def main(env, turno):
    global memoria
    global ram 
    empieza = 0
    i = 0
    for i in range (Totalordenes):
        Rando = random.random()
        empieza = -T_process * math.log(Rando)
        yield env.timeout(empieza)
        i += 1
        env.process(running(env, 'Proceso %d'% i, turno))
        ram = ram + memoria 


random.seed(Semilla)   
env = simpy.Environment()
turno = simpy.Resource(env, ram)
env.process(main(env, turno))
env.run()

