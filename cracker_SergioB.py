#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import string
import math
import time
import multiprocessing
import subprocess
from os import remove
from os import path
from time import time



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


def gen_key_partitions(alphabet, key_len, n_partitions):
    key_space = len(alphabet) ** key_len

    partition_size = math.ceil(key_space / n_partitions)
    print("Partition size = key space / #partitions = {:,} / {} = {:,}".format(
        key_space, n_partitions, partition_size))

    for first in range(0, key_space, partition_size):
        last = min(first + partition_size, key_space) -1
        yield first, last

def keyDiccionary(first, last, alphabet):
    #Genera la secuencia de de combinaciones
    for key in range(first, last+1):
        password= "{}".format(to_base(key, alphabet, key_len))
        #print("FIRTS {} , LAST {}: PASSWORD {}\n".format(first,last, password))
        pass_a = subprocess.run(args=['gpg', '--ignore-mdc-error', '-d', '--batch', '--output', '/home/warrios/Escritorio/universidad/seguridad_Redes/cracker/trabajos-teoría.pdf','--passphrase', password,
                                      '/home/warrios/Escritorio/universidad/seguridad_Redes/cracker/trabajos-teoría.pdf.gpg-no-mdc'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        not_Password = '{!r}'.format('gpg: datos cifrados CAST5\ngpg: cifrado con 1 frase contraseña\ngpg: descifrado fallido: Clave incorrecta de sesión\n')
        intento_pass = '{!r}'.format(pass_a.stderr.decode('utf-8'))
        if len(not_Password) != len(intento_pass):
            print('Eureka! la password es: ',password)

        #print(combinacion)


alphabet = string.ascii_lowercase # Si quieres que la encuentre rapido'buz'
print(alphabet)
key_len = 4


if path.exists("diccionario.txt"):
    remove('diccionario.txt')
start_time = time()

jobs = []
for first, last, in gen_key_partitions(alphabet, key_len=key_len, n_partitions=multiprocessing.cpu_count()):
    print("- {:>20,} {:>20,} -{:>20,}".format(
        last-first, first, last), end='')
    print(" {:>10} -{:>10}".format(to_base(first, alphabet, key_len), to_base(last, alphabet, key_len)))
    
    p = multiprocessing.Process(target=keyDiccionary, args=(first,last, alphabet))
    jobs.append(p)
    p.start()



for j in jobs:
    j.join()

elapsed_time = time() - start_time
print("Elapsed time: %0.10f seconds." % elapsed_time)