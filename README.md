# Ising
Modelo de Ising implementado en Fortran 90 como parte de la materia Introducción a la Simulación computacional 

## Cómo correr la simulación

- Editar el archivo `input.dat`. La primera línea tiene los nombres de las variables de ingreso y es ignorada por el programa. La segunda tiene los valores de las variables.
- Compilar el programa de Frontran con `make`.
- Correr el ejecutable resultante: `./ising`.
- Si existe un archivo `matriz.dat`, el programa lo toma como arreglo inicial para la simulación. Debe ser un arreglo de LxL de 1 y -1. Al finalizar la simulación, el programa sobreescribe `matriz.dat` con la última configuración simulada. Precaución: al cambiar de tamaño de red, los archivos `matriz.dat` no funcionarán para la nueva simulación.

### Archivos de salida

- `output.dat`: 2 columnas y (steps / L * L) filas. Contiene valores de Energía y Magnetización sampleados de la secuencia de pasos de Montecarlo.
- `averages.dat`: 2 filas: Una con títulos y otra con 4 datos promediados sobre las configuraciones sampleadas: Energía media, Magnetización media, Energía^2 media, y Magnetización^2 media. Si bien se calculan dentro del programa `ising`, pueden obtenerse a partir de `output.dat` (y deben coincidir).
- `matriz.dat`: Última configuración obtenida. Sobreescribe a la configuración de entrada.
- `seed.dat`: Archivo utilizado por `ziggurat` para obtener números aleatorios. Se usa tanto como entrada como salida.

## Cómo hacer un barrido de temperaturas

- Editar en `send_jobs.py` el tamaño de red y el numero de pasos de MC.
- Ejecutar `python3 send_jobs.py NJOBS` donde NJOBS es el número de veces que se hace el barrido.

Las distintas simulaciones se organizan en un árbol de archivos. Por ejemplo, de la siguiente forma:
```
20_size/
    |____01_JOB/
    |       |____0.1_temp/
    |       |       |____output.dat
    |       |       |____averages.dat
    |       |       |____matriz.dat
    |       |       |____output.dat
    |       |____0.2_temp/
    |       |       |____output.dat
    |       |       |____averages.dat
    |       |       |____matriz.dat
    |       |       |____output.dat
    |       |       ...
    |       |____4.0_temp/
    |               ...
    |____02_JOB/
    |       |____0.1_temp/
    |               ...
100_size/
    |____01_JOB/
            ...
```

Toda la información contenida en los distintos `averages.dat` se puede recopilar en un solo archivo mediante:
`python3 recopilar_data.py`
Esto crea (o sobreescribe) el archivo `alldata.dat`, con el cual se pueden analizar los resultados obtenidos.

## Análisis de datos en Jupyter

El notebook `analisis.ipynb` contiene los cálculos y las figuras realizadas con la información de `alldata.dat`. Al ejecutarlo se llama a `recopilar_data.py` para asegurarse de tener los datos actualizados.
Para correr este notebook tenemos que usar Jupyter, que no está por defecto en Ubunutu. Podemos instalarlo en un entorno virtual:
 -`sudo apt install python-venv`
 -`python -m venv .venv`
 Con esto tenemos creado el entorno virtual, para usarlo lo activamos con:
 -`source .venv/bin/activate`
 Ahora podemos instalar Jupyter y otros paquetes mediante `pip`
 - `pip install -r requirements.txt`

