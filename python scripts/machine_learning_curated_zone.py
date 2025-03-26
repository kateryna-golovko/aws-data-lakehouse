import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Accelerometer trusted 
Accelerometertrusted_node1742855498968 = glueContext.create_dynamic_frame.from_catalog(database="kgolovko-db", table_name="accelerometer_trusted", transformation_ctx="Accelerometertrusted_node1742855498968")

# Script generated for node Step trainer trusted
Steptrainertrusted_node1742855552147 = glueContext.create_dynamic_frame.from_catalog(database="kgolovko-db", table_name="step_trainer_trusted", transformation_ctx="Steptrainertrusted_node1742855552147")

# Script generated for node Change Schema
ChangeSchema_node1742861162602 = ApplyMapping.apply(frame=Accelerometertrusted_node1742855498968, mappings=[("user", "string", "user", "string"), ("timestamp", "long", "timestamp", "long"), ("x", "float", "x", "float"), ("y", "float", "y", "float"), ("z", "float", "z", "float")], transformation_ctx="ChangeSchema_node1742861162602")

# Script generated for node Change Schema
ChangeSchema_node1742861213267 = ApplyMapping.apply(frame=Steptrainertrusted_node1742855552147, mappings=[("sensorreadingtime", "long", "sensorreadingtime", "long"), ("serialnumber", "string", "serialnumber", "string"), ("distancefromobject", "int", "distancefromobject", "int")], transformation_ctx="ChangeSchema_node1742861213267")

# Script generated for node Inner join
Innerjoin_node1742855627373 = Join.apply(frame1=ChangeSchema_node1742861213267, frame2=ChangeSchema_node1742861162602, keys1=["sensorreadingtime"], keys2=["timestamp"], transformation_ctx="Innerjoin_node1742855627373")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=Innerjoin_node1742855627373, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1742854347357", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1742855738885 = glueContext.getSink(path="s3://kgolovko-lake-house/machine_learning/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1742855738885")
AmazonS3_node1742855738885.setCatalogInfo(catalogDatabase="kgolovko-db",catalogTableName="machine_learning_curated")
AmazonS3_node1742855738885.setFormat("json")
AmazonS3_node1742855738885.writeFrame(Innerjoin_node1742855627373)
job.commit()