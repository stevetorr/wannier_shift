# Wannier Shift
## A project by Shiang Fang, Eri Muramoto, Steven Torrisi, and Tianning Zhao

## Introduction, Background, and Motivation

Density functional theory (DFT) is the workhorse of computational condensed matter and physical chemistry. It allows users to compute a wide variety of material properties, such as electronic and mechanical structure, phonon/vibrational behavior, and geometric phase phenomena. However, DFT does not scale favorably with system size, and performing complicated electron orbital-structure or mechanical relaxation calculations for systems with more than a few dozen atoms becomes intractable. 



DFT typically generates wavefunctions that are in the plane-wave basis, so the periodicity across a crystal is easy to exploit. However, the use of an alternate wavefunction basis, Maximally Localized Wannier Functions (MLWF), allow us to visualize the electrons as being localized on individual atoms as well as determine the physical interaction strength, or coupling, between different orbitals. It can be advantageous to study a system from the basis of individual orbitals coupling to one another, as such a mathematical framework turns most calculations of system properties into routine linear algebra calculations.



Therefore, MLWF’s are useful to bring the toolset of DFT to bear on large systems. For instance, one of our group members demonstrated how parameterizing a tight binding model for Transition Metal Dichalcogenides could come from MLWF’s and DFT. \[[Fang 2015](https://jekyllrb.com/)\]; learning how to model two-dimensional twisted systems is a vigorous and active field of research, spurned on by the recent discovery that twisted bilayer graphene superconductors.



In order to study twisted bilayer TMDC systems, we need to understand the interactions between atoms in a wide variety of spatial configurations; even for modest twist angles, the periodicity which is necessary for DFT calculations is only by very large systems of hundreds of atoms. Therefore, a tight-binding model informed by Wannier functions is one of the precious few techniques we have to approach calculating properties of twisted 2D systems.





### Our Plan

Our chief concerns are as follows. It is very time-costly to generate data sets for different bilayer material configurations. The DFT + Wannierization software is already optimized for parallel execution over cores, and is best regarded as a black box; therefore, embarrassingly parallel execution of the code via a wrapper code for a wide variety of configurations is how we aim to optimize this step. For the management and utilization of the resulting dataset, we turn to Spark and examine other database models to rapidly query the database for different orbital-orbital coupling strengths. The advantage of this parallelization is that it allows for faster querying of the computed values for accurate tight-binding Hamiltonian parameterization.



### Our Method

The extremely fine mesh of configurations which we produce via large batches of DFT calculations comprises a big compute phase of this project; we perform calculations of N>>100 configurations, each of which takes on the order of 15 minutes to generate the optimized electron wavefunction and then convert into Wannier functions appropriately. These runs are performed in the commercial Vienna Ab Initio Simulation Package \[[VASP](https://www.vasp.at/)\]. Calculations are run from a set of physical configuration parameters and run configurations, such as the spatial orientation of the unit cell, or a cutoff for how fine the density is resolved. The ‘Wannierization’ is performed by running Wannier90, a software package which converts wavefunctions from the plane-wave formulation to the Wannier function formalism.  



From there, the program outputs a list of the orbital-orbital couplings in the default wannier90 format. It creates one such file for each local configuration, which in our first batch included 400 different unit cells and VASP runs. We wrote and applied a wrapper which converts the data into a csv format for easy load-in to a spark data frame, as well as decorating it with information which assists our post-processing efforts. From there, we wrote a spark program which loads the 400 data files into one data frame for easy querying. As mentioned before, the tight-binding-Hamiltonian is entirely represented by a giant matrix, and we populate it by querying the spark database.



The primary development platform for our calculation was a workstation physically located at Harvard, in the Kaxiras group’s office space of Cruft Hall. The workstation runs OSX High Sierra  **INCLUDE A LOT OF TECHNICAL DETAILS ABOUT THE WORKSTATION, HERE**. 

## Profiling the Problem

In order to better understand where advantages of parallelization could come in to this problem, we first draw attention to the salient features of the problem.

The batched data generation involves calling several hundred to several thousand different calculations of the VASP imeplementation of Density Functional Theory. All of the calculations' input parameters are deterministically generated and may proceed in any order; further, VASP is commercial software which is optimized already for parallel implementation on the per-calculation basis, exploiting multiple cores to more rapidly solve for the electronic density function and associated energy. **Therefore, the process of generating our data sets is ripe for embarassingly parallel MPI implementation.** 

Next, we turn to managing the data. When developing a tight-binding model for a system of atoms, we are attempting to map displacements between atoms (which arise from a twisting angle applied to a bilayer system) to the resultant coupling between their orbitals. In Transition Metal Dichalcogenide systems, we have 11 orbitals in the three-atom unit cell of a monolayer (2 sets of three p-orbitals for the Chalcogens, and five d-orbitals for the Transition Metal). In a twisted sample, we seek to find the orbital interaction between every pair of orbitals in the material. Therefore, we move from the displacements between individual atoms to the coupling strength of the atom's orbitals.

We obtain local information about how the orbital coupling should behave from the Wannierization. We end up with a data set of hundreds of displaced unit cells with associated orbital-orbital energy couplings. Querying this database is not trivial, and represents a query of several million data points to find the relevant values. Even loading the relevant data into usable memory is not a trivial task for the computer. **Therefore, managing this enormous dataset, and querying it efficiently, is ammenable to attack via Spark or other distributed database management frameworks.**. 

From there, we understand that the twisted angle displacemetns will virtually never line up with the local samplings we took-- we have to perform an interpolation. Performing this interpolation may be computationally intensive for large numbers of real-space data points. **Black-box functions exist for Scipy to perform this implementation in a way easily compatible with Spark-- but it could be possible to help perform these queries in parallel.**


To load in the 400 files takes a substantial amount of time in serial. We decided to profile t

The overall data content of all of the files, collectively, is **(GET THIS NUMBER)** which is too


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
