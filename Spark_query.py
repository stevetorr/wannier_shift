from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark import SparkConf, SparkContext
import threading
import sys
import numpy as np
import time

# To test speed up
try:
    argv = sys.argv[1]
    argv1 = int(argv)
except:
    argv1 = 12

# To run on a local mode
conf = SparkConf().setMaster('local[%i]'%argv1)

# Uncomment to run on a cluster
#conf = SparkConf()

sc = SparkContext(conf = conf)
sc.setLogLevel("WARN")
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

# Set how many files needed to be read
files=[]
prefix='new_proc_wan_'
for i in range(40):
    files.append(prefix+str(i))

# Read files into dataframe
tstart = time.time()
df = spark.read.format("csv").option("header", "true").load(files)
tend = time.time()
print('***************Reading files took %f second***************'%(tend - tstart))

# Run filter directly on the dataframe
tstart = time.time()
df2 = df.filter((df.atom_from_index == '11') & (df.atom_to_index == '11'))
df2_np = np.array(df2.select('hop_vec_x','hop_vec_y','hop_vec_z','ham_real').collect())
df2_npf = df2_np.astype(np.float)
tend = time.time()
print('***************Dataframe filter took %f second***************'%(tend - tstart))

# Run SQL directly on the dataframe
df.registerTempTable("Test")
sqlContext = SQLContext(sc)
tstart = time.time()
aa = sqlContext.sql("SELECT * FROM Test WHERE atom_from_orbital = '11' AND atom_to_orbital = '11'" ).collect()
aa_np = np.array(aa)
aa_npf = aa_np.astype(np.float)
tend = time.time()
print('***************Dataframe SQl took %f second***************'%(tend - tstart))

# Partition dataframe and save as parquet
tstart = time.time()
df.write.partitionBy('atom_from_index').format("parquet").save("myparquet_tuning.parquet")
tend = time.time()
print('***************Partitioning took %f second***************'%(tend - tstart))

# Read in the partitioned table
tstart = time.time()
spark.read.format("parquet").load("myparquet_tuning.parquet").createOrReplaceTempView("fun")
tend = time.time()
print('***************Reading parquet took %f second***************'%(tend - tstart))

# spark.catalog.cacheTable("fun"), this could be used to test cache for the whole table, but it will take even longer
# The commented code below could be used to test auto-cache of partitioned table in spark
'''
tstart = time.time()
aa = spark.sql("select hop_vec_x,hop_vec_y,hop_vec_z,ham_real from fun where atom_from_index = '11' AND atom_to_index = '11'").collect()
tend = time.time()
print('***************SQL1 took %f second***************'%(tend - tstart))

tstart = time.time()
aa = spark.sql("select hop_vec_x,hop_vec_y,hop_vec_z,ham_real from fun where atom_from_index = '11' AND atom_to_index = '11'").collect()
tend = time.time()
print('***************SQL2 took %f second***************'%(tend - tstart))

tstart = time.time()
aa = spark.sql("select hop_vec_x,hop_vec_y,hop_vec_z,ham_real from fun where atom_from_index = '11' AND atom_to_index = '11'").collect()
tend = time.time()
print('***************SQL3 took %f second***************'%(tend - tstart))
'''

# SQL query
tstart = time.time()
aa = spark.sql("select hop_vec_x,hop_vec_y,hop_vec_z,ham_real from fun where atom_from_index = '11' AND atom_to_index = '11'").collect()
aa_np = np.array(aa)
aa_npf = aa_np.astype(np.float)
tend = time.time()
print('***************SQL(only column) took %f second***************'%(tend - tstart))

# The commented code below could be used to test reading all the columns in SQL command
'''
tstart = time.time()
aaa = spark.sql("select * from fun where atom_from_index = '11' AND atom_to_index = '11'")
aaa_np = np.array(aaa.select('hop_vec_x','hop_vec_y','hop_vec_z','ham_real').collect())
aaa_npf = aaa_np.astype(np.float)
tend = time.time()
print('***************SQL(all columns) took %f second***************'%(tend - tstart))
'''

# Write the result into txt
# Not required in the combined code
tstart = time.time()
np.savetxt('test321.txt', aa_npf, delimiter=',')
tend = time.time()
print('***************Writing output took %f second***************'%(tend - tstart))

# Test threading
def query(name, k,l):
    tstart = time.time()
    aa = spark.sql("select hop_vec_x,hop_vec_y,hop_vec_z,ham_real from fun where atom_from_index = '%s' AND atom_to_index = '%s'" %(k,l)).collect()
    aa_np = np.array(aa)
    aa_npf = aa_np.astype(np.float)
    print(aa_npf[0])
    tend = time.time()
    print('SQL',name,'took %f seconds'%(tend-tstart))

tstart1 = time.time()
threads = []
for i in range(10):
    t = threading.Thread(target=query, args=(i,(i+1),1)) #task is the query function, i is the input parameter
    threads.append(t)

for x in threads:
    x.start()
    print 'spark task', i, 'has started'

for x in threads:
    x.join()

tend1 = time.time()
print('With threading, 10 queries took %f seconds'%(tend1 - tstart1))

tstart2 = time.time()
for i in range(10):
    query(i, (i+1), 1)

tend2 = time.time()
print('Without threading, 10 queries took %f seconds'%(tend2 - tstart2))
