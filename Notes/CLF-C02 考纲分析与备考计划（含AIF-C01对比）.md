# CLF-C02 考纲分析与备考计划（含AIF-C01对比）

> 讨论背景：AIF-C01学习期间，评估以后想考CLF-C02时，AIF-C01学到的内容能不能直接复用。（合并自两份重复讨论同一话题的笔记：08.16的对比分析 + 08.20的考纲分析）

## 目录

- [结论](#结论)
- [文件夹内容](#文件夹内容)
- [CLF-C02 考试基本信息](#clf-c02-考试基本信息)
- [跟AIF-C01知识对比：能复用多少](#跟aif-c01知识对比能复用多少)
- [CLF-C02需要额外补的内容](#clf-c02需要额外补的内容)
- [怎么准备](#怎么准备)
- [一句话总结](#一句话总结)

---

## 结论

能复用一部分（约20-30%），但不够，还需要补不少新内容。两个证书定位不一样：

- **AIF-C01**：AI/ML专项，懂AI概念+懂AWS AI服务
- **CLF-C02（Cloud Practitioner）**：AWS全局基础认证，懂云计算是什么+懂AWS整体架构+懂计费/安全/支持体系，跟AI几乎无关，是更广泛的"AWS入门必修课"

## 文件夹内容

- 4份PDF：`_without_answer`（纯题目，719题）、`_without_discussion`、`_with_discussion`（带社区讨论/答案）、`_aizh`（中英对照版）
- `_without_answer`这份PDF实际统计：**219页，719道题**（题号1-719，比AIF-C01那份452题的题库还大）

## CLF-C02 考试基本信息

| Domain | 领域 | 权重 |
|---|---|---|
| Domain 1 | Cloud Concepts（云概念） | **24%** |
| Domain 2 | Security and Compliance（安全与合规） | **30%**（权重仅次于Domain 3） |
| Domain 3 | Cloud Technology and Services（云技术与服务） | **34%**（权重最高） |
| Domain 4 | Billing, Pricing, and Support（计费、定价、支持） | **12%**（权重最低） |

**考试形式**：65道题（50道计分+15道不计分，混在一起分不出哪些不算分），90分钟，700/1000分及格——跟AIF-C01的考试结构完全一样。

## 跟AIF-C01知识对比：能复用多少

**能白捡的部分（约20-30%）**——主要集中在**Domain 2（安全合规，30%权重）——几乎不用重学**：
- 责任共担模型（Shared Responsibility Model）
- IAM、KMS、Secrets Manager、Macie、Inspector
- Config、CloudTrail、Trusted Advisor、Artifact、Audit Manager、Well-Architected Tool
- ISO/SOC合规标准、PII、数据加密（静态+传输）
- Well-Architected Framework六大支柱的名字——AIF-C01里提过，CLF-C02会考更细，可以直接复用记忆框架

**数据基础设施**：S3、EC2、VPC、CloudFront这些通用服务的基本概念，两边都会考
**成本管理工具**：AWS Budgets、Cost Explorer

## CLF-C02需要额外补的内容

**必须从头学的部分（约70%，AIF-C01完全没碰过）**：

**Domain 1（云概念，24%）——全新内容**
- 云计算六大优势：用OpEx代替CapEx、规模经济、不用猜容量、提升速度敏捷性、不用花钱建数据中心、几分钟内实现全球部署
- **AWS全球基础设施**：Region（区域）、Availability Zone（可用区）、Edge Location（边缘节点）的区别和关系
- **迁移策略"7个R"**：Rehost、Replatform、Repurchase、Refactor、Retire、Retain、Relocate——纯云计算商业概念，AI考试完全不涉及

**Domain 3（云技术与服务，34%，权重最高）——大部分是新内容**
这是CLF-C02里占比最大的领域，需要认识AWS**全品类**服务：
- 计算：EC2（已熟悉）、Lambda（碰过一点点）、ECS/EKS、Elastic Beanstalk
- 存储：S3（已熟悉）
- 数据库：RDS（各引擎种类没学过）、DynamoDB（没学过）
- 网络：VPC（碰过一点点，子网/路由表/NAT网关/Direct Connect/VPN这些细节没学过）、Route53（没学过）
- AWS Organizations、多账户管理

**Domain 4（计费、定价、支持，12%）——完全新内容**
- **详细计费模式**：On-Demand、Reserved Instances、Savings Plans、Spot Instances这些定价策略的区别和适用场景
- **AWS支持计划四个等级**：Basic（免费）、Developer（从29美元/月）、Business（从100美元/月）、Enterprise（从15000美元/月起）
- 定价工具：Pricing Calculator、Cost Explorer
- 账单相关概念

## 怎么准备

1. **不用重学的部分直接跳过**：Domain 2那些安全合规概念，AIF-C01已经吃得很透，考前扫一眼记忆框架就行，别浪费时间重新细看
2. **Domain 3是重点攻坚区**（权重最高+全新内容最多）：按"服务分类"过一遍——计算(EC2/Lambda/ECS)→存储(S3)→数据库(RDS/DynamoDB)→网络(VPC/Route53)→管理(Organizations)，每类服务记住"是什么、解决什么问题、跟同类服务的区别"就够，不用深究实操细节
3. **Domain 1和Domain 4内容不多但很具体**：云计算六大优势、7个R迁移策略、四档支持计划、几种计费模式——这些偏"背诵型"知识点，建议整理成表格死记，不需要理解太深的原理
4. **刷题节奏**：题库719题比AIF-C01的452题还大，但内容"广而浅"，单题难度通常比AI专项题目低。按Domain权重分配刷题量——Domain 3多刷（新内容多+占比高），Domain 2少刷（基本会了）
5. **预估备考时间**：整体1-2周左右能过，比AIF-C01轻松，但不是裸考能过的程度，Domain 3那些具体服务名称/使用场景还是要老实过一遍

**优先级建议**：不建议同时开两条线学——先把AIF-C01考完（已经投入较多），CLF-C02作为后续计划，到时候用这份大纲+719题库集中攻一次，直接复用Domain 2省下的时间，去补Domain 1/3/4。

## 一句话总结

**安全合规那部分（Domain 2，30%权重）基本白捡；其余70%权重（云概念+云技术服务+计费）都是新内容，需要重新系统学一遍**——尤其Domain 3权重最高但也最杂，覆盖AWS几乎所有品类的服务，跟AI关系不大。考虑到CLF-C02更"广而浅"，整体备考时间预估在1-2周左右，比AIF-C01轻松，但不是"直接裸考"就能过的程度。
