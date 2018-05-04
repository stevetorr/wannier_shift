import numpy as np
import time as time
from multiprocessing import Pool
import matplotlib.pyplot as plt

""" 
The point of this file is to profile in a semi-automatic way the comparative
speed of querying all of the orbitals in the Wannier-coupling database in order to compare the querying process with and without spark. 

"""


def load_pair_orbital_couplings_serial(k,l,thoroughness=1,debug=False,timer=True):
    """
    Takes as arguments orbitals k and l, and returns the data corresponding to the coupling between those two orbitals.

    Returns a numpy array of (Dx, Dy, Dz, Coupling) x number of data points.

    Load into memory all four hundred data files and extract the relevant data points for each orbital l and k. (Or, for every nth file, where n is specified by the thoroughness variable, e.g. =2 means every other file, =4 is every fourth file, etc.

    For profiling purposes, try to perform a serial query of the relevant information.
    """

    # Establish the indices for the files

    file_base = 'new_proc_wan_'
    indices = range(0,400,thoroughness)
    file_names = [file_base+str(i) for i in indices]

    # The resultant data points will be stored in data_points
    data_points=[]

    for f in file_names:
        if timer: t0=time.time()
        if debug: print("Now reading in file",f)
        
        # obtain the data points from the orbital files
        # and then store them in the data points array
        new_data=load_orbitals_python(f,k,l)
        for point in new_data:
            data_points.append(point)

        if timer: print("Read file %s which took %f seconds" %(f, time.time()-t0))

    if debug: print("returning array with dimension", np.array(data_points).shape)
    return(np.array(data_points))



def load_orbitals_python(f,k,l,debug=False):
    """

    Takes as arguments a string corresponding to a file name f, 
    orbitals k and l, and returns the data corresponding to the coupling between those two orbitals.

    Returns a numpy array of (Dx, Dy, Dz, Coupling) x number of data points.

    Load into memory all four hundred data files and extract the relevant data points for each orbital l and k. (Or, for every nth file, where n is specified by the thoroughness variable, e.g. =2 means every other file, =4 is every fourth file, etc.

    Called 'load orbitals python' because it only uses standard python functions (nothing like Spark, etc).

    """

    with open(f,'r') as f_:
        # Load in lines but skip the header
        thelines=f_.readlines()[1:]

        if debug:
            print('Heres the first line',thelines[1])
            print('Here are the orbitals to and from:', int(thelines[1].split(',')[2]), thelines[1].split(',')[5] )

        # Use a list comprehension to parse the lines in the file to find the desired k and l orbitals
        hits = [line.strip().split(',') for line in thelines if ( (int(line.split(',')[2])==k and line.split(',')[5]==l) or (int(line.split(',')[2])==l and  int(line.split(',')[5])==k)) ]
        
        if debug:
            print("Found %d hits" % len(hits))

        # Returns the lines as a list of floating point values (Dx,Dy,Dz,Coupling)
        return [[float(hit[n]) for n in [6,7,8,9]] for hit in hits]

def load_orbitals_pool(arg_tuple):
    """
    Simple helper function to make the python worker pool successfuly interface with the load_orbitals_python function.
    
    arg_tuple has form (filename string, orbital from, orbital to, debug mode on or off).
    """
    return load_orbitals_python(f=arg_tuple[0],k=arg_tuple[1],l=arg_tuple[2],debug=arg_tuple[3])


def load_pair_orbital_couplings_pool(k,l,thoroughness=1,num_workers=12):
    """ 
    Using the multiprocessing module's worker pool, load in the four hundred data files and extract the relevant coupling for k and l orbitals.
    
    k and l are the orbital indices of from and to, thoroughness means only read every nth file, where n is the vlaue of thoroughness.

    """

    file_base = "new_proc_wan_"
    indices = range(0,400,thoroughness)
    file_names = [file_base+str(i) for i in indices]


    # Instantiate worker pool

    p=Pool(num_workers)

    # Extract the data points as a list of lists of data points, which are themselves lists
    data_points = p.map(load_orbitals_pool, [[f,k,l,False,] for f in file_names])
    
    # Flatten the previous list of lists into merely a list of data points
    flat_data=[item for sublist in data_points for item in sublist]

    # Convert into numpy array and return
    return np.array(flat_data)
 

def load_all_orbital_couplings_serial(thoroughness=1):
    """
    A function which loads in all of the orbital couplings to memory.
    We did not investigate this proedure because we realized very quickly it would not scale with larger data sets.
    """
    file_base = 'new_proc_wan_'
    indices = range(0,400,thoroughness)
    file_names = [file_base+str(i) for i in indices]
    
    timer=True
    debug=True
    data_points=[]
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


    
if __name__=='__main__':    

    print('Now profiling the file query process. Please run this in the same folder as the new_proc_wan files.')
    print("====================")
    N=1
    print("Now reading in every data file in serial with thoroughness  %d" % N)
    t0 = time.time()
    #ser = load_pair_orbital_couplings_serial(1,1,N)
    t1 = time.time()
    print("Total serial run took %f seconds" %(t1-t0))

    tot_time_all = t1-t0

    print("====================")
    print("Now loading in every 10th file in serial.")
    t2 = time.time()
    ser=load_pair_orbital_couplings_serial(1,1,10)
    t3 = time.time()
    print("Abbreviated serial (only every 10th data set) run took %f seconds." %(t3-t2))

    tot_time_abb = t3-t2

    print("====================")

    num_workers=12

    print("Now loading in all files using a worker pool, using %d workers" %num_workers)
    t4 = time.time()
    par = load_pair_orbital_couplings_pool(1,1,1,num_workers)
    t5 = time.time()
    print("Total parallel run took %f seconds" %(t5-t4))

    print("====================")

    print("Now loading in every 10th file using a worker pool of %d workers" %num_workers)
    t6 = time.time()
    par= load_pair_orbital_couplings_pool(1,1,10,num_workers)
    t7=time.time()
    print("Abbreviated parallel run (only every 10th data set)  took %f seconds" %(t7-t6))

    print("Checking to make sure that the two data sets are consistent:")
    for x in par==ser:
        if x.any()==False:
            print("Warning! A discrepancy in data points was found between orbitals 1 and 1. The two methods should be the same.")

    print("Validation complete!")
