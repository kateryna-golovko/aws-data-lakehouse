CREATE EXTERNAL TABLE IF NOT EXISTS `kgolovko-db`.`customers_curated` (
  `serialNumber` string,
  `birthDay` string,
  `shareWithPublicAsOfDate` bigint,
  `registrationDate` bigint,
  `customerName` string,
  `shareWithFriendsAsOfDate` bigint,
  `email` string,
  `lastUpdateDate` bigint,
  `shareWithResearchAsOfDate` bigint,
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
LOCATION 's3://kgolovko-lake-house/customer/curated/'
TBLPROPERTIES ('classification' = 'json');