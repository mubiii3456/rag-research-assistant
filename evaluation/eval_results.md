# RAG System Evaluation Results

Total questions tested: 15

Average response time: 11.22s

---

## Q1 (easy): What is AWS?

**Expected topic:** AWS Overview

**Chunks retrieved:** 5 | **Time:** 55.33s

**Answer:**

Based on the provided context, **AWS (Amazon Web Services)** is a cloud computing platform offered by Amazon. According to the documents:

- **Page 11:** AWS is "a highly reliable, scalable, low-cost infrastructure platform in the cloud that powers hundreds of thousands of businesses in 190 countries around the world." It eliminates the need for businesses to plan for and procure servers and other IT infrastructure weeks or months in advance — instead, customers can "instantly spin up hundreds or thousands of servers in minutes and deliver results faster."

- **Page 146:** AWS "provides building blocks that you can assemble quickly to support virtually any workload." It offers a complete set of highly available services designed to work together to build sophisticated, scalable applications, including highly durable storage, low-cost compute, high-performance databases, and management tools. These services are available with no up-front cost, and customers pay only for what they use. AWS helps organizations move faster, lower IT costs, and scale, and is trusted by both large enterprises and startups to power a wide variety of workloads such as web and mobile applications, game development, data processing and warehousing, storage, and archive.

In short, AWS is a cloud-based infrastructure and services platform that enables businesses to access computing resources on demand without the burden of managing physical hardware.

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q2 (easy): What is the AWS shared responsibility model?

**Expected topic:** AWS Security

**Chunks retrieved:** 5 | **Time:** 12.41s

**Answer:**

The **AWS shared responsibility model** is a framework that defines the division of security responsibilities between AWS and its customers. Based on the provided context:

- **AWS's responsibilities**: AWS provides a secure global infrastructure and foundation services, including compute, storage, networking, and database services, as well as higher-level services and security features. AWS physically secures the infrastructure that supports its cloud services, and for managed services (such as Amazon RDS and Amazon EMR), AWS also manages the underlying infrastructure, foundation services, the operating system, and the application platform (Page 10). For infrastructure services like Amazon EC2, Amazon EBS, and Amazon VPC, AWS provides the secure global infrastructure on which they run (Page 8).

- **Customer's responsibilities**: AWS customers are responsible for protecting the confidentiality, integrity, and availability of their data in the cloud, as well as for meeting their specific business requirements for information protection (Page 4). This includes securing their operating systems, platforms, and data (Page 5). For example, while AWS provides data backup and recovery tools for services like Amazon RDS, customers are responsible for configuring and using those tools in line with their business continuity and disaster recovery (BC/DR) policy (Page 10).

In summary, the shared responsibility model requires AWS and the customer to work together toward security objectives — AWS secures the underlying infrastructure, while the customer is accountable for what they put in the cloud and how they configure it (Page 5). This model allows customers to focus on achieving their business goals using AWS services, while benefiting from AWS's physical infrastructure security (Page 16).

**Sources**: Pages 4, 5, 8, 10, and 16.

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q3 (easy): What are the pillars of the AWS Well-Architected Framework?

**Expected topic:** AWS Architecture

**Chunks retrieved:** 5 | **Time:** 9.64s

**Answer:**

The five pillars of the AWS Well-Architected Framework are:

1. **Operational Excellence**
2. **Security**
3. **Reliability**
4. **Performance Efficiency**
5. **Cost Optimization**

This information is consistent across multiple pages of the document:
- **Page 4** states: "The AWS Well-Architected Framework is based on five pillars — operational excellence, security, reliability, performance efficiency, and cost optimization."
- **Page 5** provides a detailed table describing each pillar and its purpose.
- **Page 9** reiterates: "operational excellence, security, reliability, performance efficiency, and cost optimization."

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q4 (medium): How does AWS IAM help with access control?

**Expected topic:** AWS Security

**Chunks retrieved:** 5 | **Time:** 11.77s

**Answer:**

Based on the provided context, AWS IAM helps with access control in the following ways:

1. **Securely controls access to AWS services and resources** for AWS users, groups, and roles (Page 132).

2. **Fine-grained access controls with permissions**: Using IAM, you can create and manage fine-grained access controls, specifying who can access which services and resources, and under which conditions (Page 132).

3. **Granular policies**: IAM allows you to apply granular policies that assign permissions to a user, group, role, or resource (Page 16).

4. **Centralized management**: With IAM, you can centrally manage users, security credentials (such as passwords and access keys), and permissions policies that control which AWS services and resources users can access (Page 6).

