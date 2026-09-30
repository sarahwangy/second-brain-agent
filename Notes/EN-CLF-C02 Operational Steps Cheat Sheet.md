# CLF-C02 Operational Steps Cheat Sheet

> **Purpose**: Clarifications on a batch of high-frequency CLF-C02 concepts, plus the actual AWS console operational steps — leaning toward "how to use it" rather than "what it is." Complements [[EN-CLF-C02 Core Concepts Table]] (definitions ranked by question-bank frequency) and [[EN-CLF-C02 Core Services Q&A]] (deep conceptual explanations + analogies) — this note focuses on the operational workflow.

## Table of Contents

- [Foundational Concept Clarifications](#foundational-concept-clarifications)
- [Billing / Instance Types](#billing--instance-types)
- [Security Services](#security-services)
- [Compute / Containers](#compute--containers)
- [Networking](#networking)
- [Management / Automation](#management--automation)
- [Migration & Transfer Tools (Snowball / DataSync / DMS)](#migration--transfer-tools-snowball--datasync--dms)

---

## Foundational Concept Clarifications

**Elasticity** — Resources can scale up or down automatically based on demand, without having to guess capacity in advance. Often tested alongside Auto Scaling — Auto Scaling is the concrete mechanism that "implements elasticity" (automatically adding/removing EC2 instances based on metrics like CPU).

**Shared Responsibility Model** — AWS is responsible for the security of the cloud itself (data centers/hardware/virtualization layer); you're responsible for security inside the cloud (data/configuration/access permissions).

**Availability Zone** — Multiple physically isolated data centers within a Region, connected with low latency between AZs but isolated from each other's failures. "Deploy across multiple AZs" is the standard answer for improving availability.

**Is Amazon EBS similar to a Docker volume** — The analogy points in the right direction but the scope differs: EBS is block storage **dedicated to a single EC2 instance** (like plugging a hard drive into one computer); EFS is the one that's "shared across multiple machines" (the concept that actually maps to a shared Docker volume).

## Billing / Instance Types

**Reserved Instances (RI)** — Commit to 1 or 3 years for a cheaper unit price, suited to long-term, stable workloads.
Steps: EC2 console → Reserved Instances → Purchase Reserved Instances → choose instance type/term/payment method → confirm purchase

**Spot Instances** — Uses spare capacity, the cheapest option (up to 90% savings), but can be reclaimed at any time (2-minute warning).
Steps: when launching an EC2 instance, check "Request Spot Instances" under Purchasing option → set your maximum bid → submit

**Cost Explorer** — A retrospective/analytical tool for viewing historical spending trends.
Steps: Billing console → Cost Explorer → click Enable the first time you use it (there's roughly a 24-hour data delay) → break down and filter by Service/Region/Tag; you can also use Forecast to predict future spend

**AWS Budgets vs. Cost Explorer** — Cost Explorer is "looking in the rearview mirror" (retrospective analysis); Budgets is "setting an alarm" (a proactive tool — set a threshold and get notified automatically on overspend).
Budgets steps: Billing console → Budgets → Create budget → choose the type/set the dollar threshold/set a notification email

## Security Services

**AWS WAF** — An application-layer firewall that filters malicious HTTP/HTTPS traffic (SQL injection/XSS).
Steps: WAF console → Create web ACL → attach it to CloudFront/ALB/API Gateway → add rules (AWS-managed rule groups or custom) → deploy

**AWS Shield** — DDoS protection. Standard is free and enabled automatically; Advanced is paid, offering stronger protection + expert support.
Steps: Standard requires no configuration; subscribe to Advanced in the Shield console, then attach it to resources like ALB/CloudFront/Route 53

**Amazon GuardDuty** — Uses machine learning to continuously monitor for suspicious activity (anomalous API calls/malicious IPs).
Steps: GuardDuty console → click Enable GuardDuty (one-click activation, automatically analyzes CloudTrail/VPC Flow Logs/DNS logs) → view findings in the Findings list, sorted by severity

**Does encryption mean KMS or S3** — They're not the same thing, they work together: KMS manages the encryption **keys** themselves; the encryption toggle in services like S3/RDS/EBS "uses" a key provided by KMS to encrypt the data.
S3 steps: select the bucket in the console → Properties → Default encryption → choose SSE-S3 (AWS manages the key) or SSE-KMS (uses a key you created in KMS yourself, with more granular permission control)

## Compute / Containers

**Amazon ECS/EKS/Fargate** — ECS is AWS's own container orchestrator; EKS is AWS-managed Kubernetes; Fargate is a **running mode** (not an orchestrator) — both ECS and EKS can choose to run on Fargate, so you don't have to manage the underlying EC2 instances yourself.
Steps (ECS + Fargate): Create Cluster (choose the Fargate type) → define a Task Definition (container image + CPU/memory) → Create Service (how many instances to run + attach a load balancer)

**Is AWS Lambda a FaaS, and what does the syntax look like** — Yes, Lambda is the poster child for FaaS.
Steps: Create function → choose a runtime (Python/Node.js, etc.) → write the handler:
```python
def lambda_handler(event, context):
    # event: the data that triggered this; context: runtime info
    return {'statusCode': 200, 'body': 'Hello from Lambda'}
```
The function name is fixed as `lambda_handler` (or a custom name you specify), and the two parameters are always `event` and `context`. You can attach triggers (S3/API Gateway/EventBridge, etc.) to invoke it automatically.

## Networking

**AWS Direct Connect** — A dedicated physical network connection from an on-prem enterprise data center to AWS, bypassing the public internet, with low latency and stable bandwidth.
Steps: contact AWS or a partner to physically wire a connection to a Direct Connect Location (takes several weeks) → create a Virtual Interface (VIF) in the console to configure routing → a dedicated channel is established between your on-prem network and your VPC. **This doesn't take effect with a few console clicks — it requires physical deployment.**

## Management / Automation

**AWS Organizations** — Centrally manages multiple accounts (consolidated billing + unified permission boundaries).
Steps: Create organization → invite accounts to join (or create new ones) → group them using Organizational Units (OUs) → set Service Control Policies (SCPs) to restrict which services an OU/account can use

**Does AWS Systems Manager only manage EC2** — No, it can also manage hybrid environments (on-prem servers/other-cloud machines, requires installing the SSM Agent) and non-compute resources (Parameter Store for configuration values).
Steps: install the SSM Agent on target machines (already installed on most EC2 AMIs by default) → view managed nodes in Fleet Manager → use Run Command to execute commands in bulk / Patch Manager to bulk-patch / Session Manager to SSH directly into a machine (no need to open port 22)

**AWS CloudFormation deployment steps**:
1. Write a template file (YAML/JSON) defining the resources to create
2. Create stack → upload the template → fill in parameters
3. Review and confirm → Create stack; CloudFormation creates resources automatically in dependency order, with real-time progress visible under the Events tab
4. After editing the template, choose Update stack to update; Delete stack automatically cleans up everything it created

**Amazon Redshift steps**:
1. Create cluster → choose node type/count
2. Set the database name/admin username and password
3. Configure VPC/security groups
4. Connect using the console's built-in Query Editor (or a client like DBeaver)
5. Write SQL to create tables — a common approach is using the `COPY` command to bulk-import data from S3, then run analytical queries

## Migration & Transfer Tools (Snowball / DataSync / DMS)

| Service | Transfer method | Ships physical hardware? | Requires code? | Best suited for |
|---|---|---|---|---|
| Snowball | Offline physical device transport | Yes (AWS ships it to you, you ship it back) | No — just use the client software to copy files | Massive data volumes (TB to PB scale), poor network conditions |
| DataSync | Online network sync (via an installed Agent) | No | No — configure the task in the console | Continuous/periodic file synchronization |
| DMS (Database Migration Service) | Online network migration | No | No — configure the migration task in the console, supports CDC for continuous replication | Database migration requiring minimal downtime |

Memory hook: only the **"Snow"-prefixed services** (Snowball, Snowmobile, Snowcone) involve shipping physical hardware — every other migration service is a pure software/network solution. (Merged in from [[EN-CLF-C02 Core Services Q&A]] per a Gardener Fission recommendation — this content leans "how to use it," a better fit for this note's focus.)
