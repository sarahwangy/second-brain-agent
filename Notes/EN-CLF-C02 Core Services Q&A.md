# CLF-C02 Core Services Q&A

> **Purpose**: A Q&A-style deep dive on a batch of commonly-used AWS services/concepts for CLF-C02 exam prep, with concrete examples and analogy corrections. Complements [[EN-CLF-C02 Core Concepts Table]] (a compact reference ranked by question-bank frequency) — that one is a quick-reference table, this one is the fully-worked-through Q&A record.

## Table of Contents

- [Dev / CLI Tools](#dev--cli-tools)
- [Identity and Permissions](#identity-and-permissions)
- [Infrastructure as Code (IaC)](#infrastructure-as-code-iac)
- [Service Models (Cloud Responsibility Split)](#service-models-cloud-responsibility-split)
- [Storage and Networking](#storage-and-networking)
- [Databases](#databases)
- [Compute](#compute)
- [The Monitoring/Audit Trio](#the-monitoringaudit-trio)
- [Event-Driven / Integration Services](#event-driven--integration-services)
- [Supplementary Networking, Security & Storage Q&A](#supplementary-networking-security--storage-qa)
- [Do You Need to Know How to Code for All of This?](#do-you-need-to-know-how-to-code-for-all-of-this)

---

## Dev / CLI Tools

![[Sources/ScreenShot_2026-08-20_103601_343.png]]
*AWS Management Console home page overview: EC2/IAM/Cloud9/S3/VPC/CloudFront/CloudFormation/RDS/Elastic Beanstalk and other common services can all be reached directly from "Recently visited" here.*

**AWS CloudShell** — A command-line terminal you use directly in the browser. Log into the console, click the icon, and it's ready — pre-installed with the AWS CLI and common tools, no environment setup required. Example: running a few quick `aws s3 ls` commands without wanting to install the CLI on your own machine.

**AWS CLI** — A tool for operating AWS from your own terminal using commands. Once installed and configured with an access key, you can run `aws ec2 describe-instances` instead of clicking through the console.

**AWS Cloud9** — A cloud-based IDE in your browser, with its own terminal and debugging tools. The interface (browser editor) and the compute resource (the machine actually running your code) are two separate things:
- Cloud9 can automatically spin up an **EC2** instance in the background for you, and your code actually runs on that EC2 — **that EC2 is billed at normal EC2 rates**; the Cloud9 interface itself doesn't cost extra. Remember to stop the EC2 (or set auto-hibernation) when you're done, or it keeps billing.
- You can also connect it to an existing local/other machine and let the Cloud9 interface operate that machine instead.

## Identity and Permissions

**IAM** — Manages "who can access what." A **Key** is the credential pair used for programmatic access (access key ID + secret access key); a **Policy** is a JSON-formatted permission rule file attached to users/groups/roles to take effect.

**ARN (Amazon Resource Name)** — Every AWS resource's unique "ID number," formatted like `arn:aws:s3:::my-bucket/photo.jpg`. Used in IAM policies to precisely specify which resource a rule governs.

**AWS Account ID** — A 12-digit number, the unique identifier for each AWS account.

![[Sources/ScreenShot_2026-08-20_112109_365.png]]
*AWS Account Root User: root account privileges can't be deleted and can't be restricted with an IAM policy — they can only be constrained via an Organizations SCP. There can only be one root user per account.*

**AWS Access Key** — A credential file stored on your local machine, typically at `~/.aws/credentials` (INI format), read by the CLI/SDK for authentication. **Never commit it to git or share it with anyone** — if it leaks, someone else can use it to run resources on your account and rack up your bill.

![[Sources/ScreenShot_2026-08-20_105840_248.png]]
![[Sources/ScreenShot_2026-08-20_105915_686.png]]
![[Sources/ScreenShot_2026-08-20_105943_789.png]]
![[Sources/ScreenShot_2026-08-20_110025_534.png]]
*Access key generation flow: create it in the IAM console → it gets stored in `~/.aws/credentials` (TOML/INI format) → you can use `[default]` plus custom profile names to distinguish multiple credential sets → the `aws configure` command can write directly into this file.*

## Infrastructure as Code (IaC)

![[Sources/ScreenShot_2026-08-20_104944_197.png]]
*CFN (declarative — what you see is what you get) vs. CDK (imperative — say what you want and the rest gets filled in) compared.*

**CloudFormation** — Describes "what resources I want" using a YAML/JSON template; AWS reads the template and automatically creates/updates/deletes resources — no need to click through the console manually.

![[Sources/ScreenShot_2026-08-20_105012_543.png]]
*A real CloudFormation YAML snippet: defining an EC2 instance, using `Fn::FindInMap` to look up the AMI ID by Region, and attaching a security group and subnet.*

**CDK (Cloud Development Kit)** — Defines infrastructure using an actual programming language (Python/Node.js/TypeScript, etc.). Deployment happens in two steps:
1. **`cdk synth`** (local): **translates** your code into a CloudFormation template file — this step never touches AWS.
2. **`cdk deploy`**: submits the generated template to the CloudFormation service, which reads it and actually creates the resources.

The full chain: **write Python code → CDK translates it into a CloudFormation template → CloudFormation reads the template and creates resources**. CDK just saves you from hand-writing YAML — under the hood, it's still CloudFormation doing the work.

## Service Models (Cloud Responsibility Split)
- **IaaS**: Only the infrastructure is provided (VM/network/storage); you manage everything from the OS up. Example: EC2
- **PaaS**: The runtime environment is managed for you too; you only upload code. Example: Elastic Beanstalk
- **FaaS**: You only write a function; you never see a server; billed per invocation. Example: Lambda
- **SaaS**: A ready-made software product; you just log in and use it. Example: Gmail, Zoom

![[Sources/ScreenShot_2026-08-20_110236_126.png]]
*Under IaaS/PaaS/SaaS, the dividing line between "customer responsible" (light) and "AWS responsible" (dark) — the further down the line moves, the more AWS manages.*

![[Sources/ScreenShot_2026-08-20_110359_857.png]]
*Using compute as the worked example: which AWS service corresponds to each of IaaS/PaaS/SaaS/FaaS, and exactly what the customer is responsible for in each.*

![[Sources/ScreenShot_2026-08-20_110521_535.png]]
*The general rule of thumb for the Shared Responsibility Model: anything you can configure/store is "security IN the cloud" (your responsibility); anything you can't configure is "security OF the cloud" (AWS's responsibility).*

## Storage and Networking

![[Sources/ScreenShot_2026-08-20_110926_883.png]]
*Additional storage services: the Snow Family (Snowball Edge/Snowmobile/Snowcone — physical hardware for moving large amounts of data), AWS Backup (unified backup management across EC2/EBS/RDS/DynamoDB/EFS), CloudEndure (disaster-recovery replication), Amazon FSx (a high-performance file system supporting Windows' SMB or Linux's Lustre protocol).*

**S3** — Object storage for files (images/video/backups/static websites).

**S3 storage-class tiers** (the same data can be placed in different tiers by access frequency to save money):
- **S3 Standard** — Frequently accessed, most expensive
- **S3 Standard-IA** — Infrequently accessed, cheap storage, billed on retrieval
- **S3 One Zone-IA** — Stored in only one AZ, even cheaper but with one less layer of disaster resilience (lose that AZ, lose the data)
- **S3 Glacier / Glacier Deep Archive** — Archival storage, extremely cheap but retrieval takes time (hours to days), suited to long-term backups
- **S3 Lifecycle Policy** — Automated rules that migrate old data to cheaper tiers over time (e.g., auto-move to IA after 30 days, to Glacier after 90)

**EFS (Elastic File System)** — A network file system that **multiple EC2 instances can mount and read/write simultaneously** (analogous to a shared Docker volume — multiple containers mounting the same volume, where a file written by one is instantly readable by the others; EFS is essentially "a network-based shared volume for multiple EC2 instances" — same idea, just applied across multiple machines instead of multiple containers on one machine). S3 is not a file system, and EBS is dedicated to a single EC2 instance — different positioning from EFS's multi-machine sharing.

**CloudFront** — A CDN that caches content at global edge locations for faster nearby access. Often paired with S3: static site assets/images live in S3, CloudFront accelerates global delivery.

**VPC** — A private virtual network you can customize with your own subnets/route tables/security groups. **Inbound** controls whether external traffic can come in; **Outbound** controls whether internal traffic can go out.
- **Subnet**: Public Subnet (directly internet-accessible) vs. Private Subnet (not, typically used for things like databases that shouldn't be exposed)
- **Internet Gateway** — The "door" that connects a VPC to the internet
- **Route Table** — Decides where traffic should go

![[Sources/ScreenShot_2026-08-20_111657_005.png]]
*Full VPC network architecture diagram: Internet → IGW → Router → Route Table/NACL → Public Subnet (EC2, Security Group) / Private Subnet (RDS), with NAT letting the private subnet reach the internet outbound.*

**Security Group vs. NACL** (two firewalls at different granularities):
| | Security Group | NACL |
|---|---|---|
| Scope | Instance level | Subnet level |
| Rule type | "Allow" only | Can "Allow" or "Deny" |
| State | Stateful (return traffic for an allowed inbound connection is automatically permitted) | Stateless (inbound and outbound must be configured separately) |

Memory aid: a Security Group is like a doorman who only checks people coming in (default deny-all, only what you allow gets through); a NACL is like a perimeter checkpoint — it checks both in and out, and can actively blacklist.

![[Sources/ScreenShot_2026-08-20_111726_902.png]]
*A diagram of NACLs blocking traffic at the subnet level: you can set an explicit Deny rule for a specific IP (e.g., "block a known-abuse IP"); Security Groups sit inside the NACL as a second, instance-level gate.*

**Auto Scaling + ELB**:
- **ELB (Elastic Load Balancer)** — distributes traffic across multiple EC2 instances, preventing any single point from being overloaded
- **Auto Scaling** — automatically increases/decreases EC2 instance count based on traffic metrics
Common scenario: fluctuating traffic that needs to automatically handle peaks while saving cost during quiet periods — the two are usually used together (ELB spreads the traffic, Auto Scaling decides how many machines to spread it across).

## Databases

**RDS** — Managed relational database, supports engines like MySQL/PostgreSQL/SQL Server; AWS handles backups/patching/failover.
**Aurora** — AWS's own relational database, compatible with the MySQL/PostgreSQL protocols but with better performance — the "premium" tier of the RDS family.
**Redshift** — A data warehouse purpose-built for large-scale analytical queries (not day-to-day CRUD), with a dedicated Query Editor for writing SQL directly.

![[Sources/ScreenShot_2026-08-20_111350_924.png]]
*The RDS/Aurora console home page: you can choose "Express configuration" to get a pre-configured database running in seconds, or "Full configuration" to customize every detail.*

![[Sources/ScreenShot_2026-08-20_111359_258.png]]
*The engine-selection screen when creating a database: Aurora (MySQL/PostgreSQL compatible), MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, and IBM Db2 are all options.*

## Compute

![[Sources/ScreenShot_2026-08-20_110137_409.png]]
*AWS's official documentation home page (using EC2 as the example): each service's docs generally include a User Guide, Instance Types, and topic-specific feature guides — when you can't remember a detail, just check docs.aws.amazon.com.*

**AMI (Amazon Machine Image)** — EC2's "image template," a snapshot containing the OS plus pre-installed software. Example: configure one EC2 instance, package it as an AMI, then spin up many identical servers from that AMI later without reinstalling everything each time.

![[Sources/ScreenShot_2026-08-20_110557_788.png]]
*The full compute-services family: LightSail (a simplified, beginner-friendly version of EC2), ECS/ECR/Fargate (container orchestration + image registry + serverless running), EKS (managed Kubernetes), Lambda (serverless functions).*

**AWS Elastic Beanstalk (PaaS)** — Think of it as an automated version of manually deploying with Nginx yourself: a normal manual deployment requires (1) spinning up a server, (2) installing Nginx as a reverse proxy/static file server, (3) installing an application runtime (Gunicorn/PM2, etc.), with Nginx forwarding requests to it, (4) configuring startup-on-boot/logging/monitoring, and (5) if you need to scale, manually adding machines and configuring a load balancer. **Beanstalk automates this entire pipeline** — you pick a platform (e.g. "Python"), upload your code, and Beanstalk automatically configures the runtime environment + load balancer + Auto Scaling. Note: under the hood it's still EC2 running your app — it's just that this layer of configuration/scaling is handled by AWS, and you never touch it directly. The difference from plain EC2: EC2 gives you "a blank VM, you install everything yourself" (IaaS); Beanstalk gives you "you only manage the application code, AWS sets up the runtime layer" (PaaS).

**Reserved Instances vs. Savings Plans** (both are "commit money now for a discount," but with different flexibility):
| | Reserved Instances | Savings Plans |
|---|---|---|
| Commitment type | Commits to a **specific instance type + Region** (e.g. "use m5.large in Sydney for 1 year") | Commits to **how much you'll spend per hour** (e.g. "$10/hour for 1 year"), without locking to a specific instance type |
| Flexibility | Low — switching instance type/Region generally means repurchasing | High — as long as total spend matches the committed amount, you can switch instance type/Region/even switch to Lambda/Fargate mid-term and the discount still applies |
| Coverage | Mostly EC2 (RDS/ElastiCache, etc. each have their own RI) | EC2 + Lambda + Fargate can all be covered by the same Savings Plan |

In one line: **an RI is "reserving one specific model of car for a year"; a Savings Plan is "committing to spend at least $500/month on rides, no matter what car you take, it all counts toward that amount."** The latter is more flexible — AWS has increasingly recommended Savings Plans over RIs in recent years (unless you're very confident your instance type/Region won't change at all for the next 1–3 years).

![[Sources/ScreenShot_2026-08-20_111828_309.png]]
*EC2 instance-size comparison: within the same family (t2), going from small to large roughly doubles vCPU/memory/price each step — a pattern worth internalizing when choosing a size.*

![[Sources/ScreenShot_2026-08-20_111946_771.png]]
*An overview of the five EC2 payment options: On-Demand (most flexible, most expensive), Spot (cheapest, up to 90% off but can be reclaimed), Reserved (commit for 1/3 years, up to 75% off), Dedicated (dedicated physical hardware).*

![[Sources/ScreenShot_2026-08-20_112012_987.png]]
*Reserved Instances explained in detail: the discount is jointly determined by Term (length) × Class (Standard/Convertible) × Payment Option (upfront percentage) — the longer the term, the higher the upfront payment, the lower the flexibility, and the bigger the discount.*

![[Sources/ScreenShot_2026-08-20_112036_007.png]]
*Standard RI vs. Convertible RI: Standard can't change its configuration but can be resold on the RI Marketplace; Convertible can change instance type/platform but can't be sold on the marketplace — it can only be exchanged with AWS.*

**Amazon ECS/EKS/Fargate (why container orchestration is needed)** — Running containers in production raises a bunch of problems: which machine should a container run on, how does it auto-restart on a crash, how does it scale when traffic spikes, how do updates happen without downtime — these are collectively called "container orchestration," and both ECS and EKS solve exactly this.
- **ECS**: A proprietary orchestration system AWS invented itself, usable only within AWS, not open source.
- **EKS**: The underlying technology wasn't invented by AWS — it's **Kubernetes** (an open-source container-orchestration standard from Google, an industry norm, portable across clouds). EKS means "AWS manages the complex operations of this open-source system for you (especially the control plane)" — you don't maintain the underlying infrastructure yourself, but the technology standard itself is open and not locked into AWS.
- **Fargate** (no official translated name, think of it as "a serverless container-running engine"): Regardless of whether you choose ECS or EKS for orchestration, the container ultimately has to run on some machine — by default, that's an EC2 instance you provision and configure yourself. Fargate hands off "that machine" to AWS too — you just tell AWS how much CPU/memory the container needs, and AWS automatically finds a machine to run it on. You never see that server, and you're billed by actual container usage.

In one line: **ECS/EKS decides "how to schedule containers," Fargate decides "whose machine the container actually runs on" (answer: not your problem).**

## The Monitoring/Audit Trio

| Service | What it does | Memory hook |
|---|---|---|
| CloudWatch | Monitors performance metrics, sets alarms, views logs | Check the dashboard, set the alerts |
| CloudTrail | Records who did what and when (API call logs) | Who touched my resources |
| Config | Tracks the history of resource **configuration** changes, checks compliance | Has the configuration been changed |

These three are easy to mix up — CloudWatch is about "is performance okay," CloudTrail is about "who did the action," and Config is about "did the configuration change, and is it compliant." They answer completely different questions.

## Event-Driven / Integration Services

The SQS/SNS/EventBridge comparison, the Fanout pattern, the EventBridge-vs-Kafka analogy correction, and AppSync's Schema/Resolver explanation + code examples have all been split out into [[EN-CLF-C02 Event-Driven Services Comparison]] (per a Gardener Fission recommendation — this content forms a self-contained unit).

## Supplementary Networking, Security & Storage Q&A

**The order traffic passes through NACL and Security Group** — An external request reaching an EC2 instance must pass through two gates in sequence: ①NACL (the subnet's front gate) → ②Security Group (the instance's inner door) → EC2. If ① denies it, the traffic is dropped immediately — the Security Group never even sees the request. Only if ① allows it does it move on to ② to decide whether to let it through. Common mistakes: NACL rule numbers being ordered so a different rule matches first, inbound/outbound direction configured backwards, or editing the NACL attached to the wrong subnet (a NACL attaches to a subnet, not to an EC2 instance).

**What are port numbers** — Think of them as "room numbers" in a server (a building): 80 = HTTP, 443 = HTTPS, 22 = SSH, 3306 = MySQL.

**The exam point behind "Security Group only has an inbound rule, but the outbound response still works"** — A Security Group is stateful: once an inbound rule allows a connection, it remembers that connection, and the corresponding return traffic is automatically allowed — no extra outbound rule needed. A NACL is stateless, so inbound and outbound traffic must each be configured separately.

**When exactly is Redshift used** — The core distinction: RDS/DynamoDB handle OLTP (real-time business-system reads/writes), while Redshift handles OLAP (large-scale historical data analysis). Typical scenarios: BI reporting, a data warehouse aggregating data from multiple systems for analysis, pairing with QuickSight/Tableau for visualization, large-scale log analysis. The underlying reason: RDS uses row-based storage, suited to reading/updating a whole record; Redshift uses columnar storage, suited to scanning only a few columns for aggregation — much more efficient for that use case. Many companies use RDS and Redshift together: RDS runs the real-time business, Redshift periodically syncs data for analytical reporting.

**Is AWS Auto Scaling its own standalone service** — Two layers exist: individual services already have their own independent scaling mechanisms (EC2 Auto Scaling, DynamoDB Auto Scaling, ECS Service Auto Scaling, Aurora Auto Scaling); "AWS Auto Scaling" (the capitalized, full-name service) is a later-introduced unified management dashboard — it doesn't perform scaling directly itself, but calls into each service's own mechanism. CLF-C02 basically only tests the most common combination, "EC2 Auto Scaling + ELB," and doesn't dig into the distinction between the two layers.

**The setup steps for S3 + CloudFront acceleration**:
1. Upload static assets to an S3 bucket as the origin
2. Create a CloudFront Distribution, pointing to that S3 bucket as the origin
3. Configure Origin Access Control (OAC) so S3 only trusts requests coming from that CloudFront distribution, preventing users from bypassing CloudFront and hitting the S3 URL directly
4. Set up the Cache Behavior — configure what content gets cached and for how long (TTL)
5. (Optional) attach a custom domain, use ACM to get a free SSL certificate for HTTPS
6. Deploy, and wait for the configuration to propagate to global edge locations (a few minutes to twenty)
7. Verify: compare the latency of hitting the S3 URL directly vs. going through the CloudFront domain

**Is S3 file sharing possible because CloudFront is configured** — No, these are two different things: an S3 file being accessible is a matter of **permissions** (the bucket/object is publicly readable, or you use a **presigned URL** — a temporary link with an expiration time that works even while the bucket stays private; the request goes straight to S3, nothing to do with CloudFront). CloudFront solves the **speed** problem — letting global users fetch a cached copy from the nearest edge location. Analogy: sharing via S3 alone is like "the file sits in the company's headquarters archive room, and everyone has to make a trip to headquarters to see it"; S3+CloudFront is like "opening branch stores globally, with copies pre-delivered to the branch nearest you."

## Do You Need to Know How to Code for All of This?

| Service | Do you need to write code? |
|---|---|
| S3, basic EC2 usage, Cloud9 | No — point and click in the console |
| CloudFormation | Yes, you need to write a YAML/JSON template |
| CDK, Lambda | Yes, it's fundamentally programming |
| EventBridge, AppSync | Basic configuration is mostly console-based; complex logic still needs code (usually Lambda) |

**CLF-C02 only tests the conceptual level** — knowing what each service is, what problem it solves, and which scenario calls for which service. It does not require you to actually write code or operate anything hands-on.