5. **Individual user creation**: IAM lets you create individual users within your AWS account and give each of them their own user name, password, and access keys. Individual users can then log into the console using a URL that's specific to your account (Page 6).

6. **Role-based identity and access management**: The IAM service provides role-based identity and access management for AWS, enabling centralized access control which is essential for managing risk (Page 45).

7. **Control user and programmatic access**: IAM allows you to control both user and programmatic access to AWS services and resources (Page 16).

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q5 (easy): What is Amazon S3 used for?

**Expected topic:** AWS Overview

**Chunks retrieved:** 5 | **Time:** 5.4s

**Answer:**

According to the provided context, **Amazon S3 (Amazon Simple Storage Service)** is an object storage service that offers industry-leading scalability, data availability, security, and performance. It is used by customers of all sizes and industries to **store and protect any amount of data** for a range of use cases, including:

- Websites
- Mobile applications
- Backup and restore
- Archive
- Enterprise applications
- IoT devices
- Big data analytics

**Source:** Page 142

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q6 (medium): What is the difference between horizontal and vertical scaling in AWS?

**Expected topic:** AWS Architecture

**Chunks retrieved:** 5 | **Time:** 7.07s

**Answer:**

I don't have this information in the provided documents. The context mentions "horizontal scalability" in passing on Page 43 (referring to AWS instances being able to be zoned at the operating systems level), and discusses various AWS scaling services like AWS Auto Scaling (Page 96) and Amazon EC2 Auto Scaling (Page 44), but it does not define or compare horizontal and vertical scaling.

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q7 (medium): What encryption options does AWS provide for data at rest?

**Expected topic:** AWS Security

**Chunks retrieved:** 5 | **Time:** 11.06s

**Answer:**

Based on the provided context, AWS provides the following encryption options for protecting data at rest:

## 1. **Amazon S3** (Pages 20, 24)
- **Server-side encryption (SSE)** – implemented by AWS to make it easier to store data in encrypted form.
- **Client-side encryption** – the AWS-provided Java SDK offers Amazon S3 client-side encryption features.

## 2. **Amazon Glacier** (Page 26)
- **Server-side encryption** – all data stored on Amazon Glacier is protected using server-side encryption.
  - AWS generates separate unique encryption keys for each Amazon Glacier archive.
  - Data is encrypted using **AES-256**.
  - The encryption key itself is encrypted using AES-256 with a master key stored in a secure location.
  - The master key is rotated on a regular basis.
- **Client-side encryption** – you can encrypt data prior to uploading it to Amazon Glacier for additional protection.

## 3. **Amazon DynamoDB** (Page 27)
- **Application-layer encryption** – you can implement a data encryption layer over the standard DynamoDB service.
- Best practice: use **raw binary fields** or **Base64-encoded string fields** when storing encrypted fields.

## 4. **Amazon EMR** (Pages 27–28)
- **Hybrid approach** – a combination of:
  - Amazon S3 server-side encryption
  - Client-side encryption
  - Application-level encryption
- Third-party solutions are also available (e.g., Gazzang).

## 5. **Application-Level Encryption** (Page 26, referencing Oracle)
- Tools like **Oracle Transparent Data Encryption** can be used to encrypt table spaces or specific table columns using industry-standard algorithms such as **AES** and **Triple DES**.

## 6. **Amazon EBS** (Page 24)
- Table 9 summarizes features for protecting Amazon EBS data at rest (specific details are not provided in the context, but the volume is received in raw, unformatted mode where you control partitioning, RAID, file systems, and data protection).

---

**Summary of encryption types AWS supports for data at rest:**
- Server-side encryption (S3, Glacier)
- Client-side encryption (S3, Glacier, EMR)
- Application-level encryption (DynamoDB, EMR, Oracle TDE)
- Hybrid approaches combining the above (EMR)

**Source pages:** 20, 24, 26, 27, 28

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q8 (easy): What is Amazon EC2?

**Expected topic:** AWS Overview

**Chunks retrieved:** 5 | **Time:** 6.24s

**Answer:**

**Amazon EC2 (Amazon Elastic Compute Cloud)** is a web service that provides secure, resizable compute capacity in the cloud (Page 42).

According to the context (Page 42), Amazon EC2 has the following characteristics:

