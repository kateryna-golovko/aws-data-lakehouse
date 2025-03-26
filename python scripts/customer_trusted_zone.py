import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
import re

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
AmazonS3_node1742697098644 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://kgolovko-lake-house/customer_landing/"], "recurse": True}, transformation_ctx="AmazonS3_node1742697098644")

# Script generated for node PrivacyFilter
PrivacyFilter_node1742729757213 = Filter.apply(frame=AmazonS3_node1742697098644, f=lambda row: (not(row["shareWithResearchAsOfDate"] == 0)), transformation_ctx="PrivacyFilter_node1742729757213")

# Script generated for node Trusted Customer Zone
EvaluateDataQuality().process_rows(frame=PrivacyFilter_node1742729757213, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1742696902238", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
TrustedCustomerZone_node1742697151222 = glueContext.getSink(path="s3://kgolovko-lake-house/customer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="TrustedCustomerZone_node1742697151222")
TrustedCustomerZone_node1742697151222.setCatalogInfo(catalogDatabase="kgolovko-db",catalogTableName="customer_trusted")
TrustedCustomerZone_node1742697151222.setFormat("json")
TrustedCustomerZone_node1742697151222.writeFrame(PrivacyFilter_node1742729757213)
job.commit()