from pyspark.sql import SparkSession, DataFrame
from delta.tables import DeltaTable
import sys
from delta import DeltaUtils

# Função principal do job
def main(spark : DataFrame, input_path : str, output_path : str, partition_col : str):
    
    # Ler o dado da Bronze
    df = spark.read.json(input_path)
    
    # Escrever o DataFrame como uma Delta Table
    delta = DeltaUtils(spark=spark, delta_path=output_path)

    # Formato de inserção append
    delta.append(output_path=output_path, partition_col=partition_col)

    # Optimize delta table
    delta.optimize()

    # Limpeza de antigas versões de dados
    delta.vaccum(retention_hours=168)

if __name__ == "__main__":
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    partition_col = sys.argv[3]

    # Inicializar a SparkSession com Delta Lake
    spark = SparkSession.builder \
                        .appName("spark_silver") \
                        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0") \
                        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
                        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
                        .getOrCreate()
    
    main(spark=spark, 
         input_path=input_path, 
         output_path=output_path,
         partition_col=partition_col)
