
### Serial Loading with Standard Python code

The following is the result of executing serial_query_profile.py on AWS. It collected the displacements and electronic coupling (to be collectively called "coupling") between two orbital "11"'s, from 40 files and 200 files. The mere serial query (shown with blue bars) took 13 s to query 40 files, and the execution time was directly proportional to the number of files. It takes approximately 130 s to collect the coupling for a single pair of orbitals query from 400 files so this shows that we needed a more efficient way as we are querying a few hundred times. The query using a worker Pool with 12 workers decreased the execution time to 1/6 - 1/7. However, it still takes 8.8 s for 200 files, which will become 15 min if we were to query 100 times.

<img src="../figures/Non-spark.png" width="450">

### Loading using Spark Cluster with m4.2xlarge

spark_query.py was ran on a Spark cluster with one Master and two Worker m4.2xlarge instances. m4.2xlarge was chosen as it has 8 vCPUs and using two of it allowed us to experiment with 12 cores, which is what the workstation has. The query above (collecting information for orbital 11 - orbital 11 coupling) was also tested here. 

<img src="../figures/m4.2xlarge.png" width="800">
