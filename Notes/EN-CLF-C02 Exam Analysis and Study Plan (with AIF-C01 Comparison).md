# CLF-C02 Exam Analysis and Study Plan (with AIF-C01 Comparison)

> Background: while studying for AIF-C01, I wanted to assess how much of that material would carry over if I later decided to take CLF-C02. (Merged from two notes that separately discussed the same topic: the 08.16 comparison analysis + the 08.20 exam-syllabus analysis.)

## Table of Contents

- [Conclusion](#conclusion)
- [Folder Contents](#folder-contents)
- [CLF-C02 Exam Basics](#clf-c02-exam-basics)
- [Comparison with AIF-C01 Knowledge: How Much Carries Over](#comparison-with-aif-c01-knowledge-how-much-carries-over)
- [What CLF-C02 Requires Additionally](#what-clf-c02-requires-additionally)
- [How to Prepare](#how-to-prepare)
- [Reference Resources](#reference-resources)
- [One-Line Summary](#one-line-summary)

---

## Conclusion

Some of it carries over (roughly 20–30%), but not enough — there's still a lot of new material to cover. The two certifications are positioned differently:

- **AIF-C01**: AI/ML-specialized — understanding AI concepts + AWS AI services
- **CLF-C02 (Cloud Practitioner)**: AWS's overall foundational certification — understanding what cloud computing is + AWS's overall architecture + billing/security/support systems. Almost unrelated to AI; it's a broader "AWS 101" requirement.

## Folder Contents

- 4 PDFs: `_without_answer` (questions only, 719 questions), `_without_discussion`, `_with_discussion` (with community discussion/answers), `_aizh` (Chinese-English bilingual version)
- Actual count for the `_without_answer` PDF: **219 pages, 719 questions** (numbered 1–719, an even larger bank than AIF-C01's 452 questions)

## CLF-C02 Exam Basics

| Domain | Area | Weight |
|---|---|---|
| Domain 1 | Cloud Concepts | **24%** |
| Domain 2 | Security and Compliance | **30%** (second-highest weight) |
| Domain 3 | Cloud Technology and Services | **34%** (highest weight) |
| Domain 4 | Billing, Pricing, and Support | **12%** (lowest weight) |

**Exam format**: 65 questions (50 scored + 15 unscored, mixed together so you can't tell which don't count), 90 minutes, pass mark is 700/1000 — structurally identical to the AIF-C01 exam.

## Comparison with AIF-C01 Knowledge: How Much Carries Over

**The easy wins (roughly 20–30%)** — concentrated mainly in **Domain 2 (Security & Compliance, 30% weight) — almost no need to re-study**:
- The Shared Responsibility Model
- IAM, KMS, Secrets Manager, Macie, Inspector
- Config, CloudTrail, Trusted Advisor, Artifact, Audit Manager, the Well-Architected Tool
- ISO/SOC compliance standards, PII, data encryption (at rest + in transit)
- The names of the six Well-Architected Framework pillars — AIF-C01 mentioned these, CLF-C02 goes deeper, but the memorized framework carries over directly

**Data infrastructure**: basic concepts for general-purpose services like S3, EC2, VPC, CloudFront are tested on both
**Cost-management tools**: AWS Budgets, Cost Explorer

## What CLF-C02 Requires Additionally

**Material that has to be learned from scratch (roughly 70%, entirely untouched by AIF-C01)**:

**Domain 1 (Cloud Concepts, 24%) — entirely new material**
- The six advantages of cloud computing: trading CapEx for OpEx, economies of scale, no more guessing capacity, increased speed and agility, no data-center build-out costs, going global in minutes
- **AWS global infrastructure**: the distinction and relationship between Region, Availability Zone, and Edge Location
- **The "7 R's" of migration strategy**: Rehost, Replatform, Repurchase, Refactor, Retire, Retain, Relocate — pure cloud-business concepts, entirely absent from the AI exam

**Domain 3 (Cloud Technology and Services, 34%, the highest weight) — mostly new material**
This is the largest domain in CLF-C02, requiring familiarity with AWS's **entire catalog** of services:
- Compute: EC2 (already familiar), Lambda (touched on a little), ECS/EKS, Elastic Beanstalk
- Storage: S3 (already familiar)
- Databases: RDS (hadn't studied the various engines), DynamoDB (hadn't studied at all)
- Networking: VPC (touched on a little — subnets/route tables/NAT gateways/Direct Connect/VPN details hadn't been studied), Route 53 (hadn't studied at all)
- AWS Organizations, multi-account management

**Domain 4 (Billing, Pricing, and Support, 12%) — entirely new material**
- **Detailed billing models**: the differences and use cases for On-Demand, Reserved Instances, Savings Plans, and Spot Instances
- **The four AWS Support Plan tiers**: Basic (free), Developer (from $29/month), Business (from $100/month), Enterprise (from $15,000/month)
- Pricing tools: Pricing Calculator, Cost Explorer
- Billing-related concepts

## How to Prepare

1. **Skip what doesn't need re-studying**: the Domain 2 security/compliance concepts are already well internalized from AIF-C01 — just skim the memorized framework before the exam, don't waste time re-reading in detail
2. **Domain 3 is the main battleground** (highest weight + most new content): go through it "by service category" — Compute (EC2/Lambda/ECS) → Storage (S3) → Databases (RDS/DynamoDB) → Networking (VPC/Route 53) → Management (Organizations). For each category, it's enough to remember "what it is, what problem it solves, and how it differs from similar services" — no need to dig into hands-on operational detail
3. **Domain 1 and Domain 4 have less content but it's very specific**: the six cloud-computing advantages, the 7 R's migration strategy, the four support-plan tiers, the various billing models — these lean toward memorization-type knowledge, best organized into tables and memorized directly, without needing to understand deep underlying principles
4. **Practice-question pacing**: the question bank has 719 questions, even bigger than AIF-C01's 452, but the content is "broad but shallow" — individual question difficulty is generally lower than the AI-specialized exam. Allocate practice volume by Domain weight — do more for Domain 3 (more new content, highest weight), less for Domain 2 (mostly already known)
5. **Estimated study time**: roughly 1–2 weeks overall to be exam-ready — easier than AIF-C01, but not passable by walking in cold. The specific service names/use cases in Domain 3 still need to be gone through properly
6. **Concrete resource recommendations**: use the free AWS Skill Builder course "Cloud Practitioner Essentials" to build a foundation; for practice questions, consider Stephane Maarek's or Tutorials Dojo's (Jon Bonso's) question banks on Udemy (focus on reading the explanations, not just right/wrong); if possible, hands-on practice creating an EC2/S3/IAM user in the Free Tier speeds up understanding; before the exam, time yourself with the official Practice Exam (90 minutes, 65 questions) — **only sit the real exam once your accuracy is consistently above 80%**

**Priority recommendation**: don't study both certifications at once — finish AIF-C01 first (already heavily invested in it), and treat CLF-C02 as a follow-up. When the time comes, use this outline plus the 719-question bank to tackle it in one focused push, directly reusing the time saved on Domain 2 to cover Domains 1/3/4.

## Reference Resources
- [[EN-Video Resource | Andrew Brown's Full CLF-C02 Course]] — a 14-hour free video course covering all four Domains, leaning heavily on hands-on demos

## One-Line Summary

**The security/compliance portion (Domain 2, 30% weight) is basically a freebie; the remaining 70% of the weight (cloud concepts + cloud technology/services + billing) is all new material requiring systematic study from scratch** — especially Domain 3, which carries the highest weight but is also the most varied, covering almost every category of AWS service, with little relation to AI. Given that CLF-C02 is more "broad but shallow," overall study time is estimated at 1–2 weeks — easier than AIF-C01, but not the kind of exam you can pass by walking in without preparation.
