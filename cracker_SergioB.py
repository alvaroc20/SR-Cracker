#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-
import string
import math
from time import time
from multiprocessing import Process, cpu_count
import gnupg
import subprocess

subprocess.run(args=['pip3', "install", "progress"])
subprocess.run(args=['pip3', "install", "gnupg"])
from progress.bar import IncrementalBar

def to_base(n, alphabet, width):
    """
    Change int to any base

    >>> to_base(255, string.hexdigits[:16])
    'ff'
    >>> to_base(12345678, string.hexdigits[:16])
    'bc614e'
    """
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

def gpg_Process(first, last, bar):
    #Genera la secuencia de de combinaciones para la CPU x
    for key in range(first,last+1):
        password ='{}'.format(to_base(key, alphabet, key_len)) #print(password)
        status = gpg.decrypt_file(open('trabajos-teoría.pdf.gpg-no-mdc', 'rb'), passphrase=password, output='trabajos-teoría.pdf')

        if status.ok:
            print("\033[4;32m\n########################################\n")
            print("La password es: ",password)
            print("\n########################################\n\033")
        bar.next()
        
#Tipo de valores a combinar
alphabet = 'buz'#string.ascii_lowercase # Si quieres que la encuentre rapido'buz'
#Tamaño de la cadena a formar
key_len = 4
key_space = len(alphabet) ** key_len
n_partition = cpu_count()
partition_size = math.ceil(key_space / n_partition)

print("Partition size = key space / partitions = {:,} / {} = {:,}".format(key_space, n_partition, partition_size))

bar = IncrementalBar('', max = partition_size)
gpg = gnupg.GPG(options= '--ignore-mdc-error',)
jobs =[]


#Inicialización crackeo
start_time = time()
for first, last in gen_key_partitions(key_space=key_space, partition_size=partition_size):  
    #Rango i de valores a combinar
    print("- {:>20,} {:>20,} -{:>20,}".format(
        last-first, first, last), end='')
    print(" {:>10} -{:>10}".format(to_base(first, alphabet, key_len), to_base(last, alphabet, key_len)))

    #gpg_Process(first, last, bar)
    
    p = Process(target=gpg_Process, args=(first, last, bar))
    jobs.append(p)

#Inicialización procesos
for j in jobs:
    j.start()

#Espera finalización procesos
for j in jobs:
    p.join()

elapsed_time = time() - start_time
print("Elapsed time: %0.10f seconds." % elapsed_time)