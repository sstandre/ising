#!/usr/bin/env python3

import sys
import os

def traverse_folders(data, names, level=0):
    if level >= len(names):
        write_averages(data)
        return
    else:
        name = names[level]
    for dirname in os.listdir():
        if os.path.isdir(dirname) and dirname.endswith(f'_{name}'):
            data_new = data + [dirname.split('_')[0]]
            
            os.chdir(dirname)
            traverse_folders(data_new, names, level+1)
            os.chdir('..')


def write_averages(data):
    with open('averages.dat', 'r') as file:
        next(file) # skip headers
        line = next(file)
    
    data = '\t'.join(data)+line
    datafile.write(data)


HEADER = '\t'.join((
    'size',
    'B',
    'temperature',
    'job', 
    'energy', 
    'energy^2', 
    'magnetization',
    'magnetization^2',
    'aceptados'
    ))+'\n'

OUTFILE = 'alldata.dat'
NAMES = ['size', 'B', 'temp', 'JOB']

with open(OUTFILE, 'w') as datafile:
    datafile.write(HEADER)
    data = []
    traverse_folders(data, NAMES)
