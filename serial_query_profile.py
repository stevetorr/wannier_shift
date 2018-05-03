import numpy as np
import time as time
from multiprocessing import Pool

import matplotlib.pyplot as plt

""" 
The point of this file is to profile in a semi-automatic way the comparative
speed of querying all of the orbitals in the Wannier-coupling database in order to 
compare the querying process with and without spark. 

"""


def load_pair_orbital_couplings_serial(k,l,thoroughness=1):
    """
    For profiling purposes, try to perform a serial query of the relevant information.
    """

    debug=False
    timer=True

    # Loop through the current directory to look at the new proc wan files

    file_base = 'new_proc_wan_'
    indices = range(0,400,thoroughness)
    file_names = [file_base+str(i) for i in indices]

    data_pieces=[]

    for f in file_names:
        if timer: t0=time.time()
        if debug: print("Now reading in file",f)
        
        new_data=load_orbitals_python(f,k,l)
        for point in new_data:
            data_pieces.append(point)

        if timer: print("Read file %s which took %f seconds" %(f, time.time()-t0))

    if debug: print("returning array with dimension", np.array(data_pieces).shape)
    return(np.array(data_pieces))


def load_orbitals_python(f,k,l,debug=False):
    """
    Loads in the orbitals from f which match a given profile from orbitals k and l
    Using standard python tools.
    """

    with open(f,'r') as f_:
        thelines=f_.readlines()[1:]

        if debug:
            print('Heres the first line',thelines[1])
            print(int(thelines[1].split(',')[2]), thelines[1].split(',')[5] )

        hits = [line.strip().split(',') for line in thelines if ( (int(line.split(',')[2])==k and line.split(',')[5]==l) or (int(line.split(',')[2])==l and  int(line.split(',')[5])==k)) ]
        
        if debug:
            print("Found %d hits" % len(hits))

        return [[float(hit[n]) for n in [6,7,8,9]] for hit in hits]

def load_orbitals_pool(arg_tuple):
    """
    Simple helper function to make the python arguments work with each other
    """
    return load_orbitals_python(f=arg_tuple[0],k=arg_tuple[1],l=arg_tuple[2],debug=arg_tuple[3])


def load_pair_orbital_couplings_pool(k,l,thoroughness=1):

    file_base = "new_proc_wan_"
    indices = range(0,400,thoroughness)
    file_names = [file_base+str(i) for i in indices]

    p=Pool(12)

    data_pieces = p.map(load_orbitals_pool, [[f,k,l,False,] for f in file_names])
    
    flat_data=[item for sublist in data_pieces for item in sublist]

    return np.array(flat_data)
 

def load_all_orbital_couplings_serial(thoroughness=1):

    file_base = 'new_proc_wan_'
    indices = range(0,400,thoroughness)
    file_names = [file_base+str(i) for i in indices]
    
    timer=True
    debug=True
    data_pieces=[]
    all_lines=[]
    for f in file_names:
        if timer: t0=time.time()
        if debug: print("Now reading in file",f)
        with open(f,'r') as f_:
            thelines=f_.readlines()[1:]
            
            thelines=[line.split(',') for line in thelines]

            thelines=[ [float(x[n]) for n in [2,5,6,7,8,9]] for x in thelines]
            all_lines+=thelines

        if timer: print("Read file %s which took %f seconds" %(f, time.time()-t0))

    if debug: print("returning array with dimension", np.array(all_lines).shape)
    return(np.array(all_lines))


    
    

#TODO: ADD TO THIS
load_all_orbital_couplings_serial(thoroughness=10)
exit()


t0 = time.time()
ser = load_pair_orbital_couplings_serial(1,1,1)
t1 = time.time()
print("Total serial run took %f seconds" %(t1-t0))

tot_time_all = t1-t0

t2 = time.time()
ser=load_pair_orbital_couplings_serial(1,1,10)
t3 = time.time()

print("Abbreviated serial (only every 10th data set) run took %f seconds" %(t3-t2))

tot_time_abb = t3-t2


t4 = time.time()
par = load_pair_orbital_couplings_pool(1,1,1)
t5 = time.time()
print("Total parallel run took %f seconds" %(t5-t4))

t6 = time.time()
par= load_pair_orbital_couplings_pool(1,1,10)
t7=time.time()
print("Abbreviated parallel run (only every 10th data set)  took %f seconds" %(t7-t6))

print(par==ser)


