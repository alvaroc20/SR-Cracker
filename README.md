# SR-Cracker

Cracker realizado para obtener los temas teoricos de la asignatura de Seguridad en Redes, parte de la intensificación de Ingeniería de Computadores. Realizamos el cracker para la versión que no tiene integridad, por Álvaro Cerdá y Sergio Barrios.  

## Requisitos Previos  
Es necesario tener tanto python3 como pip3. También es necesario algunas librerías que instalaremos al ejecutar el programa.  

## Compilacion y uso   
Para compilar usar:  
`python3 gpg-cracker --len 4 --charset digits cifrado.gpg `  

**--len:** Indicar el número de posiciones que sea desea buscar.  
**--charset:** Indicar si queremos buscar entre digits/upper/lower.  
**name:** Nombre del archivo que queremos descifrar.  


## Versiones  
### Version 1.0  
Genera diccionarios con el numero de posiciones que queremos.

### Version 1.1  
Prueba todas las contraseñas del diccionario.  

### Version 1.2  
Encuentra la contraseña pero todavia no es optimo.  

### Version 1.3  
Finalizado el correcto funcionamiento a excepción de la gestión de la finalización de los procesos al encontrar un resultado válido.  