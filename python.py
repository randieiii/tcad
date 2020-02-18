from pyspark.sql.functions import *
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
sc = SparkContext('local')
spark = SparkSession(sc)

textFile = spark.read.text("ollo.txt")
wordCounts = textFile.select(explode(split(textFile.value, "\s+")).alias("word")).groupBy("word").count()
ll = wordCounts.orderBy('count', ascending=False).collect()
for i in ll[:100]:
    print(i)