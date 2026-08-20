# CLF-C02 核心服务讲解问答

> **Purpose**: CLF-C02 备考中对一批常用 AWS 服务/概念的问答式深度讲解，包含具体例子和类比纠偏。跟 [[08.20-CLF-C02-核心概念表]]（按题库频率排的精简定义）互补——那份是速查表，这份是讲透理解的问答记录。

## 目录

- [开发/CLI 工具](#开发cli-工具)
- [身份与权限](#身份与权限)
- [基础设施即代码（IaC）](#基础设施即代码iac)
- [服务模型（云计算责任划分）](#服务模型云计算责任划分)
- [存储与网络](#存储与网络)
- [数据库](#数据库)
- [计算相关](#计算相关)
- [事件驱动/集成服务](#事件驱动集成服务)
- [是否都需要会写代码](#是否都需要会写代码)

---

## 开发/CLI 工具

**AWS CloudShell** — 浏览器里直接用的命令行终端，登录控制台点一下图标就能用，预装了 AWS CLI 和常用工具，不用自己配置环境。例：临时跑几条 `aws s3 ls` 命令，不想在自己电脑装 CLI。

**AWS CLI** — 在自己电脑终端里用命令操作 AWS 的工具，装好后配置 access key，就能用 `aws ec2 describe-instances` 代替点控制台。

**AWS Cloud9** — 浏览器里的云端 IDE，自带终端、调试工具。界面（浏览器编辑器）和计算资源（实际跑代码的机器）是分开的两件事：
- 可以让 Cloud9 自动帮你在后台开一台 **EC2**，代码实际在这台EC2上运行——**这台EC2按正常EC2价格收费**，Cloud9界面本身不额外收钱，停用记得关掉EC2或设自动休眠
- 也可以连接你已有的本地/其他机器，让Cloud9界面去操作那台机器

## 身份与权限

**IAM** — 管"谁能访问什么"。**Key**是programmatic access用的密钥对（access key ID + secret access key）；**Policy**是JSON格式权限规则文件，挂在用户/组/角色上生效。

**ARN（Amazon Resource Name）** — 每个AWS资源的唯一"身份证号"，格式类似 `arn:aws:s3:::my-bucket/photo.jpg`，写IAM policy时精确指定管的是哪个资源。

**AWS Account ID** — 12位数字，每个AWS账户的唯一编号。

**AWS Access Key** — 本地机器上存的凭证文件，通常在 `~/.aws/credentials`（INI格式），CLI/SDK读这个文件认证。**绝对不能提交进git或分享给别人**，泄露后别人能直接拿去用你的账户跑资源花钱。

## 基础设施即代码（IaC）

**CloudFormation** — 用YAML/JSON模板描述"我要什么资源"，AWS读模板自动创建/更新/删除，不用手动点控制台。

**CDK（Cloud Development Kit）** — 用Python/Node.js/TypeScript等编程语言定义基础设施，实际部署分两步：
1. **`cdk synth`**（本地）：把你写的代码**翻译成**一份CloudFormation模板文件，这步不碰AWS
2. **`cdk deploy`**：把生成的模板提交给CloudFormation服务，CloudFormation读模板真正创建资源

完整链条：**写Python代码 → CDK翻译成CloudFormation模板 → CloudFormation读模板创建资源**。CDK只是省去手写YAML，底层还是走CloudFormation。

## 服务模型（云计算责任划分）
- **IaaS**：只给基础设施（虚拟机/网络/存储），操作系统以上自己管。例：EC2
- **PaaS**：连运行环境都管好，只管上传代码。例：Elastic Beanstalk
- **FaaS**：只写一个函数，看不到服务器，按调用次数计费。例：Lambda
- **SaaS**：现成软件产品，登录直接用。例：Gmail、Zoom

## 存储与网络

**S3** — 对象存储，存文件（图片/视频/备份/静态网站）。
**EFS（Elastic File System）** — 网络文件系统，**多台EC2可以同时挂载共享读写**（类比Docker共享volume——多个容器挂同一个volume，谁写的文件其他容器立刻能读到；EFS就是"给多台EC2用的、网络版的共享volume"，思路完全一致，只是作用对象从"同一台机器上的多个容器"变成"多台不同的机器"）。S3不是文件系统，EBS是单台EC2专属，跟EFS的多机共享定位不同。
**CloudFront** — CDN，把内容缓存到全球边缘节点，就近访问加快加载。
**VPC** — 私有虚拟网络，可自定义子网/路由表/安全组。**Inbound**控制外部流量能不能进来，**Outbound**控制内部流量能不能出去。

## 数据库

**RDS** — 托管关系型数据库，支持MySQL/PostgreSQL/SQL Server等引擎，AWS管备份/打补丁/故障转移。
**Aurora** — AWS自研关系型数据库，兼容MySQL/PostgreSQL协议但性能更强，是RDS家族的"高级款"。
**Redshift** — 数据仓库，专做大规模分析查询（不是日常增删改查），有专门Query Editor直接写SQL。

## 计算相关

**AMI（Amazon Machine Image）** — EC2的"镜像模板"，含操作系统+预装软件快照。例：配置好一台EC2打包成AMI，以后批量开一模一样的服务器直接用这个AMI，不用每台重装。
**Savings Plans** — 承诺未来1/3年花固定金额换取比On-Demand更便宜的价格，适用EC2/Lambda/Fargate等。

**Amazon ECS/EKS/Fargate（为什么需要容器编排）** — 生产环境用容器要解决一堆问题：容器该放哪台机器跑、崩溃了怎么自动重启、流量变大怎么扩容、更新怎么不停机——这些统称"容器编排（orchestration）"，ECS和EKS都是干这个的。
- **ECS**：AWS自己发明的专有编排系统，只能在AWS用，不开源
- **EKS**：不是AWS发明的技术——底层是 **Kubernetes**（Google开源出来的容器编排标准，业界通用，能跨云）。EKS是"AWS帮你把Kubernetes这套开源系统的复杂运维（尤其control plane）管起来"，你不用自己维护底层，但技术标准是开源的，不锁定AWS
- **Fargate**（无正式中文译名，可理解为"无服务器容器运行引擎"）：不管选ECS还是EKS编排，容器终究要跑在某台机器上——默认这台机器是你自己申请配置的EC2；Fargate把"这台机器"也交给AWS，你只告诉AWS容器需要多少CPU/内存，AWS自动找机器跑，你永远看不到那台服务器，按容器实际用量付费

一句话：**ECS/EKS决定"怎么调度容器"，Fargate决定"容器实际跑在谁的机器上"（答案：不用你操心）**。

## 事件驱动/集成服务

**Amazon EventBridge**（原名Event Bus）— 事件总线服务。发布者（比如S3）往总线上发事件，订阅者（Lambda等）根据规则被自动通知，两边完全解耦、互不知道对方存在。

**类比修正**：不是webhook（webhook是点对点、A硬编码B的地址），更接近 **Kafka的producer/consumer模型**（发布-订阅、解耦思想一致）。但跟Kafka有关键区别：
| | Kafka | EventBridge |
|---|---|---|
| 订阅方式 | 按topic名字订阅 | 按**事件内容做模式匹配**（pattern matching），更像"内容路由" |
| 消息保留 | 持久化存储，consumer可回放历史、控制offset | **不保留历史**，事件发生即时推送，没有回放机制 |
| 定位 | 通用消息队列/流处理基础设施 | AWS服务事件的"胶水"，没有Kafka的海量吞吐/流处理定位 |

一句话：发布-订阅解耦思想一样，但Kafka是"持久化消息日志"，EventBridge是"实时事件路由器，过了就没了"。需要"消息不能丢、能重新消费"的场景该用SQS或AWS MSK（Kafka托管版），不该用EventBridge。

**AWS AppSync** — 托管GraphQL API服务，把多个数据源（数据库、Lambda、REST API）包装成统一查询入口，前端一次请求能同时拿到分散在不同数据源的数据。**是否需要写代码**：Schema部分是用GraphQL schema语言手写的声明式定义（类似写建表SQL）；Resolver（字段怎么去数据源取数据）简单场景（比如直接接DynamoDB）AppSync能自动生成，复杂业务逻辑就得自己写Lambda函数。

## 是否都需要会写代码

| 服务 | 需要写代码吗 |
|---|---|
| S3、EC2基础用法、Cloud9 | 不需要，控制台点点鼠标 |
| CloudFormation | 需要写YAML/JSON模板 |
| CDK、Lambda | 需要，本质是编程 |
| EventBridge、AppSync | 基础配置多靠控制台，复杂逻辑仍需代码（通常是Lambda） |

**CLF-C02 只考概念层面**——知道每个服务是什么、解决什么问题、什么场景用哪个，不要求真的会写代码或操作。
