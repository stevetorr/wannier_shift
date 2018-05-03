import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
import scipy.interpolate as interp
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark import SparkConf, SparkContext
import sys
import time
import copy as copy

#this function filters df by atom_from_index and atom_to_index
#def load_all_orbital_couplings(k,l):
#    df2 = df.filter((df.atom_from_index == k) & (df.atom_to_index == l))
#    df2_np = np.array(df2.select('hop_vec_x','hop_vec_y','hop_vec_z','ham_real').collect())
#    df2_npf = df2_np.astype(np.float)
#    return df2_npf

def load_all_orbital_couplings(k,l):
    aa = spark.sql("select hop_vec_x,hop_vec_y,hop_vec_z,ham_real from fun where atom_from_index = '%d' AND atom_to_index = '%d'" % (k,l)).collect()
    df2_np = np.array(aa)
    df2_npf = df2_np.astype(np.float)
    return df2_npf

def load_all_orbital_couplings_serial(k,l,thoroughness=1):
    """
    For profiling purposes, try to perform a crummy query of the relevant information.
    """
    file_base = 'new_proc_wan'
    indices = range(0,400,thoroughness)
    file_names = [file_base+str(i) for i in indices]

    data_pieces=[] 

    for f in file_names:
        with open(f,'r') as f_:
            thelines=f_.readlines()[1:]
            
            hits = [line.split(',') for line in thelines if (int(line.split(',')[2])==k and line.split(',')[5]==l)]
            
            hits = [    [float(hit[n]) for n in [6,7,8,9]] for hit in hits]
            data_pieces.append( list(hits) )


    print(data_pieces)
                



def reduce_index(n):
    """
    Maps an input d-orbital to a value from 0-4,
    Maps an input p-orbital to the b
    
    The desired enumeration is:
    [0,1,2,3,4]: D-Orbitals
    [5,6,7]: Upper P-orbital
    [8,9,10]: Lower P-orbital
    """
    n-=1
    if n in [0,1,2,3,4]: # D ORBITALS IN THE BOTTOM LAYER
        return n
    
    if n in [5,6,7,8,9]: # D ORBITALS IN THE TOP LAYER
        return n-5
    
    if n in [10,11,12]: # TOP P ORBITAL FOR BOTTOM LAYER
        return n-5
    
    if n in [13,14,15]: # BOTTOM P ORBITAL FOR BOTTOM LAYER
        return n-5
    
    if n in [16,17,18]: # TOP P ORBITAL IN THE TOP LAYER
        return n-11
        
    if n in [19,20,21]: # BOTTOM P ORBITAL IN THE BOTTOM LAYER
        return n-11
    

    print("Warning!! Passed an index that is not in [0,21], not acceptable bounds!")


def upper_or_lower(index):
    """ Returns 0 if an index starting at 1 is in the lower bilayer, returns 0 if in the top.
    """
    if index in[1,2,3,4,5,11,12,13,14,15,16]:
        return 0
    if index in[6,7,8,9,10,17,18,19,20,21,22]:
        return 1

class atom(object):
    """
    Contains three attributes:
    
    int layer : 0 or 1 depending on lower/upper
    tuple index (int,int) which specifies where it is on it's original undistorted bravais lattice
    tuple position (float,float) or (float,float,float) depending on if we have xy or xyz 
    """
    def __init__(self,layer=0,index=(0,0),position=(0,0)):
        self.layer=layer # takes form 0,1
        self.index=index # takes form (n,m) or 'None'
        self.position= position #takes form (x,y) or #(x,y,z)
        

def sort_atoms_by_layer(atoms):
    
    bots=[atom for atom in atoms if atom.layer==0]
    tops=[atom for atom in atoms if atom.layer==1]
    
    return bots+tops
    
