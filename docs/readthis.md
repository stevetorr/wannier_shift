# wannier_shift
Interpolating Wannier functions for TMDC Heterostructure Tight-Binding Hamiltonians

Our website is [here](https://stevetorr.github.io/wannier_shift/header).

# Description of Files in Top Folder

## serial_query_profile.py

Serial_query_profile.py is a standard Python code generated to obtain the serial execution time of a single query along with a parallel execution time with a worker Pool. It reads all files into local memory, goes through every line of each file, and uses a list comprehension to parse the lines to find the desired k and l orbitals. It returns the lines as a list of floating point values (Dx,Dy,Dz,Coupling), and the time it takes from loading files to returning these values is collected and printed for each file.

When this code is executed, four tasks are completed – two serial and two parallel loadings, for all 400 files and for every N (“thoroughness”) files. The default N is 10, and the default number of workers is 12.

## spark_query.py

Spark_query.py compares three spark-based implementations. All of them start by reading 400 data files into one dataframe, and return the floating point values as a numpy array. In the first implementation, the dataframe is transformed by dataframe.filter( ). Another implementation creates a temporary view of the dataframe and runs SQL directly on it. The last implementation partitions and writes the data in the format of parquet. The data are stored in new directories, with partitioning column values encoded in the path of each partition directory. When querying by orbital indices k and l, the data in the corresponding partition directory will be queried directly. Running this code gives the execution time of each implementation in an easily comparable format.

## generate_model.py

Generate_model.py generates the Tight Binding Hamiltonian model, querying the already-generated parquet multiple times. It first constructs atom positions for the 2D material being studied, and computes displacements to perform interpolation and obtain corresponding electronic couplings. The TBH model is built from these couplings and printed in the output. In order to run this code, spark_query.py has to be first executed to create a parquet directory using the desired number of data files. The number of data files to be read can be specified by modifing the following part of spark_query.py.
```
# Set how many files needed to be read
files=[]
prefix='new_proc_wan_'
for i in range(400):
#if i % 2 == 0: Uncomment to run on every other file (200 files)
if i % 10 == 0: # this is for 40 files
files.append(prefix+str(i))
````

# Description of Folders

## docs
Where we store the website information, as well as the figures which are included in the website. The files in here represent individual pages, but we will briefly note that it has a subfolder called:

### Figures
Contains all of the figures which we generated for the website.

## project_presentations
Contains our final presentation, the original proposal, and one of our intermediate presentation slides (for archival purposes).

## example_run

### TBH.2x2
A pickled numpy 88x88 matrix which was generated from the model builder. This figure is featured in the results section.

### TBH_analyze.ipynb
An ipython notebook which generates the figures from TBH.2x2, and **OPTIONALLY** TBH.20x20, which is obtainable from the google drive on request. TBH.20x20 was not included in the repository because it's 700 MB.


## DFT-WAN

Below is a summary of the files in the DFT-WAN folder.

### gen_pos.py
This python script generates the batch of the varied crystal strcutre and corresponding wannier input parameter file for the DFT+Wannier procedure. All the generated files will be written to the allpos subfolder.

### allpos subfolder:
This contains the setup crystal structure files for the scanning from gen_pos.py script.

### vasp_wan.py
The script to loop over the DFT+Wannier procedure for all the 400 configurations from the crystal setup (read from allpos subfolder). This can be called from the job file submitted to the job manager on the cluser.

### data subfolder:
This will contain all the raw simulation data from running DFT+Wannier. Later it will be reprocessed by the wrapper and rewritten into more concise files.

### KSCAN subfolder:
This folder contains the main structure needed for running DFT VASP+Wannier90 method. In it, one can find SCF, BANDS and WAN subfolders. They are the steps to carry out the Wannier transformation and generate our own data set. Some descriptions of them can be found in the GitHub webpage and VASP official website. In the recursive process of generating the data, this folder will be copied and combined with the corresponding crystal configuration data from allpos to run the simulation.

### rec_proc_mp.py
After the simulation for 400 configurations has been carried out, one can then proceed with the post-processing (or the wrapper) of the simulation data. This script will go through all the data generated and reformat and clean up the information to prepare them as the input for the database. Note that this script is the parallel version to handle several data sets at the same time using multiple cores.

Flow of simulation of DFT+Wannier:

1) setup the crystal configurations to be sampled:
gen_pos.py

2) Loop over these configurations with VASP+Wannier90:
vasp_wan.py

3) Post-process of the simulation results:
rec_proc_mp.py







