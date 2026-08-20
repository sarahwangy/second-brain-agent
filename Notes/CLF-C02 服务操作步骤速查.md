# CLF-C02 服务操作步骤速查

> **Purpose**: CLF-C02 备考中一批高频概念的澄清 + 实际 AWS 控制台操作步骤，偏"怎么用"而不是"是什么"。跟 [[08.20-CLF-C02-核心概念表]]（按题库频率排的定义）、[[CLF-C02 核心服务讲解问答]]（概念深度讲解+类比）互补，这份专注操作流程。

## 目录

- [基础概念澄清](#基础概念澄清)
- [计费/实例类型](#计费实例类型)
- [安全类服务](#安全类服务)
- [计算/容器](#计算容器)
- [网络](#网络)
- [管理/自动化](#管理自动化)

---

## 基础概念澄清

**Elasticity（弹性）** — 资源能根据需求自动增减，不用提前猜容量。常跟 Auto Scaling 一起考——Auto Scaling 是"实现弹性"的具体机制（根据CPU等指标自动加/减EC2实例数）。

**Shared Responsibility Model（责任共担模型）** — AWS负责云本身安全（机房/硬件/虚拟化层），你负责云里面安全（数据/配置/访问权限）。

**Availability Zone（可用区）** — 一个Region内多个物理隔离的数据中心，AZ间低延迟连接但故障隔离。"跨AZ部署"是提升可用性的标准答案。

**Amazon EBS 是否类似Docker volume** — 类比方向对但范围不同：EBS是**单台EC2专属**的块存储（像单台电脑插一块硬盘）；EFS才是"多台机器共享"的（对应共享Docker volume的概念）。

## 计费/实例类型

**Reserved Instances（预留实例）** — 承诺用1/3年换更便宜单价，适合长期稳定负载。
操作：EC2控制台 → Reserved Instances → Purchase Reserved Instances → 选实例类型/期限/付款方式 → 确认购买

**Spot Instances（竞价实例）** — 用闲置容量，最便宜（省最多90%），可能被随时回收（提前2分钟通知）。
操作：启动EC2时 Purchasing option 勾 "Request Spot Instances" → 设最高出价 → 提交

**Cost Explorer** — 回顾/分析型工具，看历史花费趋势。
操作：Billing控制台 → Cost Explorer → 首次用点 Enable（有约24小时数据延迟）→ 按Service/Region/Tag拆解筛选，也能用Forecast预测未来花费

**AWS Budgets vs Cost Explorer** — Cost Explorer是"看后视镜"（回顾分析），Budgets是"设警报器"（预警型，设阈值超支自动通知）。
Budgets操作：Billing控制台 → Budgets → Create budget → 选类型/设金额阈值/设通知邮箱

## 安全类服务

**AWS WAF** — 应用层防火墙，过滤恶意HTTP/HTTPS流量（SQL注入/XSS）。
操作：WAF控制台 → Create web ACL → 关联CloudFront/ALB/API Gateway → 添加规则（AWS托管规则组或自定义）→ 部署

**AWS Shield** — DDoS防护。Standard免费自动启用；Advanced付费，提供更强防护+专家支持。
操作：Standard不用配置；Advanced在Shield控制台订阅后关联ALB/CloudFront/Route53等资源

**Amazon GuardDuty** — 机器学习持续监控可疑活动（异常API调用/恶意IP）。
操作：GuardDuty控制台 → 点Enable GuardDuty（一键开启，自动分析CloudTrail/VPC Flow Logs/DNS日志）→ Findings列表按严重程度查看发现

**Encryption 是指 KMS 还是 S3** — 不是一回事，是配合关系：KMS管理加密**密钥**本身；S3/RDS/EBS等服务的加密开关是"使用"KMS提供的密钥加密数据。
S3操作：控制台选桶 → Properties → Default encryption → 选SSE-S3（AWS自管密钥）或SSE-KMS（用自己在KMS建的密钥，权限控制更细）

## 计算/容器

**Amazon ECS/EKS/Fargate** — ECS是AWS自家容器编排；EKS是AWS托管Kubernetes；Fargate是**运行方式**（不是编排器），ECS/EKS都可选Fargate运行，不用自己管底层EC2。
操作（ECS+Fargate）：Create Cluster（选Fargate类型）→ 定义Task Definition（容器镜像+CPU/内存）→ Create Service（跑几个实例+关联负载均衡）

**AWS Lambda 是FaaS吗，语法怎么写** — 是，Lambda是FaaS代表服务。
操作：Create function → 选运行时（Python/Node.js等）→ 写handler：
```python
def lambda_handler(event, context):
    # event: 触发数据；context: 运行时信息
    return {'statusCode': 200, 'body': 'Hello from Lambda'}
```
函数名固定`lambda_handler`（或自定义指定），两个参数固定`event`和`context`。可关联触发器（S3/API Gateway/EventBridge等）自动调用。

## 网络

**AWS Direct Connect** — 企业本地到AWS的专用物理网络连接，不走公共互联网，延迟低带宽稳。
操作：联系AWS或合作伙伴物理布线到Direct Connect Location（需数周）→ 控制台创建Virtual Interface(VIF)配置路由 → 本地网络与VPC间建立专线通道。**不是控制台点几下就生效，需要物理部署**。

## 管理/自动化

**AWS Organizations** — 集中管理多账户（合并账单+统一权限边界）。
操作：Create organization → Invite账户加入（或创建新账户）→ 用Organizational Units(OU)分组 → 设置Service Control Policies(SCP)限制OU/账户可用服务

**AWS Systems Manager 是否只管EC2** — 不止，也能管混合环境（本地服务器/其他云机器，需装SSM Agent）和非计算资源（Parameter Store存配置参数）。
操作：目标机器装SSM Agent（EC2默认已装大部分AMI）→ Fleet Manager查看受管节点 → Run Command批量执行命令 / Patch Manager批量打补丁 / Session Manager直接SSH进机器（不用开22端口）

**AWS CloudFormation 部署步骤**：
1. 写模板文件（YAML/JSON），定义要创建的资源
2. Create stack → 上传模板 → 填参数
3. Review确认 → Create stack，CloudFormation按依赖顺序自动创建资源，Events标签页实时看进度
4. 改模板后选Update stack更新；Delete stack自动清理所有创建过的资源

**Amazon Redshift 步骤**：
1. Create cluster → 选节点类型/数量
2. 设置数据库名/管理员账号密码
3. 配置VPC/安全组
4. 用控制台内置Query Editor（或DBeaver等客户端）连接
5. 写SQL建表，常见方式用`COPY`命令从S3批量导入数据，再跑分析查询
