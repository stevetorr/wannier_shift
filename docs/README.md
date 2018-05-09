# wannier_shift
Interpolating Wannier functions for TMDC Heterostructure Tight-Binding Hamiltonians


# Description of Folders

## docs
Where we store the website information, as well as the figures which are included in the website. The files in here represent individual pages, but we will briefly note that it has a subfolder called:

### Figures
Contains all of the figures which we generated for the website.

## project_presentations
Contains our final presentation, the original proposal, and one of our intermediate presentation slides (for archival purposes).

##





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







