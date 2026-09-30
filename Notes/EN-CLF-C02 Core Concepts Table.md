# AWS CLF-C02 Core Concepts Table

> Extracted from the `Aws-CLF-C02-10月考/` question bank (719 questions), ranked by "how many questions this concept appears in" (highest first) — same method as the AIF-C01 concept table (`⭐️-08.14-AWS-AIF-C01-核心概念表.md`). Question numbers are this bank's own numbering (not the official exam's), so you can search "Question #N" directly in the PDF to jump to the question.
>
> ⚠️ Note: this is a regex-based keyword frequency scan (searching each question for service names). Concepts with low counts (e.g. PII, TCO, OpEx/CapEx) may be undercounted due to wording variations — treat this as a priority guide, not an exact count.

## Table of Contents

- [How to Use This](#how-to-use-this)
- [Concept Table](#concept-table)
- [Review Priority Recommendations](#review-priority-recommendations)
- [Question Number Index (this bank's numbering, in concept-table order)](#question-number-index-this-banks-numbering-in-concept-table-order)

---

> For deeper explanations (with analogies and common-mistake corrections) see [[EN-CLF-C02 Core Services Q&A]]; for hands-on operational steps see [[EN-CLF-C02 Operational Steps Cheat Sheet]].

## How to Use This

The more questions a concept appears in, the more it's a core exam battleground — prioritize mastering it. **EC2, S3, Elasticity, IAM, and On-Demand/Reserved/Spot — these pricing + compute + storage + permissions fundamentals account for the overwhelming majority of questions in the bank.** Without nailing these, passing is unlikely. Concepts appearing only single digits of times just need a general understanding — don't over-invest in their details.

Mapped against Domain weights: **specific service names like EC2/S3/RDS/DynamoDB/VPC map to Domain 3 (34% weight, the largest)**; **IAM/Shared Responsibility/Encryption/Compliance map to Domain 2 (30% weight, mostly already covered from AIF-C01)**; **On-Demand/Reserved/Spot/Savings Plans/Support Plans map to Domain 4 (12% weight)**; **Elasticity/the 7 R's of migration map to Domain 1 (24% weight)**.

## Concept Table

| Concept | What it is | When it's used |
|---|---|---|
| **Amazon EC2** (175 questions) | AWS's virtual machine service — rent compute resources (CPU/memory) on demand; the most fundamental, most commonly used compute service | Used when you need a server where you control the OS yourself. Highest frequency in the bank — must master instance types and pricing models |
| **Amazon S3** (83 questions) | Object storage service for files (images, video, backups, static websites); billed by capacity + request count, with multiple storage tiers (Standard/IA/Glacier, etc.) | Static assets, backups, data lake scenarios; exam frequently tests which storage tier is cheapest for a given access pattern |
| **Elasticity** (78 questions) | One of cloud computing's core advantages — resources scale up/down automatically based on demand, no need to guess capacity in advance or run short when demand spikes | The core keyword for Domain 1 "cloud advantages" questions, often paired with Auto Scaling |
| **IAM** (76 questions) | Identity and Access Management — controls "who can access what resource, and do what," the foundation of AWS security | Tested in nearly every AWS certification; least-privilege principle and the distinction between users/groups/roles/policies are high-frequency topics |
| **On-Demand** (46 questions) | Pay for what you use, no long-term commitment, highest unit price but most flexible | Short-term/unpredictable-usage scenarios; the default billing mode, often compared against Reserved/Spot in "which is cheapest" questions |
| **Reserved Instances** (45 questions) | Commit to 1 or 3 years for a much lower price than On-Demand | Long-term, stable, predictable workloads (e.g. an always-on database); saves money but sacrifices flexibility |
| **Amazon RDS** (42 questions) | Managed relational database service (supports MySQL/PostgreSQL/SQL Server, etc.), AWS handles backups/patching/failover | For when you need a relational database but don't want to manage server operations yourself |
| **AWS Trusted Advisor** (41 questions) | Automatically inspects account configuration and gives recommendations across five dimensions: cost optimization/performance/security/fault tolerance/service limits | The standard answer for "how do I find issues/optimization opportunities in my account" |
| **Shared Responsibility Model** (41 questions) | AWS is responsible for "security OF the cloud" (hardware, infrastructure), the customer is responsible for "security IN the cloud" (data, configuration, access control) — this boundary is always tested | Already covered in AIF-C01, directly reusable; "should AWS or the customer own this security issue" questions appear frequently |
| **Spot Instances** (41 questions) | Uses AWS's spare compute capacity, cheapest option (up to 90% off On-Demand), but AWS can reclaim it anytime (2-minute warning) | Interruption-tolerant workloads (batch processing, testing, fault-tolerant distributed jobs); not for critical business workloads |
| **Amazon VPC** (37 questions) | Carve out your own private virtual network within AWS, define your own subnets, routing, and security groups | The foundation of network isolation and security architecture; core of Domain 3 networking questions |
| **Amazon DynamoDB** (36 questions) | Fully managed NoSQL database, auto-scales on demand, suited to massive data + low-latency read/write scenarios | Compared against RDS in "relational vs NoSQL, which to pick" questions — DynamoDB suits simple-structure, high-concurrency scenarios |
| **Amazon GuardDuty** (35 questions) | Intelligent threat-detection service, uses machine learning to continuously monitor account activity for anomalies (unusual API calls, malicious IPs, etc.) | The standard answer for "how to automatically detect security threats"; easily confused with Inspector (finds vulnerabilities) and WAF (blocks attacks) |
| **AWS WAF** (33 questions) | Web Application Firewall, filters malicious HTTP/HTTPS traffic at the application layer (SQL injection, XSS attacks, etc.) | Protects public-facing web applications, often paired with AWS Shield (DDoS protection) — the two protect at different layers |
| **AWS Lambda** (32 questions) | Serverless compute service — upload code, AWS runs it automatically, no server management, billed by actual execution time | The core answer for "don't want to manage servers, pay only for usage" — the heart of serverless architecture |
| **AWS Inspector** (30 questions) | Automated security assessment service, scans EC2/container images for known vulnerabilities | Distinction from GuardDuty: Inspector finds "known vulnerabilities" (static scanning), GuardDuty finds "anomalous behavior" (real-time monitoring) |
| **Amazon CloudWatch** (29 questions) | Monitoring service — collects metrics (CPU usage, etc.), sets alarms, views logs | The standard answer for "how to monitor resource health, set up alerts" |
| **Encryption** (28 questions) | Protection for data in transit and data at rest | Already covered in AIF-C01, directly reusable, often paired with KMS |
| **Amazon ECS/EKS/Fargate** (28 questions) | Container orchestration services — ECS is AWS's own container management service, EKS is managed Kubernetes, Fargate is a serverless container-running mode usable with either (no need to manage underlying EC2 instances) | The choice when running Dockerized applications; Fargate often appears as the answer for "don't want to manage servers" |
| **AWS Direct Connect** (28 questions) | A dedicated physical network connection from an on-prem data center to AWS, bypassing the public internet | For stable, low-latency, high-bandwidth hybrid cloud connectivity — compared against VPN in "which is more suitable" questions |
| **AWS Well-Architected Framework** (28 questions) | An architecture best-practices framework with six pillars (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability) | AIF-C01 covered the pillar names; CLF-C02 tests more specific pillar content and assessment tools |
| **AWS CloudTrail** (27 questions) | Logs all API calls made within an AWS account (who did what, when) | The standard answer for audit trails; often confused with AWS Config (which tracks configuration state changes) |
| **AWS Shield** (26 questions) | DDoS protection service — Standard is free and enabled automatically; Advanced is paid, offering stronger protection plus expert support | Defends against high-volume DDoS attacks; used alongside WAF (application-layer protection) but at a different protection layer |
| **Amazon CloudFront** (26 questions) | CDN content-delivery network, caches content at global edge locations so users get faster load times from a nearby location | The standard solution for accelerating static content delivery and reducing origin-server load |
| **AWS Config** (25 questions) | Continuously tracks the change history of AWS resource configurations, checks compliance against preset rules | The standard answer for "was a configuration changed unexpectedly, and is it currently compliant" |
| **AWS CloudFormation** (25 questions) | Defines and auto-deploys AWS infrastructure using code (template files) — i.e., Infrastructure as Code | Used when you need to deploy the same infrastructure architecture repeatedly and consistently, avoiding manual console clicks and errors |
| **Amazon Aurora** (25 questions) | AWS's own high-performance relational database, compatible with MySQL/PostgreSQL, better performance than standard RDS | For relational database scenarios needing higher performance/availability than standard RDS |
| **Cost Explorer** (23 questions) | A tool to visualize and analyze AWS spending trends, can break down costs by service/time/tag | The standard answer for "how to analyze/forecast AWS spend" |
| **AWS Organizations** (23 questions) | Centrally manages multiple AWS accounts (consolidated billing, unified permission boundaries via SCPs) | Used when an enterprise has multiple AWS accounts (different departments/environments) needing unified management |
| **AWS Systems Manager** (22 questions) | A toolset for centrally managing/automating operations on EC2 and other resources (patch management, remote command execution, etc.) | Operational automation at scale across many EC2 instances |
| **Amazon EBS** (21 questions) | A block storage volume attached to an EC2 instance (like a virtual hard drive), data persists, survives EC2 reboots | Attached when EC2 needs persistent storage (database files, etc.), distinct from instance store (temporary) |
| **Availability Zone** (21 questions) | Multiple physically isolated data centers within a Region, low-latency connections between AZs but isolated failure domains | Domain 1 global-infrastructure topic; "deploy across multiple AZs to improve availability" is a common answer |
| **Compliance (ISO/SOC/PCI)** (20 questions) | Third-party compliance certifications AWS has obtained (ISO 27001, SOC reports, PCI DSS payment-card industry standard, etc.) | Consulted when a customer wants to verify AWS infrastructure meets industry compliance requirements |
| **AWS Budgets** (20 questions) | Sets spending thresholds, sends automatic alerts as spend approaches/exceeds budget | The standard answer for "how to prevent unexpected AWS bill overruns" — complements Cost Explorer (which looks at history) |
| **Amazon Redshift** (18 questions) | Fully managed data warehouse service, purpose-built for large-scale data analysis/BI queries (columnar storage, suited to aggregate queries) | Used for complex analytical queries and building data warehouses — different purpose from RDS (transaction-oriented) |
| **AWS Artifact** (17 questions) | A self-service portal for downloading AWS compliance reports/agreements (doesn't do detection itself, it's a document hub) | Used when you need to download ISO certificates, SOC reports, and other compliance documents |
| **Savings Plans** (17 questions) | Commit to a stable usage level for a set duration (without locking to a specific instance type) in exchange for a lower price than On-Demand — more flexible than Reserved Instances | For stable-usage scenarios where instance type/region may change — a more flexible alternative to Reserved Instances |
| **AWS Support Plans** (17 questions) | Four tiers: Basic (free), Developer, Business, Enterprise — response time and support depth increase up the tiers | A core Domain 4 topic — remember the rough price threshold and use case for each tier |
| **Amazon Route 53** (16 questions) | DNS domain-resolution service, also supports health checks and traffic-routing policies | Domain management, cross-region traffic distribution/failover scenarios |
| **AWS Secrets Manager** (15 questions) | Centrally stores and automatically rotates secrets/passwords/API keys | Used when an application needs to securely access sensitive credentials like database passwords and wants automatic periodic rotation |
| **Auto Scaling** (15 questions) | Automatically increases/decreases EC2 instance count based on load, pairs with the Elasticity concept | For applications with fluctuating traffic — automatically handles peaks/valleys, saving cost while maintaining performance |
| **Amazon Macie** (14 questions) | Automatically scans S3 data, uses ML to detect sensitive information (PII, credit card numbers, etc.) | Already covered in AIF-C01, directly reusable |
| **The "7 R's" of migration strategy** (7 questions) | Rehost/Replatform/Repurchase/Refactor/Retire/Retain/Relocate — seven strategies for migrating workloads to the cloud | Domain 1 cloud-migration topic; remember each R roughly represents an increasing degree of change |

---

## Review Priority Recommendations

**Top priority (extremely high question count, must master)**: Amazon EC2, Amazon S3, Elasticity, IAM, the three billing models On-Demand/Reserved/Spot

**Second priority (30–45 questions, cover thoroughly)**: Amazon RDS, AWS Trusted Advisor, Shared Responsibility Model, Amazon VPC, Amazon DynamoDB, GuardDuty, WAF, Lambda

**Already covered in AIF-C01, directly reusable (no need to re-study in depth)**: Shared Responsibility Model, IAM, Encryption, AWS Well-Architected Framework, Compliance (ISO/SOC/PCI), AWS Artifact, Amazon Macie

**Domain 3 specific services that are entirely new (never tested in AIF-C01, go through these properly)**: ECS/EKS/Fargate, Elastic Beanstalk, Aurora, Redshift, Route 53, Direct Connect, Systems Manager, CloudFormation

**Domain 4 billing-related (entirely new, mostly memorization)**: the differences between the four billing models On-Demand/Reserved/Spot/Savings Plans, the four AWS Support Plan tiers, and the division of labor between Cost Explorer/Budgets

**Concepts with single-digit question counts**: just know roughly what they are and when they're used — no need to memorize exact parameters (e.g. for the 7 R's of migration, knowing there are roughly these strategies and their rough meaning is enough; no need to recite exact definitions).

---

## Question Number Index (this bank's numbering, in concept-table order)

- **Amazon EC2**: 2-4, 7-9, 16-17, 20, 24, 29, 40, 46, 57, 60, 67-68, 88, 97, 99, 108, 112, 116-118, 121, 128-130, 132, 136, 138, 144, 146-147, 157, 162, 175, 179, 183-184, 190, 192-193, 198-200, 209, 213, 222, 230, 232-233, 235, 239-240, 242-243, 246, 250, 254, 266, 269, 272, 281, 289-290, 293, 298, 302, 305, 311, 314, 318, 322-323, 329-331, 340, 346, 348, 350, 358-359, 361-363, 365, 373-374, 377, 380, 384, 390, 393, 399, 413, 425-426, 429, 431-432, 437, 440-442, 444, 462-463, 465, 467, 469, 472-473, 482, 494, 497-498, 502, 508, 513, 515, 521, 524, 531, 535, 538, 542, 546, 548, 554-555, 557, 560, 564-566, 569, 573, 578, 589-590, 592-593, 599-600, 604, 610, 634, 637, 639, 644-646, 652, 656-657, 664, 668, 674, 677, 680, 682, 684, 689, 691, 693, 697, 701, 706, 708, 711-712, 714
- **Amazon S3**: 1, 3-4, 18, 29, 36, 43, 49, 54, 58, 61, 83, 87, 90, 110, 120, 123, 132, 143, 153, 161, 163, 165, 168, 179, 183, 194, 196, 201-202, 208, 219, 233, 251, 255, 262, 274, 286, 293-294, 311-313, 318, 320, 331, 338, 349, 368, 402, 414, 416, 446, 450, 453, 456, 469, 496-497, 503, 506, 523, 526, 533, 535, 543, 550, 560, 587, 593, 596, 607, 623, 625, 644, 646, 648, 658, 660, 671, 683, 700, 718
- **Elasticity**: 3, 14, 17, 40, 54, 64, 68, 77, 81, 87, 90, 103, 109, 116, 121, 125, 139, 152-153, 167, 179, 181, 183, 193-194, 196, 205, 211, 228, 231, 255, 299, 304-305, 311, 313, 317, 322-323, 347, 349, 353, 356, 361, 363, 366, 397, 400, 426, 450-451, 456, 461, 464, 469, 473, 492, 517, 530, 533, 536, 552, 560, 573, 587, 590, 593-594, 614, 621-622, 625, 638, 673-674, 678, 708, 718
- **IAM**: 4, 26, 36, 39, 52, 54, 58, 60, 83, 94, 98-99, 105-106, 108, 111, 119, 122, 132, 149, 160, 165, 168, 170, 177, 192, 200, 202, 216-217, 220-221, 229, 232, 234, 273, 279, 283, 288, 296-297, 300, 336, 339, 343, 348, 373, 385, 391-392, 409, 412, 416, 428, 433-434, 437, 448, 460, 474-475, 477, 482, 511, 534, 539, 571, 582, 584, 595, 610, 636, 648, 650, 656, 716
- **On-Demand**: 16, 20, 33, 46, 57, 67, 112, 128-129, 136, 138, 144, 162, 180, 213, 222, 230, 245, 250, 254, 266, 272, 281, 350, 380, 429, 431, 462, 479, 494, 508, 524, 538, 548, 557, 565-566, 569, 578, 634, 639, 652, 677, 684, 691, 711
- **Reserved Instances**: 16, 20, 33, 46, 57, 67-68, 104, 128-129, 136, 144, 162, 213, 230, 245, 250, 254, 266, 272, 281, 350, 362, 411, 429, 431, 462, 465, 521, 524, 538, 548, 551, 557, 564-566, 578, 634, 639, 677, 684, 697, 701, 711
- **Amazon RDS**: 7, 43, 47, 55, 63, 79, 96, 105, 161, 182-183, 190, 200, 227, 235, 240, 242, 280, 293, 322, 330, 369, 374, 409, 411, 428, 438, 489, 503, 525, 551, 587-588, 592, 596, 623, 627, 662, 664, 680, 696, 718
- **AWS Trusted Advisor**: 2, 10, 41, 53, 65, 100, 122, 126, 135, 140, 175, 184, 214, 224-226, 231, 273, 288, 298, 377-378, 405, 408, 412, 425, 448, 457, 479, 513, 520, 553, 575, 599, 611-612, 635, 637, 654, 698, 713
- **Shared Responsibility Model**: 5, 29, 42, 56, 79, 105, 130, 132, 146, 156, 163, 173, 198, 200, 239, 241, 243, 249, 282, 293, 297, 300, 334, 384, 434, 437, 475, 483, 497-498, 511, 514, 535, 544-545, 592, 609-610, 627, 631, 648
- **Spot Instances**: 16, 20, 33, 46, 57, 67, 107, 112, 128-129, 136, 144, 157, 162, 213, 230, 250, 254, 266, 272, 281, 350, 362, 431, 462, 494, 521, 524, 538, 548, 557, 565-566, 569, 578, 639, 677, 684, 689, 701, 711
- **Amazon VPC**: 21, 24, 59, 70, 86, 95, 119, 146, 150, 172, 181, 197, 199, 242, 310, 321, 326-327, 340, 352, 413-414, 474, 493, 516, 528, 536, 543, 574, 581, 604, 608, 630, 644, 653, 657, 665
- **Amazon DynamoDB**: 5, 29, 55-56, 61, 63, 66, 157, 182-183, 190, 233, 235, 241, 247, 293, 308, 330, 369-370, 389, 438, 484, 489, 497, 503, 511, 518, 587-588, 596-597, 662, 664, 672, 680
- **Amazon GuardDuty**: 2, 53, 58, 65, 68, 115, 117, 159, 168, 192, 197, 223, 280, 284, 286-287, 343, 363, 393, 413, 416, 436, 468, 474, 479, 490, 506, 509, 519, 546, 589, 603, 620, 654, 716
- **AWS WAF**: 35, 54, 80, 95, 115, 124, 126, 155, 168, 175, 184, 197, 211, 244, 280, 296, 309, 352, 412-413, 417, 425, 468, 490, 519, 536, 542, 546, 554, 606, 640, 665, 713
- **AWS Lambda**: 7, 29, 42, 92, 96, 103, 118, 235, 237, 246, 361, 365, 376, 394, 397, 426, 434, 464, 467, 476, 497, 502, 504, 537, 550, 590, 594, 600, 609, 648, 702, 708
- **AWS Inspector**: 2, 32, 41, 84, 111, 115, 117, 155, 159, 172, 175, 211, 218, 221, 224, 229, 284, 302, 310, 393, 416, 435, 468, 470, 506, 519, 654, 693, 715-716
- **Amazon CloudWatch**: 27, 31, 44, 59, 65, 91, 100, 111, 115, 119, 165, 206, 229, 244, 302, 314, 331, 343, 373, 376, 378, 435-436, 495, 513, 576, 586, 599, 707
- **Encryption**: 5, 10, 18, 74, 105, 130, 132, 158, 173, 198, 217, 219, 231, 239, 241, 282, 304, 334, 349, 418, 423, 449, 463, 483, 498, 545, 627, 636
- **Amazon ECS/EKS/Fargate**: 7, 62, 64, 103, 109, 121, 125, 234, 305, 309, 321-322, 353, 361, 363, 366, 397, 421, 440, 492, 552, 590, 594, 600, 646, 674, 708, 714
- **AWS Direct Connect**: 19, 21, 47, 70, 73, 80, 181, 263, 326-327, 355, 357, 398, 402, 445, 460, 466, 471, 473, 476, 528, 542, 547, 593, 608, 616, 630, 653
- **AWS Well-Architected Framework**: 23, 25, 30, 93, 164, 178, 185, 252, 258, 261, 268, 277, 285, 331, 337, 356, 386, 404, 424, 432, 514, 559, 619, 647, 659, 678-679, 687
- **AWS CloudTrail**: 41, 59-60, 111, 119, 155, 232, 244, 310, 373, 378, 435, 475, 495, 504-505, 513, 558, 586, 591, 599, 612, 617, 623, 628-629, 654
- **AWS Shield**: 35, 68, 78, 80, 126, 159, 175, 211, 217, 221, 223, 286-287, 296, 340, 363, 412, 417, 490, 506, 519, 546, 589, 640, 685, 693
- **Amazon CloudFront**: 49, 85, 147, 150, 181, 194, 269, 283, 289, 321, 357, 364-365, 394, 426, 468, 472, 476, 511, 528, 547, 597, 616, 643, 694, 714
- **AWS Config**: 2, 44, 74, 100, 120, 131, 155, 221, 306, 323-324, 399, 457, 470, 479, 502, 509, 513, 558, 563, 574, 580, 612, 630, 690
- **AWS CloudFormation**: 19, 51, 78, 100, 122, 161, 187, 193, 212, 253, 305, 353, 376, 451, 464, 487, 502, 517, 526, 574, 583, 591, 597, 629, 706
- **Amazon Aurora**: 55, 61, 66, 96, 153, 182, 190, 233, 240, 308, 333, 369-370, 438, 469, 488-489, 492, 545, 586, 588, 617, 649, 662, 664
- **Cost Explorer**: 9, 13, 27, 91, 104, 141, 204, 225, 259-260, 331, 378, 392, 396, 406, 432, 553, 561, 572-573, 641, 695, 706
- **AWS Organizations**: 12-13, 22, 36, 44, 122, 141, 203, 225, 247, 260, 309, 339, 348, 401, 405-406, 474, 488, 515, 553, 690, 695
- **AWS Systems Manager**: 12, 36, 72, 74, 120, 212, 218, 226, 259-260, 303, 314, 346, 375, 478, 487, 509, 591, 605, 623, 635, 682
- **Amazon EBS**: 3, 68, 74, 87, 90, 103, 153, 196, 231, 255, 311, 313, 317, 349, 450, 456, 587, 593, 614, 625, 718
- **Availability Zone**: 29, 150, 156, 186, 243, 269, 360, 372, 411, 441, 472, 508, 525, 527, 543, 555, 559, 562, 581, 627, 651
- **Compliance (ISO/SOC/PCI)**: 26, 37, 84, 174, 218, 232, 287, 436, 479, 504, 512, 523, 541, 585, 611-612, 655, 690, 714, 717
- **AWS Budgets**: 27, 91, 104, 141, 178, 204, 225, 264, 399, 405-406, 501, 553, 570, 572, 614, 637, 641, 675, 695
- **Amazon Redshift**: 14, 43, 55, 61, 96, 166, 182, 318, 330, 332-333, 369-370, 450, 458, 489, 596, 662
- **AWS Artifact**: 26, 28, 37, 84, 174, 218, 283, 287, 423, 441, 448, 457, 479, 512, 541, 611, 685
- **Savings Plans**: 46, 112, 138, 245, 264, 267, 330, 380, 508, 521, 548, 565-566, 569, 675, 697, 701
- **AWS Support Plans**: 71, 135, 236, 246, 265, 267, 319, 407, 454, 520, 556, 567, 575, 577, 602, 640, 698
- **Amazon Route 53**: 21, 70, 73, 85, 208, 242, 326-327, 426, 445, 463, 476, 496, 528, 630, 643
- **AWS Secrets Manager**: 70, 72, 120, 158, 174, 217, 394, 423, 526, 534, 571, 612, 620, 623, 650
- **Auto Scaling**: 81, 85, 138, 157, 209, 314, 363, 380, 390, 432, 442, 465, 555, 628, 663
- **Amazon Macie**: 37, 58, 73, 159, 229, 284, 286, 343, 367, 416, 494, 546, 617, 693
- **The "7 R's" of migration strategy**: 3, 148, 235, 480-481, 499-500
