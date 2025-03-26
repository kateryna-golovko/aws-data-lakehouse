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

# Script generated for node Amazon S3
AmazonS3_node1742775435762 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://kgolovko-lake-house/accelerometer_landing/"], "recurse": True}, transformation_ctx="AmazonS3_node1742775435762")

# Script generated for node S3 bucket
S3bucket_node1742775322996 = glueContext.create_dynamic_frame.from_catalog(database="kgolovko-db", table_name="customer_trusted", transformation_ctx="S3bucket_node1742775322996")

# Script generated for node Customer Privacy Filter
CustomerPrivacyFilter_node1742775606194 = Join.apply(frame1=S3bucket_node1742775322996, frame2=AmazonS3_node1742775435762, keys1=["email"], keys2=["user"], transformation_ctx="CustomerPrivacyFilter_node1742775606194")

# Script generated for node Drop Fields
DropFields_node1742775966451 = DropFields.apply(frame=CustomerPrivacyFilter_node1742775606194, paths=["email", "phone"], transformation_ctx="DropFields_node1742775966451")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=DropFields_node1742775966451, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1742774161136", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1742775872050 = glueContext.getSink(path="s3://kgolovko-lake-house/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1742775872050")
AmazonS3_node1742775872050.setCatalogInfo(catalogDatabase="kgolovko-db",catalogTableName="accelerometer_trusted")
AmazonS3_node1742775872050.setFormat("json")
AmazonS3_node1742775872050.writeFrame(DropFields_node1742775966451)
job.commit()