from pyspark.sql import SparkSession, DataFrame
import sys

# Função principal do job
def main(spark : DataFrame, input_path : str, output_path : str):
    
    # Ler o dado da Bronze
    df = spark.read.format("delta").load(input_path)
    
    # Criar view
    df_view = df.distinct().groupBy("brewery_type", "city").count()

    # Escrever no Formato CSV
    df_view.write.mode('overwrite').format("csv").save(output_path)

if __name__ == "__main__":
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Inicializar a SparkSession com Delta Lake
    spark = SparkSession.builder \
            .appName("spark_gold") \
            .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .getOrCreate()
    
    main(spark=spark, 
         input_path=input_path, 
         output_path=output_path)
