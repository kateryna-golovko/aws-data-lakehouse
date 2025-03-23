# AWS Data Lakehouse Project - Spark and Human Balance

The third project in the "Data Engineering with AWS" course provided by Udemy.

The background of the task is STEDI is working on development of a hardware STEDI Step Trainer.

The aim is to extract the data produced by the STEDI Step Trainer sensors and the mobile app, and curate them into a data lakehouse solution on AWS. 

Privacy is an essential consideration when it comes to customer data. Some of the customers have given permission for their data to be used for training the model purposes. Hence, the data used will be limited to the customers` data that gave their permission. This will be done by ensuring 


For these project, the following environments are required:
- Python and Spark
- AWS Glue
- AWS Athena
- AWS S3

As part of the project, creating Python scripts using AWS Glue and Glue Studio.Python editor can be used to locally run the code, but to test or run the Glue Jobs, they weill need to be submitted to an AWS Glue environment.

Project data:
The project consists of 3 datasets:
- *customer*
- *step_trainer*
- *accelerometer*

Using AWS Glue, AWS S3, Python, and Spark, create or generate Python scripts to build a lakehouse solution in AWS. The image below shows the requirements:
![image](https://github.com/user-attachments/assets/273f32f1-3a47-48ad-9056-3cfe63ad3719)

Steps:
1.
2.
...

Relational diagram is given below:
![image](https://github.com/user-attachments/assets/32921352-9175-489d-957a-15563e1d9cfb)


 *aws ec2 describe-vpcs --query "Vpcs[*].VpcId* - to get VPC id if it is not shown in JSON
