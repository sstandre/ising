# Ising
Modelo de Ising implementado en Fortran 90 como parte de la materia Introducción a la Simulación computacional.
www.tandar.cnea.gov.ar/~pastorin/cursos/intro_sims/

#### Autores 
  - Augusto Román [augustojre](https://github.com/augustojre)
  - Simón Saint-André [sstandre](https://github.com/sstandre)

## Cómo correr una simulación

- Editar el archivo `input.dat`. La primera línea tiene los nombres de las variables de ingreso y es ignorada por el programa. La segunda tiene los valores de las variables.
- Compilar el programa de Fortran con `make`
- Correr el ejecutable resultante: `./ising`
- Si existe un archivo `matriz.dat`, el programa lo toma como arreglo inicial para la simulación. Debe ser un arreglo de LxL de 1 y -1. Al finalizar la simulación, el programa sobreescribe `matriz.dat` con la última configuración simulada. Precaución: al cambiar de tamaño de red, los archivos `matriz.dat` no funcionarán para la nueva simulación.

### Archivos de salida

- `output.dat`: 2 columnas y (steps / L * L) filas. Contiene valores de Energía y Magnetización sampleados de la secuencia de pasos de Montecarlo.
- `averages.dat`: 2 filas: Una con títulos y otra con 5 datos. Lo primeros 4 son promedios sobre todos los pasos de MC: Energía media, Magnetización media, Energía^2 media, y Magnetización^2 media. El último valor corresponde a la fracción de pasos de MC aceptados. Si bien todas las cantidades se calculan dentro del programa `ising`, pueden aproximarse a partir de `output.dat`.
- `matriz.dat`: Última configuración obtenida. Sobreescribe a la configuración de entrada.
- `seed.dat`: Archivo utilizado por `ziggurat` para obtener números aleatorios. Se usa tanto como entrada como salida.

## Cómo hacer un barrido de temperaturas

- Editar en `send_jobs.py` el tamaño de red, el numero de pasos de MC y el valor del campo magnético (B).
- Ejecutar `python3 send_jobs.py NJOBS` donde NJOBS es el número de corridas que hace en cada temperatura.

Las distintas simulaciones se organizan en el directorio `data/`. Por ejemplo, de la siguiente forma:
```
data/
  |______20_size/
            |____0.0_B/
            |       |____0.1_temp/
            |       |       |____01_JOB/
            |       |       |       |____output.dat
            |       |       |       |____averages.dat
            |       |       |       |____matriz.dat
            |       |       |____02_JOB/
            |       |       |       |____output.dat
            |       |       |       |____averages.dat
            |       |       |       |____matriz.dat   
            |       |       |      ...
            |       |       |____10_JOB/
            |       |              ...
            |       |____0.2_temp/
            |       |      |____01_JOB/
            |       |      ...
            |       |____4.0_temp/
            |              ...
            |____0.01_B/
            |       |____0.1_temp/
            |              ...
            |
        100_size/
            |____0.0_B/
         ...
```

Toda la información contenida en los distintos `averages.dat` se puede recopilar en un solo archivo mediante:
`python3 recopilar_data.py`
Esto crea (o sobreescribe) el archivo `alldata.dat`, con el cual se pueden analizar los resultados obtenidos.

## Análisis de datos en Jupyter

El notebook `analisis.ipynb` contiene los cálculos y las figuras realizadas con la información de `alldata.dat`. Al ejecutarlo se llama a `recopilar_data.py` para asegurarse de tener los datos actualizados.

Para correr este notebook tenemos que usar Jupyter, que no está por defecto en Ubunutu. Puede ser instalado en un entorno virtual:

 - `sudo apt install python3-venv`
 - `python3 -m venv .venv`
 Con esto tenemos creado el entorno virtual, para usarlo lo activamos con:
 - `source .venv/bin/activate`
 Ahora podemos instalar Jupyter y otros paquetes mediante `pip`:
 - `pip3 install -r requirements.txt`