- **Designed for web-scale computing**: It is designed to make web-scale computing easier for developers.
- **Simple web interface**: It allows you to obtain and configure capacity with minimal friction.
- **Complete control**: It provides you with complete control of your computing resources and lets you run on Amazon's proven computing environment.
- **Quick scaling**: It reduces the time required to obtain and boot new server instances (called Amazon EC2 instances) to minutes, allowing you to quickly scale capacity, both up and down, as your computing requirements change.
- **Pay-as-you-use pricing**: It changes the economics of computing by allowing you to pay only for capacity that you actually use.
- **Resilience tools**: It provides developers and system administrators the tools to build failure-resilient applications and isolate themselves from common failure scenarios.

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q9 (medium): How does AWS support high availability across regions?

**Expected topic:** AWS Architecture

**Chunks retrieved:** 5 | **Time:** 9.01s

**Answer:**

Based on the provided context, AWS supports high availability across regions through the following mechanisms:

1. **Multi-Region Architecture**: AWS infrastructure is built around Regions and Availability Zones (Page 15). An AWS Region is a physical location in the world containing multiple Availability Zones, each consisting of one or more discrete data centers with redundant power, networking, and connectivity housed in separate facilities.

2. **Fault Isolation within Regions**: Each Region consists of at least two (often more) Availability Zones designed for fault isolation. They are connected to multiple Internet Service Providers (ISPs) and different power grids, and are interconnected using high-speed links for LAN connectivity between Availability Zones (Page 6).

3. **Disaster Recovery Design**: AWS recommends designing systems to span multiple Availability Zones and to survive temporary or prolonged failure of an Availability Zone in the case of a disaster. Users are responsible for carefully selecting the Availability Zones where their systems reside (Page 6).

4. **Multi-Region Connectivity for High Availability**: When using multiple AWS Regions, customers need multiple AWS Direct Connect (DX) locations in at least 2 regions, along with redundant circuits and multiple VPN tunnels between separately deployed private IP address spaces (Page 67).

5. **Regional Services with Cross-AZ Replication**: Some AWS services, such as Amazon EFS, are regional services that store data within and across multiple Availability Zones for high availability and durability, allowing access to file systems across both Availability Zones and AWS Regions (Page 139).

**Note**: The context primarily discusses high availability within a region (via Availability Zones) and mentions multi-region considerations, but does not provide extensive details specifically about cross-region high availability architectures.

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q10 (medium): What is AWS CloudTrail and why is it used?

**Expected topic:** AWS Security

**Chunks retrieved:** 5 | **Time:** 7.6s

**Answer:**

Based on the provided context, **AWS CloudTrail** is a service that **records AWS API calls** for your account. It is used for the following purposes:

- **Auditing**: CloudTrail delivers log files to you for auditing of API activity (Page 27).
- **Security analysis**: The AWS API call history produced by CloudTrail enables security analysis (Page 98).
- **Resource change tracking**: It enables resource change tracking (Page 98).
- **Compliance auditing**: It supports compliance auditing (Page 98).
- **Change Management**: CloudTrail is listed as a key component of Change Management, working alongside services like AWS Config and Amazon CloudWatch to track and record configuration changes in your AWS environment (Page 27).
- **Detective Controls**: CloudTrail is also part of the Detective Controls category in AWS security, working together with AWS Config, Amazon GuardDuty, and Amazon CloudWatch (Page 21).

In summary, AWS CloudTrail provides a record of API activity in your AWS account, which supports auditing, security monitoring, resource change tracking, and compliance requirements.

**Sources: Pages 21, 27, and 98**

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q11 (edge_case): What is the capital of France?

**Expected topic:** NONE - should say not found

**Chunks retrieved:** 5 | **Time:** 4.69s

**Answer:**

I don't have this information in the provided documents. The context provided covers AWS services, the AWS Well-Architected Framework, cloud computing concepts, and related topics, but does not contain any information about France or its capital.

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q12 (edge_case): How do I bake a chocolate cake?

**Expected topic:** NONE - should say not found

**Chunks retrieved:** 5 | **Time:** 4.31s

**Answer:**

I don't have this information in the provided documents. The context provided covers AWS-related topics such as AWS Systems Manager Automation, cost optimization, data classification, and network segmentation, but does not contain any information about baking a chocolate cake.

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q13 (hard): What is serverless computing and how does AWS Lambda relate to it?

**Expected topic:** AWS Overview or Architecture

**Chunks retrieved:** 5 | **Time:** 8.19s

**Answer:**

Based on the provided context, there is no explicit definition of "serverless computing" as a general concept, but the context describes several characteristics of serverless services and how AWS Lambda fits into this paradigm.

**Key characteristics of serverless computing as described in the context:**

- You run code without provisioning or managing servers (Page 47)
- You pay only for the compute time you consume — there is no charge when your code is not running (Pages 40, 47)
- The service handles everything required to run and scale your code with high availability (Page 47)
- There is zero administration required from the user (Page 47)

