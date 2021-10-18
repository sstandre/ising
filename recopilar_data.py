#!/usr/bin/env python3

import sys
import os

def transverse_folders(data, names, level=0):
    if level >= len(names):
        write_averages(data)
        return
    else:
        name = names[level]
    for dirname in os.listdir():
        if os.path.isdir(dirname) and dirname.endswith(f'_{name}'):
            os.chdir(dirname)

            data_out = data + [dirname.split('_')[0]]
            transverse_folders(data_out, names, level+1)
            os.chdir('..')


def write_averages(data):
    with open('averages.dat', 'r') as file:
        next(file) # skip headers
        line = next(file)
    
    data = '\t'.join(data)+line
    datafile.write(data)


HEADER = '\t'.join((
    'size', 
    'job', 
    'temperature', 
    'energy', 
    'energy^2', 
    'magnetization',
    'magnetization^2',
    ))+'\n'

OUTFILE = 'alldata.dat'
NAMES = ['size', 'JOB', 'temp']

with open(OUTFILE, 'w') as datafile:
    datafile.write(HEADER)
    data = []
    transverse_folders(data, NAMES)