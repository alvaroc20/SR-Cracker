#!/usr/bin/pyhon3

import itertools
import string
import os.path as path
import subprocess
import readline

### Genera un diccionario de posibles soluciones
def keyGenerator(n, alphabet):
       for p in itertools.product(alphabet, repeat=n):
           file.write("".join(p))
           file.write("\n")

### Probar cada una de las combinaciones mediante el comando de descifrado.
def keyTest(comb):
    for password in comb:
        password = password[:len(password)-1]
        command = "gpg", "--batch", "--passphrase", password ,"-d ejemplos/ejemplo3.gpg"
        print(command)
        pass_a = subprocess.run(args=['gpg', '--batch', '--passphrase', password, '-d', 'ejemplos/teoria.pdf.gpg'])
        if pass_a.returncode == 0:
            print("HAAAS ACERTADOOOOO MOSTROOOOOOO")

        #print(pass_a.stdout)

### PARAMETROS DE ENTRADA
alphabet = string.ascii_lowercase
n =int(input("What is the password size?\n"))
fileDir = input("Name of the file where the dictionary will be generated\n")

### Apertura y/o creacion de un archivo donde se guarda el resultado
if path.exists(fileDir):
    print(f"El archivo {fileDir} ya existe. Abriendo\n")
    file = open(fileDir, "a")
else:
    print(f"Has creado {fileDir}\n")
    file = open(fileDir, "x")

### Llamada al metodo que genera todas las posibles contraseñas
keyGenerator(n, alphabet)
print(f"Diccionario creado en el archivo {fileDir} con {n} posiciones de contraseña")

### Probamos todas las contraseñas que hemos generado
f = open(fileDir, "r")
comb = f.readlines()
#keyTest(comb)
f.close()