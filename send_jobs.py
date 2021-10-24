#!/usr/bin/env python3

import sys
import os
from subprocess import call
from shutil import copy

B = 1.0                           # Campo magnético
L = 100                           # Tamaño de la red (lado)
steps = 30_000_000                # Pasos de MC para producción (~L*L * 3k)
steps_term = int(0.1*steps)       # Pasos de MC para termalización (~0.1*steps)
# La secuencia de temperatura se define con una T inicial, seguida de pares (step, end)
# que definen rampas del estilo: [start, start+step, start+2*step+..., end]
# Luego la secuencia se invierte y las simulaciones se corren de T max a T min.
temp_sequence = (
    0.1,                #   start
    (0.1,1.6),          #   (step, end)
    (0.02, 2.1),        #   (step, end)
    (0.01, 2.4),        #   (step, end)
    (0.02, 3.0),        #   (step, end)
    (0.1, 4.1),         #   (step, end)
)
data_files = ['input.dat', 'output.dat', 'averages.dat', 'matriz.dat']
SKIP_EXISTING = True

def make_interval(start, *ramps):
    interval = []
    for step, end in ramps:
        n_steps = round( (end-start)/step )
        interval += [start + step*i for i in range(n_steps)]
        start = end
    return interval

temperatures = make_interval(*temp_sequence)
temperatures = temperatures[::-1]
# temperatures = [1.0]

def run_job(L, steps, temp, B):
    header = 'L\tpasos\tTemp\tB\n'
    data = f'{L}\t{steps}\t{temp:.3}\t{B:.3}\n'
    with open('input.dat','w') as infile:
        infile.write(header)
        infile.write(data)
    call('./ising')


def main(args):
    
    if len(args) != 2:
        print('Modo de uso: ./send_jobs.py N_JOBS')
        return 1
    else:
        try:
            njobs = int(args[1])
        except ValueError:
            print('El argumento debe ser un numero entero')
            return 1
        
        if os.path.exists('matriz.dat'):
                print('Quitando matriz.dat para trabajo inicial.')
                os.remove('matriz.dat')

        for temp in temperatures:
            tempdir = f'data/{L}_size/{B:.3}_B/{temp:.3}_temp'
            if os.path.exists(tempdir) and SKIP_EXISTING:
                print(f'El directorio {tempdir} ya existe, continuando con el siguiente.')
                continue
            print('*'*30)
            print(f'Corrida a T={temp:.3}\n')
            
            # corrida de termalizacion
            run_job(L, steps_term, temp, B)
                
            for job in range(1,njobs+1):
                dirname = f'{tempdir}/{job:02}_JOB'
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                
                print(f'Inciando trabajo {job}, a temperatura {temp:.3}')
                # corrida de produccion
                run_job(L, steps, temp, B)
                
                for file in data_files:
                    copy(file, dirname)

        print(f'Todos los trabajos finalizados')

        return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
