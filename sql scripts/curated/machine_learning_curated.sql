CREATE EXTERNAL TABLE IF NOT EXISTS `kgolovko-db`.`machine_learning_curated` (
  `serialnumber` string,
  `z` double,
  `birthday` string,
  `sharewithpublicasofdate` bigint,
  `sharewithresearchasofdate` bigint,
  `registrationdate` bigint,
  `customername` string,
  `user` string,
  `y` double,
  `sharewithfriendsasofdate` bigint,
  `x` double,
  `timestamp` bigint,
  `lastupdatedate` bigint,
  `sensorreadingtime` bigint,
  `email` string,
  `distancefromobject` int,
  `phone` string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'ignore.malformed.json' = 'FALSE',
  'dots.in.keys' = 'FALSE',
  'case.insensitive' = 'TRUE',
  'mapping' = 'TRUE'
)
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://kgolovko-lake-house/machine_learning/curated/'
TBLPROPERTIES ('classification' = 'json');