def generate_atom_positions(A,R,Nmin,Nmax,Mmin,Mmax,z=3.5):
    """
    Generates a simple rotation with no relaxation and a constant z coordinate
    
    np array A : Matrix of 2D bravais lattice which goes [[a11, a21],[a12,a22]] acting on [n,m]
    np array R : Matrix which rotates the lattice
    int N:       Extent of one direction of the lattice
    int M:       Extent of another direction of the lattice
    """
    indices=[]
    positions=[]
    
    atoms=[]
    # Set up (n,m) integer tuples which index the atoms in each lattice
    for n in range(Nmin,Nmax):
        for m in range(Mmin,Mmax):
            indices.append((n,m))
            
    # Obtain positions by multiplying the indices by the Bravais matrix A
    for x in indices:
        # Generate bottom layer 'atom'
        newpos=np.append(np.dot(A,np.array(x)),(0))
        atoms.append(atom(layer=0,index=x,position=newpos))
        # Generate top layer 'atom'
        newpos=np.append(np.dot(np.dot(R,A),np.array(x)),z)
        atoms.append(atom(layer=1,index=x,position=newpos))
        
    
    # List of objects of type atom
    return atoms
        
    
def plot_atom_positions(atoms):

    bot_atoms=[at for at in atoms if at.layer==0]
    top_atoms=[at for at in atoms if at.layer==1]
    
    plt.figure()
    plt.scatter([at.position[0] for at in bot_atoms], [at.position[1] for at in bot_atoms],color='b',label='Bottom')
    plt.scatter([at.position[0] for at in top_atoms], [at.position[1] for at in top_atoms],color='r',label='Top')
    plt.legend()
    plt.show()
    
def print_atom_positions(atoms,filename):
    
    with open(filename,'w') as f:
        for at in atoms:
            at_str=str(at.position[0])+','+str(at.position[1])+',' + str(at.position[2])+'\n'
            f.write(at_str)
    
def read_positions(file):
    
    ## Assumes data which is formatted as 
    #  x,y,layer   | with type | float, float, 0 or 1
    # or 
    # x,y,z, layer | with type | float, float, float, 0 or 1
    #  for when we implement z-relaxation.
    
    
    with open(file,'r') as f:
        thelines=f.readlines()
        
    ####################
    # This chunk of code checks to see if there is a alphabet letter in the first line
    # which is a reasonable expectation for the header. If there is a header, it starts on the second line.
    ####################
    alphabet="abcdefhijklmnopqrstuvwxyz"
    alphabet=[alphabet[i] for i in range(26)]
    start_idex=0
    for letter in alphabet:
        if letter in thelines[0].lower():
            start_index=1
    
    ####################
    # Turn the lines into atoms
    ####################    
    
    atoms=[None]*len(thelines[start_index:])
    for n in range(len(thelines[start_index:])):
        [xpos, ypos, layer] = thelines.split(',')
        atoms[n] = atom(layer=int(layer), position=(float(xpos),float(ypos)))


    return atoms

def unit_cell_modulus(A,Dx,Dy,Ainv=None):
    """ 
        
        Assumes A has the form
        
        [a1x, a2x] [n] = [x]
        [a1y, a2y] [m] = [y]
        
        so takes the transpose to make it
        
        [A1x, A1y]
        [A2x, A2y]
                
        Takes an x,y position and modulates it into the unit cell.
        
        Works by solving the system of equations
        x = c * a1_x  + d a2_x
        y = c * a1_y  + d a2_y 
        
        Then taking the coefficients c and d modulo 1, which places them into the unit cell.
        
        If this will be called many times, pass the inverted matrix A in as Ainv.

    
    """
    if Ainv is None:
        Ainv = la.inv(A.T)
    indexes=np.dot(Ainv,np.array([Dx,Dy]))   # Obtain c and d   
    print(indexes)
    indexes=np.array([x%1 for x in indexes]) # Modulate by 1
    print(indexes)

    unit_cell_pos= np.dot(A.T,indexes)         # Put back into real space
    return unit_cell_pos[0],unit_cell_pos[1]

#print(unit_cell_modulus(A,51,1))


