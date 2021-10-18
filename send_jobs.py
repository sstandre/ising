#!/usr/bin/env python3.9

import sys
import os
from subprocess import call
from shutil import copy

L = 10
steps = 1_000_000
steps_term = int(0.1*steps)
temp_sequence = (
    0.1,                #   start
    (0.1,1.6),          #   (step, end)
    (0.02, 2.1),        #   (step, end)
    (0.01, 2.4),        #   (step, end)
    (0.02, 3.0),        #   (step, end)
    (0.1, 4.1),         #   (step, end)
)
data_files = ['input.dat', 'output.dat', 'averages.dat', 'matriz.dat']


def make_interval(start, *ramps):
    interval = []
    for step, end in ramps:
        n_steps = int( (end-start)/step )
        interval += [start + step*i for i in range(n_steps)]
        start = end
    return interval

temperatures = make_interval(*temp_sequence)
temperatures = temperatures[::-1]
# temperatures = [1.0]

def run_job(L, steps, temp):
    header = 'L\tpasos\tTemp\n'
    data = f'{L}\t{steps}\t{temp:.3}\n'
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

        for job in range(1,njobs+1):
            jobdir = f'{L}_size/{job:02}_JOB'
            if os.path.exists(jobdir):
                print(f'El trabajo {job} ya existe, continuando con el siguiente.')
                continue
            print('*'*30)
            print(f'Inciando trabajo {job}')
            if os.path.exists('matriz.dat'):
                print('Quitando matriz.dat para trabajo inicial.')
                os.remove('matriz.dat')

            for temp in temperatures:
                dirname = f'{jobdir}/{temp:.3}_temp'
                if not os.path.exists(dirname):
                    os.makedirs(dirname)

                print(f'Corrida a T={temp:.3}\n')
                # corrida de termalizacion
                run_job(L, steps_term, temp)
                # corrida final
                run_job(L, steps, temp)
                
                for file in data_files:
                    copy(file, dirname)

        print(f'Todos los trabajos finalizados')

        return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
