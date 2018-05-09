# Wannier Shift
## A project by Shiang Fang, Eri Muramoto, Steven Torrisi, and Tianning Zhao


## [Intro, Background, and Motivation](https://stevetorr.github.io/wannier_shift/background) 


## Introduction, Background, and Motivation

## Physical Background: Motivation for Layered Materials

Conventional bulk solids are made of three-dimensional crystals with strong chemical bonding in between atomic constituents. Ever since the discovery of graphene \[[Nobel2010](https://www.nobelprize.org/nobel_prizes/physics/laureates/2010/press.html)\], there have been intense reserach investigations on  layered materials. These are materials with strong chemical bonding between the atoms in the same sheet and weaker van der Waals interactions between the neighboring sheets. Because of the nature of the weak interlayer bonding, individual sheets of atoms can be exfoliated via a mechanical method involving scotch tape. Ever since, the library of experimentally accessible 2D materials is constantly growing with new types of layers that can be exfoliated or fabricated. They can host a variety range of physical properties as well. For example, some layers can be magnetic or superconducting. There are great implications for the applications using these layered materials in industry or fundamental research.

Because they are sheets of materials, one might be interested in stacking different layers together to form a stack like a sandwich and hope to engineer the stack with the desired properties by combining them properly. There are many 'control knobs' in forming the stack. For example, what types of layers could be used, and what the stacking twist angle and the geometry could be. Though it is exciting to imagine the possibility to use these layered materials, theoretically it is extremely challenging to simulate the layer stacks and give insights for the experimental parameters to be tested. 

To understand the difficulty, we can first look at the system from a geometric point of view. Moire patterns is the interference pattern created when two similar images are overlapping with each other. It can be observed in daily life such as the photography.

## ![Moire Pattern from Wikipedia](moire_pattern.png) 
### This moire pattern photo is taken from the wikipedia page  on [Moire Patterns](https://en.wikipedia.org/wiki/Moir%C3%A9_pattern). It shows two identical planes of lines at a relative twist angle $\alpha$. Note the periodic pattern that emerges in their overlap, which is characterized not just by the planes themselves but by $\alpha$.

The overlap between two images would create a long-wavelength varying pattern in the combined image. The scale of this long-wavelength variation is determined by the degree of the mismatch between layers. The smaller the mismatch is, the larger the length scale is for the spatial variations. The similar phenomena would occur for atomic crystals as well and the two-dimentional geometry for the layered materials are perfect to illustrate Moire pattern physics. 

For the example of the graphene, if we have two sheets on top of each other and with about 1 degree twist angle, the Moire pattern would have a length scale about 13 nanometer and it has a triangle lattice structure. This super-structure, the large length scale atomic variation usually contains over **10,000 atoms** and this causes tremendous challenges for numerical simulations for these twisted bilayer system.

However, if we zoom in on these twisted bilayer system, we can see locally they resemble the perfect aligned crystal with the relative shift between layers that depends on the location in the super-structure. In other words, this large scale sctructure can be viewed as made of patching of various configurations of aligned crystals that has much a smaller size. Intuitively one can imagine that by studying the smaller structure of the crystal and their electronic properties and how they depend on the crystal layer shift, we can infer or construct the corresponding patched super-structure and reduce the computational resources that are needed to perform the simulation. This is in line with the multi-scale simulations. The DFT+Wannier technique mentioned above provides the necessary toolset for performing such task. First, for the smaller periodic crystal, the DFT+Wannier method is used to extract the orbital information, their coupling strength and the electronic properties, and how they vary with interlayer shift. After the basic ingredients for the modeling are obtained, we can patch these local models to form the global model for the super-structure and perform the electronic simulations. 

Overcoming this theoretical challenge to simulate the van der Waals heterostructure and twisted structure is crucial to advance the current semiconductor industry and fundamental physics research. One of the recent excitement is the discovery of superconductivity in the twisted bilayer graphene at "magic angle" (about one degree). An associated perspectives article is here: \[[Surprise graphene discovery could unlock secrets of superconductivity](https://www.nature.com/articles/d41586-018-02773-w)\]. For each individual graphene monolayer, superconductivity is not present unless it is in proximity with other conventional superconductors. The superconductivity displayed this way is not intrinsic to the graphene layers. However, what is really interesting and surprising is that when two layers of graphene are stacked with a small magic twist angle, the bilayer heterostructure becomes superconducting at about 1 Kelvin and it is intrinsic transport property. The origin of this suerpconductivity phase is still under intense debte and subject of current research now. However, it is related to the peculiar electronic band structure in the twisted bilayer graphene. At this magic angle, a set of nearly flat bands are present and these bands with low dispersion and quenched kinetic energy are usually beneficial for inducing stronger interaction effects (from electron-electron mutual interaction). Ths superconductivity is expected to originate from the enhanced interaction effects.

## ![Moire Pattern in Graphene](../figures/graphene_moire.jpg)

## From the [Nature views article](https://www.nature.com/articles/d41586-018-02660-4). The moire pattern that graphene produces is clearly visible.

Looking forward to the research with these van der Waals layer stacking, there are many open questions. How could we determine or engineer the proper layer structure and what is the geometry that we should create in order to manipulate the electronic properties to what we desire, how to optimize the combinations, and what should we be expecting for the new physics to emerge. These are extremely challenging and exciting to explore, but the efficient numerical approach and toolset are necessary to perform these simulations. One strong benefit of creating the database and having very efficient ways of querying the data entries for the related crystal types and geometry is extremely valuable to advance the theoretical approach. With the growing number of two-dimentional layered materials and various forms, our database can also be extended to many types and symmetries. One can proceed with the truly ab-initio simulations of these layer stacks, or derive the corresponding low-energy expansions and various handy models to describe them.

Density functional theory (DFT) is the workhorse of computational condensed matter physics and physical chemistry. It allows users to compute a wide variety of material properties, such as electronic and mechanical structure, phonon/vibrational behavior, and geometric phase phenomena. However, DFT does not scale favorably with system size, and performing complicated electron orbital-structure or mechanical relaxation calculations for systems with more than a few dozen atoms becomes intractable. 

DFT typically generates wavefunctions that are in the plane-wave basis, so the periodicity across a crystal is easy to exploit. However, the use of an alternate wavefunction basis, Maximally Localized Wannier Functions (MLWF), allow us to visualize the electrons as being localized on individual atoms as well as determine the physical interaction strength, or coupling, between different orbitals. It can be advantageous to study a system from the basis of individual orbitals coupling to one another, as such a mathematical framework turns most calculations of system properties into comparatively fast routine linear algebra calculations.

Therefore, MLWF’s are useful to bring the toolset of DFT to bear on large systems. For instance, one of our group members demonstrated how parameterizing a tight binding model for Transition Metal Dichalcogenides could come from MLWF’s and DFT. \[[Fang 2015](https://arxiv.org/abs/1506.08860)\]; learning how to model two-dimensional twisted systems is a vigorous and active field of research, spurned on by the recent discovery of twisted bilayer graphene superconductors.

In order to study twisted bilayer TMDC systems, we need to understand the interactions between atoms in a wide variety of spatial configurations; even for modest twist angles, the periodicity which is necessary for DFT calculations is only accessible by very large systems of hundreds of atoms. Therefore, a tight-binding model informed by Wannier functions is one of the precious few techniques we have to approach calculating properties of twisted 2D systems.



## [Project Overview and Methods](https://stevetorr.github.io/wannier_shift/plan)

## Overview and Methods

Our chief concerns are as follows. It is very time-expensive to generate data sets for different bilayer material configurations. The DFT + Wannierization software is already optimized for parallel execution over cores, and is best regarded as a black box; therefore, embarrassingly parallel execution of the code via a wrapper code for a wide variety of configurations is how we aim to optimize this step. For the management and utilization of the resulting dataset, we turn to Spark and examine other database models to rapidly query the database for different orbital-orbital coupling strengths. The advantage of this parallelization is that it allows for faster querying of the computed values for accurate tight-binding Hamiltonian parameterization.



### Our Method


### DFT+Wannier method:
DFT is the state of the art microscopic quantum mechanical simulation for materials, however it is not straightforward to derive the physics picture from the massive information output from running a DFT simulation. Intuitively what Wannier transformation does is to interpret the DFT calculation results in terms of localized Wannier function basis. These can be thought of as the chemical atomic orbitals that participate in the bonding and hybridization of the electrons. As the byproduct, the electronic properties is captured in the Wannier tight-binding model that encapsulate various bonding strength inside the crystal. The first step is to apply this DFT+Wannier method to various types of two-dimensional layers and derive their corresponding tight-binding models. This procedure immediately gives intuitive and clear physics picture for the orbital hybridization as illustrated in the figure for the model we derive for a typical transition metal dichalcogenide layer. We can see the participating orbitals at low energy are the d orbitals from transition metal atoms and p orbitals from chalcogenide atoms. The counting of the orbitals is the following, there are 5 orbitals in Wannier d orbitals and 2 atoms with three p orbitals each. Hence, we have in total 5+2x3=11 orbitals for each single layer. The number would double when either the spin degrees of freedom is included or the second layer is added to the system. The focus of our project is to derive the interlayer coupling terms across the layers and they can be extracted with the DFT+Wannier method applied for the bilayer stack.


**INSERT FIGURE HERE**

#### VASP and W90
The extremely fine mesh of configurations which we produce via large batches of DFT calculations comprises a big compute phase of this project; we perform calculations of N>>100 configurations, each of which takes on the order of 15 minutes to generate the optimized electron wavefunction and then convert into Wannier functions appropriately. These runs are performed in the commercial Vienna Ab Initio Simulation Package \[[VASP](https://www.vasp.at/)\]. Calculations are run from a set of physical configuration parameters and run configurations, such as the spatial orientation of the unit cell, or a cutoff for how fine the density is resolved. The ‘Wannierization’ is performed by running Wannier90, a software package which converts wavefunctions from the plane-wave formulation to the Wannier function formalism.  



From there, the program outputs a list of the orbital-orbital couplings in the default wannier90 format. It creates one such file for each local configuration, which in our first batch included 400 different unit cells and VASP runs. We wrote and applied a wrapper which converts the data into a csv format for easy load-in to a spark data frame, as well as decorating it with information which assists our post-processing efforts. From there, we wrote a spark program which loads the 400 data files into one data frame for easy querying. As mentioned before, the tight-binding-Hamiltonian is entirely represented by a giant matrix, and we populate it by querying the spark database.



The primary development platform for our calculation was a workstation physically located at Harvard, in the Kaxiras group’s office space of Cruft Hall. The workstation runs OSX High Sierra  **INCLUDE A LOT OF TECHNICAL DETAILS ABOUT THE WORKSTATION, HERE**. 

## Profiling the Problem

In order to better understand where advantages of parallelization could come in to this problem, we first draw attention to the salient features of the problem.

### Data Generation - Big Compute

The batched data generation involves calling several hundred to several thousand different calculations of the VASP imeplementation of Density Functional Theory. All of the calculations' input parameters are deterministically generated and may proceed in any order; further, VASP is commercial software which is optimized already for parallel implementation on the per-calculation basis, exploiting multiple cores to more rapidly solve for the electronic density function and associated energy. **Therefore, the process of generating our data sets is ripe for embarassingly parallel MPI implementation.** 

##### Insert profiling information/figures about VASP calls here.


### Data Management - Big Data

Next, we turn to managing the data. When developing a tight-binding model for a system of atoms, we are attempting to map displacements between atoms (which arise from a twisting angle applied to a bilayer system) to the resultant coupling between their orbitals. In Transition Metal Dichalcogenide systems, we have 11 orbitals in the three-atom unit cell of a monolayer (2 sets of three p-orbitals for the Chalcogens, and five d-orbitals for the Transition Metal). In a twisted sample, we seek to find the orbital interaction between every pair of orbitals in the material. Therefore, we move from the displacements between individual atoms to the coupling strength of the atom's orbitals.

We obtain local information about how the orbital coupling should behave from the Wannierization. We end up with a data set of hundreds of displaced unit cells with associated orbital-orbital energy couplings. Querying this database is not trivial, and represents a query of several million data points to find the relevant values. Even loading the relevant data into usable memory is not a trivial task for the computer. **Therefore, managing this enormous dataset, and querying it efficiently, is ammenable to attack via Spark or other distributed database management frameworks.**. 

#### Querying the Database


To load in the 400 files takes a substantial amount of time in serial. It takes Python, using standard tools (reading all files into local memory then using a list comprehension to parse them for relevant orbital information) on average .7 seconds to read one 12-MB file and return the list of displacements and couplings strengths desired. This process relies only in I/O for a set number of files, and so it is amenable to embarassingly parallel implpementation. With the multiprocessing library and using a worker pool, we were able to dramatically reduce the amount of time for a query of the database by about an order of magnitude. However, since constructing the TBH requires $\mathcal O 100$ queries about orbital-orbital coupling information, even if a query takes $\mathcal O 10$ seconds, this results in TBH model generation taking at least on the order of hours for the querying of the files alone, not even taking into account other overheads and computationally intensive processes. Therefore, any efforts in bringing down the query time is a huge step forward towards efficient implementation.

To be clear, this trial involved loading the entire file set into memory every time. **((A BETTER TRIAL WOULD LOAD IN THE ENTIRE FILE SET AND THEN QUERY THAT MEMORY OBJECT MANY TIMES-- BUT IT'D BE ORDER 4.8 GIGABYTES, SO MAYBE THAT'S JUST BAD ON IT'S FACE?))**

We experimented with three spark-based implementations. For all of them, we started by reading 400 data files into one dataframe (a step which took order 8 seconds). At first, we directly tried the untyped transformations dataframe.filter( ). We did re-partitition the dataframe around the orbital data (which is how we query the database), hoping that this would accelerate the filter process. But there was no significant improvement. With this, individual queries took on the order of 25 seconds. We also tried spark.sql directly on a temporary view created from the dataframe and it turned out to have similar query time to the first one. 

To further improve data query performance, we tried another way to partition and query the data more efficiently. Instead of dataframe repartition, we write the partitioned data out in the format of parquet. The data are now stored in different directories, with partitioning column values encoded in the path of each partition directory. When querying the data by partition keys, only the data in the corresponding partition directory will be visited. This efficiently partitioned data structure accelerates the query process significantly. With this, individual queries took on the order of 4 seconds. Further tuning was attempted for parquet query. We tested some normal tuning parameters for Spark SQL, including caching in memory, shuffle partitions, broadcast join threshold, split computation and so on. Most of them are not making much difference. 

We decided to profile the perfomance of Python loading in a smaller subset of the files to compare with the parallel process. We briefly entertained this idea, reasoning that including fewer files could still yield a high-quality dataset which was physically motivated and accurate, while providing more efficient implementation.


|                      | 40 Files | 400 Files |
|----------------------|----------|-----------|
| Serial               | 28.80 s  | 295.51 s  |
| Parallel (12 Cores)  | 3.12 s   | 27.81 s   |
| Serial/12 Core       | 9.23     | 10.62     |
| Spark (12 Cores)     |          | ~ 8 s     |
| Parquet Spark        |          | ~ 4 s     |
| Speedup vs. Serial   |          | 73        |
| Speedup vs. Parallel |          | 6.95      |
#### Table 1. Comparison of Querying Times for Serial vs Parallel using Standard Python Tools.

#### (( We could also make a histogram-style plot to show the difference, which would be satisfying))


#### Interpolating From Data

From there, we understand that the twisted angle displacements will virtually never line up with the local samplings we took-- we have to perform an interpolation. Performing this interpolation may be computationally intensive for large numbers of real-space data points. **Black-box functions exist for Scipy to perform this implementation in a way easily compatible with Spark-- but it could be possible to help perform these queries in parallel.** 


**((We found that the interpolation time ranged from .4 to 2 seconds depending on the strength of the interaction between the two orbitals. The dependence on interaction is kind of a hypothesis, but whatever.))** 

We judged that heavily profiling the interpolation was not necessary, given that it is one or two orders of magnitude faster than the querying step in the naive Python implementation, and that it is only on the same order of magnitude as the querying for the full spark implementation.
Possible ways to improve the interpolation we judged were providing some sort of interface with a dedicated C++ library such as [Boost Python](https://www.boost.org/doc/libs/1_60_0/libs/python/doc/html/article.html). We did not deem these measures necessary for the project, as querying the database was still the rate-limiting step for most of development. However, if we were able to cut the implementation time approximately in half by reducing the querying time by an order of magnitude, it might be useful for future studies if/when we integrate this project into a research project.


##### Insert profiling information/figures about data interpolation here. If we want it.


 


## [Guide to Using Code](https://stevetorr.github.io/wannier_shift/guide)

### Code

In the course of developing an efficient look-up tool, we generated the following codes, which can be downloaded from:
https://drive.google.com/drive/folders/1TPO2H14AS_1CgilDmRqsAZzv_I4oeqrX?usp=sharing

- serial_query_profile.py 
- spark_query.py
- generate_model.py

#### serial_query_profile.py

Serial_query_profile.py is a standard Python code generated to obtain the serial execution time of a single query along with a parallel execution time with a worker Pool. It reads all files into local memory, goes through every line of each file, and uses a list comprehension to parse the lines to find the desired k and l orbitals. It returns the lines as a list of floating point values (Dx,Dy,Dz,Coupling), and the time it takes from loading files to returning these values is collected and printed for each file.

When this code is executed, four tasks are completed – two serial and two parallel loadings, for all 400 files and for every N (“thoroughness”) files. The default N is 10, and the default number of workers is 12. 

#### spark_query.py

Spark_query.py compares three spark-based implementations. All of them start by reading 400 data files into one dataframe, and return the floating point values as a numpy array. In the first implementation, the dataframe is transformed by dataframe.filter( ). Another implementation creates a temporary view of the dataframe and runs SQL directly on it. The last implementation partitions and writes the data in the format of parquet. The data are stored in new directories, with partitioning column values encoded in the path of each partition directory. When querying by orbital indices k and l, the data in the corresponding partition directory will be queried directly. Running this code gives the execution time of each implementation in an easily comparable format. 

#### generate_model.py

Generate_model.py generates the Tight Binding Hamiltonian model, querying the already-generated parquet multiple times. It first constructs atom positions for the 2D material being studied, and computes displacements to perform interpolation and obtain corresponding electronic couplings. The TBH model is built from these couplings and printed in the output. In order to run this code, spark_query.py has to be first executed to create a parquet directory using the desired number of data files. The number of data files to be read can be specified by modifing the following part of spark_query.py.

    # Set how many files needed to be read
    files=[]
    prefix='new_proc_wan_'
    for i in range(400):
      #if i % 2 == 0: Uncomment to run on every other file (200 files)
      if i % 10 == 0: # this is for 40 files
          files.append(prefix+str(i))

### Guide to Running on AWS

In order to compare different implementations and make our results reproducible, we ran all of the above codes on AWS. The following are the guides to re-run our experiments using 400 files for serial_query_profile.py and 40 files for the others. Modifications of the codes are not necessary unless you would like to try with other number of files. We used 200 files to produce some of our results, so we have included comments for curious readers.

#### Serial Loading

To execute serial_query_profile.py, please launch an AWS instance:

   - Amazon Machine Image (AMI): Ubuntu Server 16.04 LTS (HVM), SSD Volume Type
  
   - Instance type: 1 m4.4xlarge instance

No additional storage is required, and the default settings can be used for other configurations.
  
 
Confirm that Python is already installed:  

    $ python3 --version 
    $ Python 3.5.2
    
Then install the necessary packages:

    $ sudo apt-get update
    $ sudo apt-get install python-pip
    $ sudo pip install numpy  
    $ sudo apt-get install unzip

Now upload the zip file “new_proc_wan_serial” to the VM, and unzip:

    $ unzip new_proc_wan_serial.zip

After following these steps, the Serial_query_profile.py code should be ready to be run in the new_proc_wan_serial directory:
  
    $ cd new_proc_wan_serial
    $ python serial_query_profile.py

Successful run will provide you with an output that looks like this:

    Now profiling the file query process. Please run this in the same folder as the new_proc_wan files.
    ====================
    Now reading in every data file in serial with thoroughness  2
    Read file new_proc_wan_0 which took 0.350999 seconds
    Read file new_proc_wan_2 which took 0.157147 seconds
    Read file new_proc_wan_4 which took 0.331090 seconds
    ...
    Now loading in every 10th file using a worker pool of 12 workers
    Abbreviated parallel run (only every 10th data set)  took 1.942010 seconds
    Checking to make sure that the two data sets are consistent:
    Validation complete!


#### Loading using Spark cluster

In order to run the data loading code using a Spark cluster, please follow these steps:

First, create a Spark cluster: 

- General configuration: Logging – off, Launch mode – Cluster

- Software configuration: Release – emr-5.8.0, Applications – Spark

- Hardware configuration: Instance type - m4.4xlarge, Number of Instances - 3 (1 master and 2 core nodes)

Upload the following folder and scripts to the cluster and HDFS

- new_proc_wan_40_files, which contain 40 data files

- spark_query.py

- generate_model.py

After uploading all the files, this is what you should see: 

    $ hadoop fs -ls
    Found 42 items
    -rw-r--r--   1 hadoop hadoop       5451 2018-05-07 02:20 spark_query.py
    -rw-r--r--   1 hadoop hadoop      16361 2018-05-07 02:20 generate_model.py
    -rw-r--r--   1 hadoop hadoop   12502006 2018-05-07 02:29 new_proc_wan_0
    -rw-r--r--   1 hadoop hadoop   12953864 2018-05-07 02:29 new_proc_wan_10
    …
    -rw-r--r--   1 hadoop hadoop   12998283 2018-05-07 02:29 new_proc_wan_60
    -rw-r--r--   1 hadoop hadoop   12834758 2018-05-07 02:29 new_proc_wan_70
    -rw-r--r--   1 hadoop hadoop   12893863 2018-05-07 02:29 new_proc_wan_80
    -rw-r--r--   1 hadoop hadoop   12765595 2018-05-07 02:29 new_proc_wan_90


Submitting Spark_query.py will give you the execution times of different query methods described in XX. 

    $ spark-submit --num-executors 2 --executor-cores 1 Spark_query.py
    …
    ***************Reading files took 4.208967 second***************
    ***************Dataframe filter took 10.148717 second***************
    ***************Dataframe SQl took 8.787971 second***************
    ***************Partitioning took 111.486392 second***************
    ***************Reading parquet took 0.630539 second***************
    ***************SQL(only column) took 0.386598 second***************
    ***************Writing output took 0.065699 second***************
    …

This creates a parquet directory myparquet_short.parquet inside HDFS, so if you are running this code multiple times, please remove myparquet_short.parquet before rerunning each time. `$ hadoop fs -rm -R -f myparquet_short.parquet`

Generate_model.py directly queries this parquet to obtain electronic coupling strengths, then computes and saves the TBH. Once you have created myparquet_short.parquet, please run:

    $ time spark-submit --num-executors 2 --executor-cores 1 generate_model.py
    …
     [[  1.00549900e+00  -9.93000000e-04  -2.38700000e-03 ...,   0.00000000e+00
    0.00000000e+00   0.00000000e+00]
     ..., 
    [  0.00000000e+00   0.00000000e+00   0.00000000e+00 ...,   0.00000000e+00
    0.00000000e+00   0.00000000e+00]]

    real	2m32.403s
    user	2m56.752s
    sys	0m4.528s

If you are reproducing the results with 200 files, it could be faster to upload the zip file new_proc_wan_200_files.zip, unzip, upload to the HDFS, and move all the files outside of the folder. Please remove the original empty folder after doing so.

    $ hadoop fs -put new_proc_wan_200_files
    $ hadoop fs -mv new_proc_wan_200_files/new* .
    $ hadoop fs -rm -R -f new_proc_wan_200_files




### Instructions for VASP+Wannier90

To generate the data set, one needs the following code installed in the computing resource:

Density Functional Theory (DFT) code: Vienna Ab initio Simulation Package (VASP) : https://www.vasp.at/
Wannier functions and transformations from DFT: Wannier90 at http://www.wannier.org/

To install these codes , the instructions can be found from the corresponding webpage, introduction files in the code package. We will not repeat the details here. In many supercomputing centers some codes are also compiled already and packaged into a module to be used. Users can replace the corresponding name/path to the executable to run the script.

The example setup folder to execute the computation is in the GitHub. First, the setups for running VASP DFT code can be seen in KSCAN subfolder. Within this folder:

SCF folder is the first stage of the calculation for VASP DFT which completes the self-consistent calculations for the electron charge and other physical quantities. The charge information can then be passed to the next stage of the calculations.
BANDS folder runs the non self-consistent calculations to derive the band structure corresponding to the crystal structure. This is to be used to validate the quality of Wannier interpolation for the band structure in the next stage.
WAN folder is the final stage to derive the Bloch wave functions and perform the Wannier transformation to obtain the localized Wannier basis function as atomic orbitals. The VASP code is executed first to derive the necessary projections for obtaining Wannier orbitals and then Wannier90 code continues with these projections to derive the localized orbitals and the tight-binding model.

Brief descriptions for the input files:
INCAR: which contains the input parameters for running the VASP DFT code such as the energy cutoff, flags to steer the calculations
KPOINTS: the mesh grid or sampling of k points in the reciprocal space
POTCAR: the pseudo potential files for each atomic species to be used in DFT simulations.
POSCAR: contains the descriptions for the crystal structure including the primitive vectors for the real space and the basis positions for the constituent atoms.
wannier90.win: setup file for executing Wannier90 code to derive Wannier orbitals and the modeling for the band structure. For example, this file specifies the energy window to derive the model, what types of atoms / orbitals should be included, etc.

As we see in the introduction, we are going to sample various configurations for the crystal structure. To prepare the files appropriate (POSCAR and wannier90.win files) for each calculation, the script gen_pos.py performs the task and generates 400 different configurations for the stacked TaS2 bilayer crystal. All the files generated will be stored in the allpos subfolder.

For the vasp_wan.py script, this prepares the environment to start the VASP+Wannier90 simulations. This script is designed to simulate the TaS2 crystal in our studies with the corresponding parameters. However, this can be easily tuned to the desired crystal type and different symmetry types. This script repeatedly execute 400 configurations for the varied TaS2 crystal. The results of the simulation of Wannier modeling will be stored in the data subfolder.

The main workhorse to generate the data is the VASP code which is a commercial DFT code. We are not changing the code for the purpose of the class project, however we would like to gauge the performance of this DFT code in terms of the number of CPU used to execute the code. However, we note that this is a very complicated code and depending on the number of CPUs used to execute the code, the default parameters in performing the simulation would adjust themselves as well. For example, the number of bands in the electronic structure will be changed to be the multiples of the number of the CPUs. This means, it will not be completely fair to compare the performance depending on the number of CPUs. However, we can still roughly see how the performance scale at the size of our crystal structure and simulation scale here. We find about 6-8 CPUs are suitable for running the simulation.



### Postprocessing for Wannier90 data

One very interesting aspect of our project is, we have to prepare our own data set to start with by running VASP+Wannier90 rather than working with existing data available on the internet/database. This gives us the chance to think about how we can clean up and manage, distill the necessary information from simulation results. We among the group members discuss over the appropriate data structure to be presented and processed before feeding into the follow-up database stage/process. 

After the discussion, we design the post process script that wraps the detailed physics background into the concise postprocessed files. These files from the wrapper contains only the essential information for the orbital coupling. These can be represented by each data entry which contains the following information for the coupling and features:

For the initial atom site, what is the atomic type, orbital type, orbital index
For the final atom site, what is the atomic type, orbital type, orbital index
The geometry, what is the displacement vector (relative position) between these two orbitals (the hopping direction/vector)
The strength for the coupling, the real part and the imaginary part of the hamiltonian.
Neighboring environment: the primitive vectors for the crystal (a1 and a2) which encodes the compressions and strain information of the parent crystal.
Further generalizations are also possible to capture other ways to vary the crystal confutation. In other words, other features to identify and specify the configuration and later would be used for potentially machine learning algorithm. This can be done by simply adding processing modules to the postprocess script and derive the necessary information to be retained. They can be added as additional data column.
Additional filters can be added to the wrapper to remove the unnecessary information. Though this is not implemented in our code here. For example, to reduce the size of the data set, we can remove the atomic coupling that has a very large hopping distance (we can set a cutoff radius). The physical idea is that, the larger the hopping range is, the smaller the coupling will be and hence can be ignored from the recording the essential atomic coupling information in the database.

The Postprocessing script reads the information from the corresponding POSCAR (crystal structure) and hamiltonian modeling file (*_hr.dat) and the implementation can be found in rec_proc.py. This will go through the all 400 sets of files from the output to process them into more intuitive files (new_proc_wan_*) which contains the atomic couplings. This script can be parallelized by multiprocessing module provided in the standard Python interpreter. As in the plot, we observe the improved performance when we parallelize the data processing. The benchmark is done with a subset (100 sets) of the full data (400 sets) we have. The machine we have has 12 physical cores and we investigate the performance up to 12 cores using pool function in multiprocessing toolkit. As the note, we also test the performance for data stored on the solid state drive and the conventional magnetic hard disk. The solid state drive provides slightly better performance over the conventional magnetic storage device.

## [Profiling](https://stevetorr.github.io/wannier_shift/profiling)


### Serial Loading with Standard Python code

The following is the result of executing serial_query_profile.py on AWS. It collected the displacements and electronic coupling (to be collectively called "coupling") between two orbital "11"'s (atom_from_index=11, atom_to_index=11), from 40 files and 200 files. 

<img src="../figures/Non-spark.png" width="450">

The mere serial query (shown with blue bars) took 13 s to query 40 files, and the execution time was directly proportional to the number of files. It takes approximately 130 s to collect the coupling for a single pair of orbitals query from 400 files so this shows that we needed a more efficient way as we are querying a few hundred times. The query using a worker Pool with 12 workers decreased the execution time to 1/6 - 1/7. However, it still takes 8.8 s for 200 files, which will become 15 min if we were to query 100 times.

### Loading using Spark Cluster with m4.2xlarge Instances

#### Dataframe Filtering and Spark.sql

A Spark version of the query code that is included in spark_query.py was run on a Spark cluster with one Master and two Worker m4.2xlarge instances. m4.2xlarge was chosen as it has 8 vCPUs and using two of it allowed us to test our codes with 12 cores, which is what the workstation has. This code first creates a dataframe and uses dataframe.filter() to collect the couplings, and also creates a temporary view and runs spark.sql on it. The query above (collecting information for orbital 11 - orbital 11 coupling) for 40 files was also tested here. The next figure shows the execution time and speedup as a function of the number of cores. 

<img src="../figures/m4.2xlarge.png" width="800">

With 12 cores, the execution time of 4 s for dataframe.filter() and that of 3 s for spark.sql were obtained. However, the execution time increased slightly for larger number of cores, most likely because the actual number of cores in the instance is smaller due to hyperthreading. For this reason we decided to use m4.4xlarge instances. 

### Loading using Spark Cluster with m4.4xlarge Instances

#### Dataframe Filtering and Spark.sql
The same experiment was done with m4.4xlarge instances, which have 16 vCPUs each, and the following is the results. 

<img src="../figures/m4.4xlarge1.png" width="800">

The execution time decreased as expected, and the query took 3.35 s with dataframe.filter() and 2.04 s with spark.sql. However, this was not much faster than the multiprocessing result.

#### Parquet + Spark.sql

In order to improve the execution time, we turned to the [parquet format](https://spark.apache.org/docs/latest/sql-programming-guide.html#parquet-files). A single script first created a parquet file with data partitioned according to orbital indices (atom_from_index and tom_to_index), read and registered the partitioned table as a temporary view, and ran spark.sqp on it. The following is the execution time of each operation, for again, 11-11 coupling. 

<img src="../figures/m4.4xlarge2.png">
<img src="../figures/m4.4xlarge_table.png">

With 12 cores, parquet creation took 15.6 s, reading it took 0.528 s, and running spark.sql took 0.431 s. The parquet file needs to be generated only once for any number of queries done on the parquet. Therefore the average query time using 16 cores was calculated for different number of queries and the result is shown below. 

<img src="../figures/Superior_parquet.png" width="500">

If query was to be done 10 times, the parquet method will be as fast as running spark.sql directly on the dataframe. Because we will conduct a few hundred queries in the actual implementation, the parquet method is the way to go. For 100 queries, the average time per query is 0.537 s and 0.417 s for 1000 queries. 

#### Experiment with 200 files

Now we executed the code with 200 files and the execution time and speedup are shown below. 

<img src="../figures/Files_comparison.png" width="600">
<img src="../figures/40vs200.png" width="800">

<img src="../figures/40vs200_2.png" width="400">

#### Query + TBH Model Building

Having developed the query code, we combined it with the interpolation code that builds the TBH models, in generate_model.py. This code first creates a parquet, reads the parquet and creates a temporary view, and queries it about 300 times to populate the TBH matrix. The execution time and speedup were compared for different number of cores using 40 files. We also tested how partitioning when creating the parquet affects the total time. 

<img src="../figures/Partition_comparison.png">

With a parquet that contained the data partitioned by atom_from_index and atom_to_index, which are the keys when querying, the execution time was as low as 150 s (figure on the right). While the execution time decreases with increasing number of cores for the parquet without partitioning, the execution time does not change for the fully partitioned data. In order to further improve our code, parallelization of the interpolation part will be necessary, and this is will be our next task. 

#### Tuning

One of the most important performance tuning aspects for Spark SQL is caching data in memory. This could be achieved by using spark.cacheTable() or dataframe.cache(). The whole dataframe, containing all the data from 400 files, is obviously too big to cache. What we could cache is the output from SQL, and this would help with following interpolation. But from Spark documentation, Spark SQL caches Parquet metadata automatically for better performance. This could be indirectly proved by running the same query multiple times. As shown in the figure below, we ran the same query (from orbital 11 to orbital 11) on 400 data files with 12 cores on the workstation multiple times, continuously. Running the query for the first time took about 1.5s, but later on it went down. Because we are querying the exact same data multiple times and it is cached in memory, the queries seem to get faster. 

<img src="../figures/Tuning2.png" width="500">

There are also some other configurations that we can play with, including split computation, broadcast join threshold, shuffle partitions. We tested our code with these configurations using 16 cores and 200 files, but it does not benefit much from the tuning. The detailed results are shown as below. 

<img src="../figures/Tuning.png" width="800">

It seems that partitioning is benefiting a little from increase of shuffle partitions, but we did not see big changes for all the others. Partitioning here refers to transformation of data structure from dataframe to partitioning table. We did run partitionBy in this part and this could possibly explain the improvement brought by changing shuffle partitions. But for the others, since in our case there is no heavy computation or multiple join/aggregation operations duing the query, most of the configuration settings are not expected to make a big difference on the performance. 



## [Results and Discussion](https://stevetorr.github.io/wannier_shift/results)

## [Appendix: Code Descriptions](https://stevetorr.github.io/wannier_shift/code_desc)

Link to files and codes (for instructors)
https://drive.google.com/drive/folders/1TPO2H14AS_1CgilDmRqsAZzv_I4oeqrX?usp=sharing

## [Bibliography](https://stevetorr.github.io/wannier_shift/biblio)



## Results

### The Tight-Binding Hamiltonian

A visualization of the tight-binding Hamiltonian can be provided for a s

## Discussion and Outlook

### Validation tests for the TBH

### Future Directions/Expansions: physics/simulation part of the story
The two-dimensional layer heterostructure stack hold promising applications in the electronics and fundamental physics research. To facilitate and implement the fast screening and simulation of the electronic properties for the stacks, the database tools developed here paves the groundwork for the future studies. With the infrastructure built for the material database, the data generation for various layer types can be automated. The generalization includes variations of the crystal geometry and configuration used for the simulation such as the deformations of the layer geometry from the strain perturbations, the height variations from the compressed pressure applied, various constituent atoms in the layers, etc. Massive atomic coupling information can be extracted from these simulations and the database is suitable to be used to manage the data set and to bridge other applications. For example, one might envision the machine learning algorithm developed to extract and model the feature for the atomic coupling and the dependence on the local environment. This would allow the prediction and modeling of the atomic coupling give a local configuration that appear in the stacked layers (locally). The database itself is also very useful to be used to visualize the atomic coupling depending on each orbital type, or used to derive simpler effective low-energy models for theoretical physics research. The simulation would then guide the fabrication of the devices and make the prediction of their physical properties. On the other hand, because of the layer geometry, the layer materials can also be probed by various experimental methods such as scanning tunneling microscope or optical measurements. These probing techniques directly access the electronic properties and can be used to validate the predications we have for the layer stacks. This would give the feedback for the theoretical modeling and further improve the quality for the simulation method. Our method is designed to retain the information from first principle calculations (DFT) and can be improved systematically without any unjustified ad hoc ansatz or assumptions for the atomic coupling. A database that manage the set of atomic coupling data is highly relevant for the field of studies on these two-dimensional layered materials and their simulations. 

### Workstation details:


Mac Pro Mid 2010 model

OS: macOS High Sierra (version 10.13.4)

CPU: 2 x 6-core 2.66 GHz Intel Xeon (256KB of L2 cache per core and 12 MB L3 cache per processor, 6.4 GT/s interconnect speed)

System Hard disk: Solid State Drive (512GB)

Data Strange Hard Disk: WD 4TB hard drives (conventional magnetic drives)

Memory: 64 GB 1333 MHz DDR3 ECC SDRAM

Fixed IP address on campus: 10.243.34.140

Graphics: 2 x AMD ATI Radeon HD 5770 (1024MB VRAM)

**FIGURE: THE STATION**

## Bibliography

\[1\] Fang 2015, PRB, [link](http://www.google.com/url?q=http%3A%2F%2Fjournals.aps.org%2Fprb%2Fabstract%2F10.1103%2FPhysRevB.92.205108&sa=D&sntz=1&usg=AFQjCNEPWOnbGlS1q9C2e6Y8fl36wxQzaA) [Arxiv](https://arxiv.org/abs/1506.08860)

\[2\] Vienna Ab Initio Simulation Package, https://www.vasp.at/

\[3\] "An updated version of wannier90: A tool for obtaining maximally-localised Wannier functions", [link](https://www.sciencedirect.com/science/article/pii/S001046551400157X?via%3Dihub)




















Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).
