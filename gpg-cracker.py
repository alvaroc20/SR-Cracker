#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

#################################################################################
''' Esta práctica está realizada por Álvaro Cerdá Pulla y Sergio Barrios Martínez 
    
    Asignatura: Seguridad en Redes
    
    Fecha: 26 de Noviembre de 2020

    GitHub: https://github.com/alvaroc20/SR-Cracker

    Compilación: python3 gpg-cracker.py --len 4 --charset lower cifrado.gpg

    options charset:
        - lower [a-z]
        - upper [A-Z]
        - digits [0-9]
    
    Intensificación: Ingeniería de Computadores                                 '''
#################################################################################

import subprocess
subprocess.run(args=['pip3', 'install', 'python-gnupg'])
subprocess.run(args=['pip3', 'install', 'progress'])
subprocess.run(args=['pip3', 'install', 'multiprocess'])

import string
import math
from time import time
from multiprocessing import Process, cpu_count, Value
import gnupg
import argparse
from progress.bar import IncrementalBar

def to_base(n, alphabet, width):

    retval = ''
    base = len(alphabet)

    while n >= base:
        index = n % base
        n = n // base
        retval += alphabet[index]

    retval += alphabet[n]

    return "{:{}>{}}".format(retval[::-1], alphabet[0], width)


def gen_key_partitions(key_space, partition_size):

    for first in range(0, key_space, partition_size):
        last = min(first + partition_size, key_space) -1
        yield first, last

def gpg_Process(first, last, bar, f, fin_Value):

    for key in range(first,last+1):
        if(fin_Value.value == 1):
            #Si ya se ha encontrado la contraseña
            break

        password ='{}'.format(to_base(key, alphabet, key_len)) #print(password)
        status = gpg.decrypt_file(open(f, 'rb'), passphrase=password, output='trabajos-teoría.pdf')

        #Si el desencriptado fue exitoso
        if status.ok:
            print("\033[1;32m\n########################################\n")
            print("La password es: ",password)
            print("\n########################################\n\033[0;37m")
            #Notificar a los demás procesos de que la contraseña se ha encontrado
            fin_Value.value = 1
            break
        bar.next()

# Paso de argumentos
parser = argparse.ArgumentParser()
parser.add_argument('--len', required=True, type=int)
parser.add_argument('--charset', required=True)
parser.add_argument('name')
args = parser.parse_args()

## Posibles tipos de valores para combinar
if(args.charset == "digits"):
    alphabet = string.digits
elif (args.charset == "lower"):
    alphabet = string.ascii_lowercase
elif (args.charset == "upper"):
    alphabet = string.ascii_uppercase
else:
    print("Charset solo puede ser digits, lower o upper.")
    sys.exit(2)


key_len = args.len #Tamaño de la cadena a formar
f = args.name # GPG FILE

# División del trabajo segun el numero de CPU's disponible
key_space = len(alphabet) ** key_len
n_partition = cpu_count()
partition_size = math.ceil(key_space / n_partition)

print("Partition size = key space / #partitions = {:,} / {} = {:,}".format(key_space, n_partition, partition_size))

# Creación de barra de progreso
bar = IncrementalBar('', max = partition_size)

# Libreria GnuPG con la opción de ignorar la integridad del documetno
gpg = gnupg.GPG(options= '--ignore-mdc-error',)

fin_Value = Value('i', 0) # Variable compartida Si 0->No_password 1->Password_encontrada

#Inicialización crackeo
jobs =[]
start_time = time()
for first, last in gen_key_partitions(key_space=key_space, partition_size=partition_size):  
    
    print("- {:>20,} {:>20,} -{:>20,}".format(
        last-first, first, last), end='')
    print(" {:>10} -{:>10}".format(to_base(first, alphabet, key_len), to_base(last, alphabet, key_len)))
    #gpg_Process(first, last, bar)
    
    #Creación de un proceso para el método gpg_Process de un rango de combinaciones
    p = Process(target=gpg_Process, args=(first, last, bar, f, fin_Value))
    jobs.append(p)

#Inicialización procesos
for j in jobs:
    j.start()

#Espera finalización procesos
for j in jobs:
    p.join()

# Si ningun proceso a cambiado a 1 la variable compartida es que en el rango intentado no se ha encontrado la contraseña
if(fin_Value.value == 0):
    print("\033[1;31m"+"No se ha podido encontrar la contraseña. Prueba con otra combinación."+"\033[0;37m")
    

elapsed_time = time() - start_time
print("Elapsed time: %0.10f seconds." % elapsed_time)