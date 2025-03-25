import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs

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

# Script generated for node Customers Trusted
CustomersTrusted_node1742789676392 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://kgolovko-lake-house/customer/trusted/"], "recurse": True}, transformation_ctx="CustomersTrusted_node1742789676392")

# Script generated for node Accelerometer Trusted 
AccelerometerTrusted_node1742789677761 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://kgolovko-lake-house/accelerometer/trusted/"], "recurse": True}, transformation_ctx="AccelerometerTrusted_node1742789677761")

# Script generated for node Security Filter
SecurityFilter_node1742789683300 = Join.apply(frame1=CustomersTrusted_node1742789676392, frame2=AccelerometerTrusted_node1742789677761, keys1=["email"], keys2=["user"], transformation_ctx="SecurityFilter_node1742789683300")

# Script generated for node Drop Fields
DropFields_node1742789691674 = DropFields.apply(frame=SecurityFilter_node1742789683300, paths=["user", "z", "y", "x", "timestamp"], transformation_ctx="DropFields_node1742789691674")

# Script generated for node Drop Duplicates
DropDuplicates_node1742791193398 =  DynamicFrame.fromDF(DropFields_node1742789691674.toDF().dropDuplicates(), glueContext, "DropDuplicates_node1742791193398")

# Script generated for node Customers curated
EvaluateDataQuality().process_rows(frame=DropDuplicates_node1742791193398, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1742776887734", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Customerscurated_node1742789698636 = glueContext.write_dynamic_frame.from_options(frame=DropDuplicates_node1742791193398, connection_type="s3", format="json", connection_options={"path": "s3://kgolovko-lake-house/customer/curated/", "partitionKeys": []}, transformation_ctx="Customerscurated_node1742789698636")

job.commit()