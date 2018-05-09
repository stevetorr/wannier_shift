
# Profiling the Problem

**On this page, we detail our thought process in understanding the necessary computational tasks and deciding the best course of action to pursue.**

In order to better understand where advantages of parallelization could come in to this project, we first draw attention to the salient features of the problem. 

### Data Generation - Big Compute

The batched data generation involves calling several hundred to several thousand different calculations of the VASP imeplementation of Density Functional Theory. All of the calculations' input parameters are deterministically generated and may proceed in any order; further, VASP is commercial software which is optimized already for parallel implementation on the per-calculation basis, exploiting multiple cores to more rapidly solve for the electronic density function and associated energy. **Therefore, the process of generating our data sets is ripe for embarassingly parallel MPI implementation.**

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

