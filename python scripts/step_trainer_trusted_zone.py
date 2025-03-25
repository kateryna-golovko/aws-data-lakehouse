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

# Script generated for node Step trainer landing
Steptrainerlanding_node1742854385745 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://kgolovko-lake-house/step_trainer_landing/"], "recurse": True}, transformation_ctx="Steptrainerlanding_node1742854385745")

# Script generated for node Customer curated
Customercurated_node1742854454403 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://kgolovko-lake-house/customer/curated/"], "recurse": True}, transformation_ctx="Customercurated_node1742854454403")

# Script generated for node Inner join
Innerjoin_node1742854499213 = Join.apply(frame1=Steptrainerlanding_node1742854385745, frame2=Customercurated_node1742854454403, keys1=["serialNumber"], keys2=["serialNumber"], transformation_ctx="Innerjoin_node1742854499213")

# Script generated for node Drop Fields
DropFields_node1742868027374 = DropFields.apply(frame=Innerjoin_node1742854499213, paths=["`.serialNumber`", "`.customerName`", "birthDay", "shareWithPublicAsOfDate", "shareWithResearchAsOfDate", "registrationDate", "customerName", "`.shareWithPublicAsOfDate`", "shareWithFriendsAsOfDate", "`.lastUpdateDate`", "`.birthDay`", "`.shareWithFriendsAsOfDate`", "`.registrationDate`", "email", "lastUpdateDate", "`.shareWithResearchAsOfDate`", "phone"], transformation_ctx="DropFields_node1742868027374")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=DropFields_node1742868027374, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1742854347357", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1742854997526 = glueContext.write_dynamic_frame.from_options(frame=DropFields_node1742868027374, connection_type="s3", format="json", connection_options={"path": "s3://kgolovko-lake-house/step_trainer/trusted/", "partitionKeys": []}, transformation_ctx="AmazonS3_node1742854997526")

job.commit()