def build_model_draft_2(atoms):
    """ 
    DRAFT 2: DOES INTERLAYER COUPLING ONLY
    
        variable : datatype, description 
        ---
        atoms: list, of objects of type atom
        
        Structure matrix so upper-left quadrant is bottom layer, lower-right is top layer
        Convention is 1,2,3,4,5: D
                      6,7,8: p_bottom
                      9,10,11: p_top
                      
    """
    
    atoms=sort_atoms_by_layer(atoms)
    bot_atoms=[atom for atom in atoms if atom.layer==0]
    top_atoms=[atom for atom in atoms if atom.layer==1]


    Nbot=len(bot_atoms)
    Ntop=len(top_atoms)
    
    NN = len(atoms) # Get length of input set of atoms
    
    TBH = np.empty(shape=(NN*11,NN*11)) # Pre-allocate orbital-orbital coupling matrix    
    
    
    # Loop over all atoms, computing each individual displacement
    displacements=np.empty(shape=(NN,NN,3))

    timer=True
    debug=False

    for i in range(NN):
        for j in range(NN):
            for n in range(3):
                if debug:
                    print(atoms[j].position[n] - atoms[i].position[n])
                    print('nominally assinging to ',i,j,n,atoms[j].position[n]-atoms[i].position[n])
                displacements[i][j][n]= atoms[j].position[n]- atoms[i].position[n]
                if debug:
                    print('and here it is:',displacements[i][j][n])
            if debug:
                print('Here is the register at',i,j, 'with disp value', displacements[i][j][:])
    if debug:
        print("Done with displacements")
        print('here is displacements',displacements)
        print('Total atom count NN is',NN)
        print("TBH has shape",TBH.shape)

    done_combinations=[]
    if debug:print('random test: here"s 1,2',displacements[1][2][:])
    for k in range(1,23):
        for l in  range(1,23):
            if (k,l) in done_combinations or (l,k) in done_combinations:
                continue
            else:
                # Intralyer matrices will have this property of all orbitals being the same across atoms
                tier=upper_or_lower(k)+upper_or_lower(l)
                if tier==0 or tier==2:
                    done_comibinations.append((k,l))
                #done_combinations.append((k,l))
           
            print("Processing coupling between orbital %d and %d (~ %.1f %%) " %(k,l, 100*(((k-1)*23+(l-1)))/231. ))
            tstart=time.time()
            couplings = load_all_orbital_couplings(k,l)
            tend=time.time()
            if timer: print("Loaded in couplings between %d and %d, which took %f seconds" %(k,l, tend-tstart))
            if debug: 
                print("Couplings, which has shape:",couplings.shape)
                print(couplings)
            
            # Coupling has shape [[x,y,z],[real,imag],n]
            data_disps = np.array([[coup[i] for i in range(3)] for coup in couplings])
            
            if debug: 
                print("Displacements, which has shape:",data_disps.shape)
                print(data_disps)
                print("And a minimum z displacement of", np.min(data_disps[:][2]))
                print("And a maximum z displacement of:", np.max(data_disps[:][2]))
        
            real_vals = np.array([coup[3] for coup in couplings])

            if debug: 
                print("Hamiltonian Term, which has shape:",real_vals.shape)
                print(real_vals)            
                with open('couplings','w') as f: np.save(f,couplings)
                with open('disps','w') as f: np.save(f,data_disps)
                with open("real_vals",'w') as f: np.save(f,real_vals)
                with open('atom_disps','w') as f: np.save(f,atom_disps)
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html#scipy.interpolate.griddata
            
            
            if upper_or_lower(l)+upper_or_lower(k)==0:
                atom_disps=[0]*Nbot**2
                for i in range(Nbot):
                    for j in range(Nbot):
                        if debug: print('assigning by',i,j,displacements[i][j][:])
                        atom_disps[i*Nbot+j]=copy.copy(displacements[i][j][:])

            
            if upper_or_lower(l)+upper_or_lower(k)==1:
                atom_disps=[0]*Nbot*Ntop
                for i in range(Nbot):
                    for j in range(Ntop):
                        atom_disps[i*Nbot+j]=copy.copy(displacements[i][Nbot+j][:])

            if upper_or_lower(l)+upper_or_lower(k)==2:
                atom_disps=[0]*Ntop**2
                for i in range(Ntop):
                    for j in range(Ntop):
                        atom_disps[i*Ntop+j]=copy.copy(displacements[Nbot+i][Nbot+j][:])

            if debug: print('atom disps is',atom_disps)
            #print("and has shape,",atom_disps.shape)
            atom_disps=np.concatenate(atom_disps,axis=0)
            atom_disps=atom_disps.reshape((len(atom_disps)/3,3))
            tstart=time.time()
            if debug:print('Sahe pf atom disps is', atom_disps.shape)
            couplings= interp.griddata(points=data_disps[:,:2],values=real_vals,xi=atom_disps[:,:2],fill_value=0)
            
            if debug: print('Shape of couplings is',couplings.shape)
            tend=time.time()
            if timer: print("Interpolated couplings, which  took %f seconds" %(tend-tstart))
            
            ##############
            # This next bit of code makes the matrix symmetric, but also makes the sub-matrix symmetric for 
            # INTRA-layer couplings but not for INTER layer couplings, because the 
            #      orbitals (top vs bottom p) have different meanings for the top and bottom layers)
            ##############3

            # Bottom-Bottom Couplings
            if upper_or_lower(l)+upper_or_lower(k)==0:
                for i in range(Nbot):
                    for j in range(Nbot):
                        #Symmetrize TBH  (interchange i<->j, k<-> l) 
                        TBH[i*11+reduce_index(k) , j*11+reduce_index(l)] = couplings[i*Nbot+j]
                        TBH[j*11+reduce_index(l) , i*11+reduce_index(k)] = couplings[i*Nbot+j]
                        
                        #Symmetrize sub-matrix (interchange k<-> l)
                        TBH[i*11+ reduce_index(l),  j*11+reduce_index(k)] = couplings[i*Nbot+j]
                        TBH[j*11+ reduce_index(k) , i*11+reduce_index(l)] = couplings[i*Nbot+j]
            
            # Bottom-Top Couplings
            if upper_or_lower(l)+upper_or_lower(k)==1:
                #for i in range(Ntop):
                #    for j in range(Nbot):
                #        TBH[Nbot + i*11 + reduce_index(k) , 0    + j*11 + reduce_index(l)] = couplings[i*Ntop+j]
                #       TBH[0    + j*11 + reduce_index(l) , Nbot + i*11 + reduce_index(k)] = couplings[i*Ntop+j] 

                for i in range(Nbot): 
                    for j in range(Ntop):
                        # Set the upper-right (bottom to top) coupling
                        TBH[ 0    + i*11 + reduce_index(k) , Nbot + j*11 + reduce_index(l)] = couplings[i*Nbot+j]
                        TBH[ Nbot + j*11 + reduce_index(l) , 0    + i*11 + reduce_index(k)] = couplings[i*Nbot+j]
            
            # Top-Top Couplings
            if upper_or_lower(l)+upper_or_lower(k)==2:
                for i in range(Ntop):
                    for j in range(Ntop):
                        #Symmetrize TBH (interchange i<->j, k<-> l )
                        TBH[Nbot + i*11+reduce_index(k),Nbot + j*11+reduce_index(l)] = couplings[i*Ntop+j]
                        TBH[Nbot + j*11+reduce_index(l),Nbot + i*11+reduce_index(k)] = couplings[i*Ntop+j]

                        #Symmetrize Sub-matrices (interchange k<->l)
                        TBH[Nbot + i*11+reduce_index(l),Nbot + j*11+reduce_index(k)] = couplings[i*Ntop+j]
                        TBH[Nbot + j*11+reduce_index(k),Nbot + i*11+reduce_index(l)] = couplings[i*Ntop+j]
      
    return TBH



if __name__=="__main__":
#setting up and caching df
    conf = SparkConf().setMaster('local[12]')
    sc = SparkContext(conf = conf)
    sc.setLogLevel("WARN")
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL basic example") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()
    sqlContext = SQLContext(sc)
    spark.read.format("parquet").load("myparquet.parquet").createOrReplaceTempView("fun")



    # Physics Parameters
    a= 3.314 # Lattice constant of material (TaS2)
    A = np.array([[np.sqrt(3)/2, -.5],[np.sqrt(3)/2, .5]]) * a      #Ta S2
    theta = 1.05 # Angle of rotation in degrees  
    theta_r= theta* np.pi / (180.)   # Convert to radians
    R = np.array([ [ np.cos(theta_r), - np.sin(theta_r)],[np.sin(theta_r), np.cos(theta_r)]]) # Rotation Matrix
    
    TBH=build_model_draft_2(generate_atom_positions(A,R,0,2,0,2))
    print(TBH)


    with open("TBH",'w') as f:
        np.save(f,TBH)
