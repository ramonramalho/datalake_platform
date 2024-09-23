from delta.tables import DeltaTable

class DeltaUtils : 
    def __init__(self, spark : SparkSession, delta_path : str):
        self.spark = spark
        self.delta_path = delta_path
    
    def get_delta_table(self, spark : SparkSession, delta_path : str):
        return DeltaTable.forPath(spark, delta_path) 
    
    def optimize(self):
        delta_table = self.get_delta_table(spark=self.spark, delta_path=self.delta_path)
        delta_table.optimize().executeCompaction()
    
    def vaccum(self, retention_hours : int = 0):
        delta_table = self.get_delta_table(spark=self.spark, delta_path=self.delta_path)
        delta_table.vacuum(retention_hours)
    
    def merge(self, merge_df : DataFrame, key_col : str):
        # Realizar o merge
        delta_table = self.get_delta_table(spark=self.spark, delta_path=self.delta_path)
        delta_table.alias("target").merge(
            merge_df.alias("source"),  # DataFrame de origem (novos dados)
            f"target.{key_col} = source.{key_col}"  # Condição de correspondência
        )\
        .whenMatchedUpdate(set={"age": "source.age"})\
        .whenNotMatchedInsert(values={"name": "source.name", "age": "source.age"})\
        .execute()
    
    def overwrite(self, output_path : str, partition_col : str ):
        self.spark.write.mode("overwrite").partitionBy(partition_col).format("delta").save(output_path)

    def append(self, output_path : str, partition_col : str ):
        self.spark.write.mode("append").partitionBy(partition_col).format("delta").save(output_path)