**How AWS Lambda relates to serverless computing:**

According to Page 40, AWS Lambda is categorized under the "Serverless" category of AWS compute services and is described as a way to "Run code without thinking about servers." It is one of several AWS serverless offerings, alongside:
- AWS Fargate (serverless compute for containers)
- AWS App Runner (build and run containerized applications on a fully managed service)
- Amazon Keyspaces (a serverless Apache Cassandra–compatible database service) — Page 56
- ElastiCache Serverless (Page 56)

**How AWS Lambda works (Page 47):**
- You upload your code, and Lambda takes care of running and scaling it
- It can run code for virtually any type of application or backend service
- Code can be set up to automatically run from other AWS services (e.g., Amazon SNS topics can trigger Lambda functions, per Page 31) or called directly from any web or mobile app

In summary, AWS Lambda is AWS's primary serverless compute service that embodies the serverless model by eliminating server management and charging only for actual compute time used.

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q14 (hard): Compare the cost implications of on-demand vs reserved EC2 instances

**Expected topic:** AWS Overview

**Chunks retrieved:** 5 | **Time:** 8.51s

**Answer:**

# Cost Comparison: On-Demand vs. Reserved EC2 Instances

Based on the provided context (Pages 38, 42, and 43), here is a comparison of the cost implications:

## On-Demand Instances
- **Pricing Model:** Pay for compute capacity by the hour or by the second, depending on the instance type (Page 42).
- **Commitments:** No longer-term commitments or upfront payments are required (Page 42).
- **Flexibility:** You can increase or decrease compute capacity based on application demands and only pay the specified per-hourly rates for the instance used (Page 42).
- **Best For:** Users who prefer low cost and flexibility without any up-front payment or long-term commitment, and applications with short-term, spiky, or unpredictable workloads that cannot be interrupted (Page 42).

## Reserved Instances
- **Discount:** Provide a significant discount of **up to 72%** (Page 43) compared to On-Demand Instance pricing — though Page 38 cites savings of **up to 75%** off On-Demand pricing.
- **Capacity:** Allow you to reserve capacity (Page 38).
- **Flexibility:** With **Convertible Reserved Instances**, you have the flexibility to change families, operating system types, and tenancies while still benefiting from Reserved Instance pricing (Page 43).

## Key Cost Takeaways
| Aspect | On-Demand | Reserved |
|---|---|---|
| Up-front cost | None | Required (commitment-based) |
| Discount vs. On-Demand | Baseline | Up to 72–75% savings |
| Commitment length | None | Long-term (implied) |
| Flexibility | High (scale up/down freely) | Lower, though Convertible RI offers some flexibility |

**Summary:** Reserved Instances offer substantial cost savings (up to 72–75%) in exchange for a long-term commitment, while On-Demand Instances provide maximum flexibility with no commitment but at a higher per-hour cost (Pages 38, 42, 43).

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

## Q15 (hard): What is defense in depth in the context of AWS security?

**Expected topic:** AWS Security

**Chunks retrieved:** 5 | **Time:** 7.04s

**Answer:**

# Defense in Depth in AWS Security

Based on the provided context, **defense in depth** is an AWS security principle that involves applying multiple layers of security controls rather than relying on protection at a single outer layer.

## Key Aspects (from Page 15)

Rather than focusing on protection of a single outer layer, defense in depth means applying security controls at **all layers**, including:
- Edge network
- VPC (Virtual Private Cloud)
- Subnet
- Load balancer
- Every instance
- Operating system
- Application

## Application to Networks (from Page 19)

Both **public and private networks** require multiple layers of defense to protect against:
- External network-based threats
- Internal network-based threats

This same principle applies to **compute resources** (EC2 instances, containers, AWS Lambda functions, database services, IoT devices, etc.), which also require multiple layers of defense against external and internal threats.

## Layered Network Defense Examples (from Page 47)

AWS supports layered network defense through technologies such as:
- Third-party firewall devices installed on Amazon EC2 instances (soft blades)
- Unified threat management (UTM) gateways
- Intrusion prevention systems
- Data loss management gateways
- Anomaly detection gateways
- Advanced persistent threat detection gateways

The Amazon VPC infrastructure also supports this approach by enabling **multiple layers of load balancers**, which is particularly important when using threat protection gateways to secure clusters of web servers, application servers, or other critical servers where scalability is key.

**Sources:** Pages 15, 19, and 47

**Manual verdict:** [x] Correct  [ ] Partially correct  [ ] Incorrect

---

