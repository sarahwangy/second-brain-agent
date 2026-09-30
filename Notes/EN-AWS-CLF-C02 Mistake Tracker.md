# AWS CLF-C02 Mistake Tracker

> Used alongside the question bank in `考证/AWS/Aws-CLF-C02-10月考/`. After each practice batch, log the questions I got wrong or was unsure about, then come back to review them a few days later. The original PDFs stay untouched — this is purely my own mistake-tracking log.

## Table of Contents

- [How to Use This](#how-to-use-this)
- [Mistake Log](#mistake-log)
- [Study Progress Tracker](#study-progress-tracker)
- [Supplementary Practice Questions (from an interactive component)](#supplementary-practice-questions-from-an-interactive-component)
- [Review To-Dos](#review-to-dos)
- [Notes](#notes)

---

## How to Use This
1. Self-test with the `_en_without_answer` version, finish a batch of questions
2. Check answers with the `_en_with_discussion` version, and log anything wrong/guessed into the table below
3. Come back 2–3 days later and redo the questions in the table — check the "Reviewed" column if correct, increment "Times missed again" if wrong

## Mistake Log

| Topic | Question # | Concept tested | My answer | Correct answer | Why I got it wrong | Reviewed✓ | Times missed again |
|---|---|---|---|---|---|---|---|
| Topic 1 | 668 | EC2 instance types vs. HPC workloads | C | B | Confused HPC (compute-intensive) with Storage Optimized (disk I/O-intensive) — got misled by the word "data lakes" into thinking storage, and missed the key distinction that "HPC = CPU & network bound" |
| Topic 1 | 634 | Choosing an EC2 purchasing option (running 1 year continuously + no interruptions + cheapest) | D | A | Chose On-Demand (the most expensive, suited to uncertain usage), didn't recognize that "runs for 1 year, no interruptions" is the textbook Reserved Instances scenario; also missed that "cheapest" means picking the highest upfront-payment option, All Upfront |
| Topic 1 | 703 | AWS Application Discovery Service (pre-migration assessment) | B | A | Chose Application Migration Service (which actually performs the migration), missed that the question said "doesn't want to replicate the workload to AWS yet" — that calls for Discovery Service to assess first, not Migration Service |
| Topic 1 | 707 | AWS Global Accelerator (improving performance for a global application) | C | A | Chose ElastiCache (solves slow database queries), didn't recognize the question was asking about "global users accessing a public app behind an ALB" — a network path/latency problem, which calls for Global Accelerator, unrelated to database caching |
| Topic 1 | 621 | ELB vs. Auto Scaling responsibility split | A | B | Chose "ELB automatically scales resources," confusing ELB's and Auto Scaling's responsibilities — ELB only distributes existing traffic across existing instances; it's not responsible for creating new instances/auto-scaling, that's Auto Scaling's job |
| Topic 1 | 705 | The Elasticity cloud advantage (testing a new application scenario) | D | B | Chose "manage all cloud-related maintenance tasks" (which actually describes the opposite of a cloud advantage), missed that "testing a new application" maps to elastic scaling + no long-term commitment (Elasticity), not maintenance management |

## Study Progress Tracker

| Date | Questions done (number range) | Accuracy | Notes |
|---|---|---|---|
| 08.20 | 690, 668, 658, 676, 619, 634 | 3/6 (50%) | First practice session, randomly sampled from the back half of the bank (600–719); got the HPC instance-type question wrong (confused compute-intensive vs. storage-intensive), got the EC2 purchasing-option question wrong (didn't recognize a long-term stable workload should use Reserved Instances); got the CAF/Well-Architected concept questions right |
| 08.20 | 641, 709, 703, 686, 707 | 3/5 (60%) | Continued practicing; got both the Cost Explorer question and the CAF Business Perspective question right (the latter is a contested question — the official answer is A, but the community is split 50/50); question 703 was the first time I hit a "Discovery vs. Migration Service" question and mixed the two up, but immediately after, question 686 tested nearly the same concept and I got it right that time, showing the correction stuck in the moment; got 707 wrong by misjudging a "global network acceleration" need as a "database caching" need |
| 08.21 | 652, 621, 557, 705 | 2/4 (50%) | Got the basic On-Demand/Reserved Instances scenario questions right; got 621 wrong by confusing ELB's and Auto Scaling's responsibilities (ELB isn't responsible for auto-scaling); got 705 wrong by not connecting "testing a new application" to the Elasticity cloud advantage, instead picking an unrelated "maintenance management" option |

## Supplementary Practice Questions (from an interactive component)

> Note: these practice questions were presented to me through an interactive component, and my answers weren't reported back to me — so below, I've compiled every question along with the correct answer and explanation, for self-review to identify where I went wrong.

**Q1.** A company's S3 bucket was set to be publicly readable, leading to a data breach. Under the Shared Responsibility Model, who is responsible for this security incident?
✅ The customer — bucket permission configuration falls under "security IN the cloud"

**Q2.** Which of the following is NOT one of AWS's officially listed six advantages of cloud computing?
✅ Guaranteeing 100% zero system downtime (AWS never makes this kind of absolute promise)

**Q3.** A startup wants to run an interruption-tolerant batch job at the lowest possible cost, one that can be interrupted at any time. Which EC2 pricing model should it choose?
✅ Spot Instances

**Q4.** Regarding the IAM principle of least privilege, which practice best aligns with it?
✅ Grant users only the minimum set of permissions necessary to complete their current task

**Q5.** An EC2 instance needs to attach a persistent block storage volume that can only be mounted to a single instance at a time. Which storage service should be chosen?
✅ Amazon EBS

**Q6.** A company wants usage across multiple AWS accounts to be aggregated into a single bill (for better volume discounts) while centrally managing those accounts. What feature should it use?
✅ AWS Organizations + Consolidated Billing

**Q7.** An enterprise needs a 15-minute technical-support response time and wants a dedicated Technical Account Manager (TAM). Which Support Plan should it choose?
✅ Enterprise

### Round 2
**Q1.** Choosing instance types wisely and reducing idle resources to lower energy consumption and improve resource efficiency best aligns with which Well-Architected pillar? ✅ Sustainability
**Q2.** What's the most direct, effective way to improve disaster resilience so business continues even if one data center fails? ✅ Deploy resources across multiple AZs within the same Region
**Q3.** Need to audit which IAM User called which API operations and when, over the past week — which service's logs should be checked? ✅ CloudTrail
**Q4.** Only an inbound rule (port 443) was configured on a Security Group, no outbound rule, yet responses come through fine — why? ✅ Security Groups are stateful; outbound return traffic is automatically allowed
**Q5.** Need to retain 7 years of audit logs, rarely accessed, retrieval can tolerate a wait of a few hours, want the lowest possible storage cost — which S3 class? ✅ S3 Glacier Deep Archive
**Q6.** A web application is frequently hit by SQL injection and XSS attacks and needs to filter malicious application-layer requests — which service? ✅ AWS WAF
**Q7.** Want to run containerized applications without managing any underlying servers/clusters, focusing only on deploying and running containers — which approach? ✅ AWS Fargate
**Q8.** Want a Lambda function triggered to send a notification when an EC2 instance's state changes to "stopped," and a completely different workflow triggered when it changes to "terminated" — which service? ✅ Amazon EventBridge
**Q9.** Before migrating a new project to AWS, want to estimate the roughly monthly cost first — which tool? ✅ AWS Pricing Calculator
**Q10.** 500TB of on-prem historical data needs to migrate to S3, but limited network bandwidth means it would take over a month at the current speed — which service? ✅ AWS Snowball

### Round 3
**Q1.** A malicious IP is detected scanning ports — need to explicitly block all traffic from that IP without affecting other normal access. How? ✅ Add an explicit Deny rule for that IP in the subnet's NACL
**Q2.** Regarding the relationship between a NACL and a subnet, which statement is correct? ✅ A single NACL can be associated with multiple subnets, but a subnet can only be associated with one NACL at a time
**Q3.** Storing image thumbnails that can be regenerated at any time, infrequently accessed, fine to lose and rebuild, want the lowest possible storage cost — which class? ✅ S3 One Zone-IA
**Q4.** An order service sends messages to an inventory service via SQS. If the inventory service goes down for 10 minutes during a deployment, what happens to messages sent during that window? ✅ They stay in the queue and are consumed once the service recovers — nothing is lost
**Q5.** Global employees need to upload medium-sized design files to a headquarters S3 bucket, but cross-region uploads are slow — which service accelerates this? ✅ Amazon S3 Transfer Acceleration
**Q6.** In a VPC, what determines whether a subnet is a Public or Private Subnet? ✅ Whether the subnet's route table has a route pointing to an Internet Gateway
**Q7.** Why is it recommended to attach an IAM Role to an EC2 instance accessing S3, rather than hardcoding an Access Key in the code? ✅ An IAM Role provides temporary credentials, avoiding the need to hardcode secrets

### Round 4
**Q1.** Storing shopping-cart data with massive volume, extremely high read/write concurrency, flexible structure, and latency-sensitive requirements — which database? ✅ Amazon DynamoDB
**Q2.** Regarding IAM policy evaluation logic, which statement is correct? ✅ Everything is denied by default unless explicitly allowed; if both an explicit Deny and an Allow exist, Deny takes precedence
**Q3.** An EC2 instance's CPU utilization exceeding 80% for 5 consecutive minutes should automatically trigger Auto Scaling to add an instance — which service does this alarm-triggering mechanism depend on? ✅ CloudWatch
**Q4.** A task runs once a day at 3am for just 2 minutes, needing no compute resources the rest of the time — which is the most cost-effective approach? ✅ Use Lambda, billed by invocation count and duration
**Q5.** Want an email alert when monthly AWS spend approaches 80% of the budget — which tool? ✅ AWS Budgets
**Q6.** Static S3 assets are being fetched by users worldwide, but every request has to go back to the same origin Region, making it slow for remote users — how to optimize? ✅ Pair S3 with CloudFront for global content distribution
**Q7.** Want to automatically detect and alert on potential malicious behavior in an account — anomalous logins/suspicious API calls, etc. — which service? ✅ Amazon GuardDuty

### Round 5
**Q1.** Need to share a contract file stored in a private S3 bucket with a client — accessible only within 24 hours, then the link expires — and the whole bucket can't be made public. How? ✅ Generate a presigned URL with an expiration time
**Q2.** In an S3 + CloudFront architecture, what's the main purpose of configuring Origin Access Control (OAC)? ✅ To prevent bypassing CloudFront and accessing the raw S3 URL directly
**Q3.** Need to aggregate data from order/customer-service/advertising systems for management to run cross-department historical sales-trend analysis and BI reporting — which database? ✅ Amazon Redshift
**Q4.** A website needs to route requests to different backend services based on URL path — which type of load balancer? ✅ Application Load Balancer (ALB)
**Q5.** Someone registers two AWS accounts and wants to merge the "12 months free" Free Tier allowance from both into one — is this possible? ✅ No — each account's allowance is independently bound and cannot be shared or merged
**Q6.** A European company must store user data within EU territory due to GDPR requirements — what should be the top priority when choosing a Region? ✅ A combination of factors: latency, compliance/data-sovereignty requirements, service availability, and cost

## Review To-Dos
- [ ] First full pass: work through the back half of the bank (the newer questions)
- [ ] Log mistakes into the table above
- [ ] Review the first batch of mistakes the following day

## Notes
- This table can be updated incrementally — just tell me "update the CLF-C02 mistake tracker" after each study session, and new mistakes get added without regenerating the whole table
- The official answer is occasionally disputed — the community discussion's vote distribution can serve as a reference; don't blindly memorize a single answer
- The question bank has 719+ questions total (`_en_without_answer.pdf`, 219 pages), same source and format as the AIF-C01 bank
