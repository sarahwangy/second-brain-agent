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
- [监控与审计三件套](#监控与审计三件套)
- [事件驱动/集成服务](#事件驱动集成服务)
- [网络安全与存储补充问答](#网络安全与存储补充问答)
- [是否都需要会写代码](#是否都需要会写代码)

---

## 开发/CLI 工具

![[Sources/ScreenShot_2026-08-20_103601_343.png]]
*AWS Management Console 首页概览：EC2/IAM/Cloud9/S3/VPC/CloudFront/CloudFormation/RDS/Elastic Beanstalk等常用服务都能从这里的"最近访问"直接进入。*

**AWS CloudShell** — 浏览器里直接用的命令行终端，登录控制台点一下图标就能用，预装了 AWS CLI 和常用工具，不用自己配置环境。例：临时跑几条 `aws s3 ls` 命令，不想在自己电脑装 CLI。

**AWS CLI** — 在自己电脑终端里用命令操作 AWS 的工具，装好后配置 access key，就能用 `aws ec2 describe-instances` 代替点控制台。

**AWS Cloud9** — 浏览器里的云端 IDE，自带终端、调试工具。界面（浏览器编辑器）和计算资源（实际跑代码的机器）是分开的两件事：
- 可以让 Cloud9 自动帮你在后台开一台 **EC2**，代码实际在这台EC2上运行——**这台EC2按正常EC2价格收费**，Cloud9界面本身不额外收钱，停用记得关掉EC2或设自动休眠
- 也可以连接你已有的本地/其他机器，让Cloud9界面去操作那台机器

## 身份与权限

**IAM** — 管"谁能访问什么"。**Key**是programmatic access用的密钥对（access key ID + secret access key）；**Policy**是JSON格式权限规则文件，挂在用户/组/角色上生效。

**ARN（Amazon Resource Name）** — 每个AWS资源的唯一"身份证号"，格式类似 `arn:aws:s3:::my-bucket/photo.jpg`，写IAM policy时精确指定管的是哪个资源。

**AWS Account ID** — 12位数字，每个AWS账户的唯一编号。

![[Sources/ScreenShot_2026-08-20_112109_365.png]]
*AWS Account Root User：root账户权限不能被删除、不能用IAM policy限制，只能靠Organizations的SCP限制；一个账户只能有一个root。*

**AWS Access Key** — 本地机器上存的凭证文件，通常在 `~/.aws/credentials`（INI格式），CLI/SDK读这个文件认证。**绝对不能提交进git或分享给别人**，泄露后别人能直接拿去用你的账户跑资源花钱。

![[Sources/ScreenShot_2026-08-20_105840_248.png]]
![[Sources/ScreenShot_2026-08-20_105915_686.png]]
![[Sources/ScreenShot_2026-08-20_105943_789.png]]
![[Sources/ScreenShot_2026-08-20_110025_534.png]]
*Access Key 生成流程：IAM控制台创建 → 存入 `~/.aws/credentials`（TOML/INI格式）→ 可以用`[default]`和自定义profile名区分多套凭证 → `aws configure`命令能直接写入这个文件。*

## 基础设施即代码（IaC）

![[Sources/ScreenShot_2026-08-20_104944_197.png]]
*CFN（声明式，What you see is what you get）vs CDK（命令式，说清楚要什么剩下自动填）的对比。*

**CloudFormation** — 用YAML/JSON模板描述"我要什么资源"，AWS读模板自动创建/更新/删除，不用手动点控制台。

![[Sources/ScreenShot_2026-08-20_105012_543.png]]
*一段真实的CloudFormation YAML片段：定义一个EC2实例，用`Fn::FindInMap`按Region查AMI ID，绑定安全组和子网。*

**CDK（Cloud Development Kit）** — 用Python/Node.js/TypeScript等编程语言定义基础设施，实际部署分两步：
1. **`cdk synth`**（本地）：把你写的代码**翻译成**一份CloudFormation模板文件，这步不碰AWS
2. **`cdk deploy`**：把生成的模板提交给CloudFormation服务，CloudFormation读模板真正创建资源

完整链条：**写Python代码 → CDK翻译成CloudFormation模板 → CloudFormation读模板创建资源**。CDK只是省去手写YAML，底层还是走CloudFormation。

## 服务模型（云计算责任划分）
- **IaaS**：只给基础设施（虚拟机/网络/存储），操作系统以上自己管。例：EC2
- **PaaS**：连运行环境都管好，只管上传代码。例：Elastic Beanstalk
- **FaaS**：只写一个函数，看不到服务器，按调用次数计费。例：Lambda
- **SaaS**：现成软件产品，登录直接用。例：Gmail、Zoom

![[Sources/ScreenShot_2026-08-20_110236_126.png]]
*IaaS/PaaS/SaaS 三种模式下，"客户负责"（浅色）vs "AWS负责"（深色）的分界线——分界线越往下移，AWS管得越多。*

![[Sources/ScreenShot_2026-08-20_110359_857.png]]
*用计算举例细化到 IaaS/PaaS/SaaS/FaaS 四种模式各自对应哪个AWS服务、客户具体要管什么。*

![[Sources/ScreenShot_2026-08-20_110521_535.png]]
*责任共担模型的通用判断口诀：能配置/存储的东西是"云中的安全"（你负责），配置不了的是"云本身的安全"（AWS负责）。*

## 存储与网络

![[Sources/ScreenShot_2026-08-20_110926_883.png]]
*存储服务补充：Snow Family(Snowball Edge/Snowmobile/Snowcone，物理硬件搬大数据)、AWS Backup(跨EC2/EBS/RDS/DynamoDB/EFS的统一备份管理)、CloudEndure(灾备复制)、Amazon FSx(高性能文件系统，支持Windows的SMB或Linux的Lustre协议)。*

**S3** — 对象存储，存文件（图片/视频/备份/静态网站）。

**S3 存储类别分级**（同一份数据可以按访问频率放在不同层级省钱）：
- **S3 Standard** — 频繁访问，最贵
- **S3 Standard-IA** — 不频繁访问，存储便宜、取用时收费
- **S3 One Zone-IA** — 只存一个AZ，更便宜但少一层容灾（丢了这个AZ数据就没了）
- **S3 Glacier / Glacier Deep Archive** — 归档存储，超便宜但取用要等待（几小时到几天），适合长期备份
- **S3 Lifecycle Policy** — 自动规则，把旧数据按时间自动迁移到更便宜的类别（比如30天后自动转IA，90天后转Glacier）

**EFS（Elastic File System）** — 网络文件系统，**多台EC2可以同时挂载共享读写**（类比Docker共享volume——多个容器挂同一个volume，谁写的文件其他容器立刻能读到；EFS就是"给多台EC2用的、网络版的共享volume"，思路完全一致，只是作用对象从"同一台机器上的多个容器"变成"多台不同的机器"）。S3不是文件系统，EBS是单台EC2专属，跟EFS的多机共享定位不同。

**CloudFront** — CDN，把内容缓存到全球边缘节点，就近访问加快加载。常与S3搭配：静态网站/图片存S3，CloudFront加速全球访问。

**VPC** — 私有虚拟网络，可自定义子网/路由表/安全组。**Inbound**控制外部流量能不能进来，**Outbound**控制内部流量能不能出去。
- **Subnet**：Public Subnet（可直接访问互联网）vs Private Subnet（不能，常放数据库这类不该暴露的资源）
- **Internet Gateway** — VPC连接互联网的"门"
- **Route Table** — 决定流量该往哪走

![[Sources/ScreenShot_2026-08-20_111657_005.png]]
*完整VPC网络架构图：Internet → IGW → Router → Route Table/NACL → Public Subnet(EC2, Security Group) / Private Subnet(RDS)，NAT负责让私有子网出网。*

**Security Group vs NACL**（两层不同粒度的防火墙）：
| | Security Group | NACL |
|---|---|---|
| 作用范围 | 实例级别 | 子网级别 |
| 规则类型 | 只能"允许" | 可"允许"也可"拒绝" |
| 状态 | 有状态（Stateful，进来的流量自动放行对应的返回流量） | 无状态（Stateless，进、出要分别设置规则） |

记忆：Security Group像门卫只查进（默认全部拒绝，只放行你允许的），NACL像围墙检查站，进出都查、还能主动拉黑。

![[Sources/ScreenShot_2026-08-20_111726_902.png]]
*NACL 在子网层面挡流量的示意图：可以针对具体IP设Deny规则（比如"屏蔽某个known-abuse的IP"），Security Group则是包在NACL里面、实例级别的第二道门。*

**Auto Scaling + ELB**：
- **ELB（Elastic Load Balancer）** — 把流量分发到多台EC2实例，避免单点过载
- **Auto Scaling** — 根据流量指标自动增减EC2实例数量
常见场景：流量波动大，需要自动应对高峰、节省闲时成本，两者通常搭配使用（ELB分流量，Auto Scaling决定开几台机器来分）。

## 数据库

**RDS** — 托管关系型数据库，支持MySQL/PostgreSQL/SQL Server等引擎，AWS管备份/打补丁/故障转移。
**Aurora** — AWS自研关系型数据库，兼容MySQL/PostgreSQL协议但性能更强，是RDS家族的"高级款"。
**Redshift** — 数据仓库，专做大规模分析查询（不是日常增删改查），有专门Query Editor直接写SQL。

![[Sources/ScreenShot_2026-08-20_111350_924.png]]
*RDS/Aurora 控制台首页：可以选"Express configuration"几秒建好预配置数据库，也可以"Full configuration"自定义各种细节。*

![[Sources/ScreenShot_2026-08-20_111359_258.png]]
*建数据库时的引擎选择界面：Aurora(MySQL/PostgreSQL兼容)、MySQL、PostgreSQL、MariaDB、Oracle、SQL Server、IBM Db2都是可选项。*

## 计算相关

![[Sources/ScreenShot_2026-08-20_110137_409.png]]
*AWS官方文档首页（以EC2为例）：每个服务的文档一般都有User Guide、Instance Types、相关特性专题指南，遇到具体细节记不清时可以直接查docs.aws.amazon.com。*

**AMI（Amazon Machine Image）** — EC2的"镜像模板"，含操作系统+预装软件快照。例：配置好一台EC2打包成AMI，以后批量开一模一样的服务器直接用这个AMI，不用每台重装。

![[Sources/ScreenShot_2026-08-20_110557_788.png]]
*计算服务全家福：LightSail(EC2的简化友好版)、ECS/ECR/Fargate(容器编排+镜像仓库+无服务器运行)、EKS(托管Kubernetes)、Lambda(无服务器函数)。*

**AWS Elastic Beanstalk（PaaS）** — 类比自己手动用 Nginx 部署到服务器的流程：正常手动部署要（1）开服务器（2）装Nginx做反向代理/静态文件服务（3）装应用运行时（Gunicorn/PM2等），Nginx转发请求给它（4）配置开机自启/日志/监控（5）要扩容还得自己加机器配负载均衡。**Beanstalk 把这一整套自动化了**——选平台（比如"Python"）、上传代码，Beanstalk 自动配好运行环境+负载均衡+Auto Scaling。注意：底层其实还是EC2在跑，只是这层配置/伸缩AWS帮你打理，你不直接碰。跟纯EC2的区别：EC2是"给空白虚拟机，自己装一切"（IaaS）；Beanstalk是"只管应用代码，运行环境这层AWS搭好"（PaaS）。

**Reserved Instances vs Savings Plans（都是"承诺花钱换折扣"，但灵活度不同）**：
| | Reserved Instances | Savings Plans |
|---|---|---|
| 承诺方式 | 承诺**具体实例类型+Region**（如"1年内用m5.large在悉尼"） | 承诺**每小时花多少钱**（如"1年内每小时$10"），不锁定实例类型 |
| 灵活度 | 低——换实例类型/Region通常要重新买 | 高——花费总额匹配承诺额度即可，中途换实例类型/Region/甚至换Lambda/Fargate折扣照样生效 |
| 覆盖范围 | 主要EC2（RDS/ElastiCache等各自有RI） | EC2+Lambda+Fargate用同一份Savings Plan覆盖 |

一句话：**RI是"预定一辆具体型号的车用1年"，Savings Plans是"承诺每月至少打车花$500，不管打什么车都按这个额度算"**——后者更灵活，AWS近年更推荐用Savings Plans代替RI（除非非常确定未来1-3年实例类型/Region完全不变）。

![[Sources/ScreenShot_2026-08-20_111828_309.png]]
*EC2实例大小对比：同一个系列(t2)从small到large，vCPU/内存/价格基本按倍数往上翻，选型时先看这个规律。*

![[Sources/ScreenShot_2026-08-20_111946_771.png]]
*EC2五种付费方式总览：On-Demand(最灵活最贵)、Spot(最便宜最多省90%但可能被回收)、Reserved(承诺1/3年最多省75%)、Dedicated(独占物理硬件)。*

![[Sources/ScreenShot_2026-08-20_112012_987.png]]
*Reserved Instances 详解：折扣由Term(期限)×Class(标准/可转换)×Payment Option(预付比例)共同决定，期限越长、预付越多、灵活性越低，折扣越大。*

![[Sources/ScreenShot_2026-08-20_112036_007.png]]
*Standard RI vs Convertible RI：Standard不能换配置但能在RI Marketplace卖掉；Convertible能换实例类型/平台但不能在市场卖，只能跟AWS换。*

**Amazon ECS/EKS/Fargate（为什么需要容器编排）** — 生产环境用容器要解决一堆问题：容器该放哪台机器跑、崩溃了怎么自动重启、流量变大怎么扩容、更新怎么不停机——这些统称"容器编排（orchestration）"，ECS和EKS都是干这个的。
- **ECS**：AWS自己发明的专有编排系统，只能在AWS用，不开源
- **EKS**：不是AWS发明的技术——底层是 **Kubernetes**（Google开源出来的容器编排标准，业界通用，能跨云）。EKS是"AWS帮你把Kubernetes这套开源系统的复杂运维（尤其control plane）管起来"，你不用自己维护底层，但技术标准是开源的，不锁定AWS
- **Fargate**（无正式中文译名，可理解为"无服务器容器运行引擎"）：不管选ECS还是EKS编排，容器终究要跑在某台机器上——默认这台机器是你自己申请配置的EC2；Fargate把"这台机器"也交给AWS，你只告诉AWS容器需要多少CPU/内存，AWS自动找机器跑，你永远看不到那台服务器，按容器实际用量付费

一句话：**ECS/EKS决定"怎么调度容器"，Fargate决定"容器实际跑在谁的机器上"（答案：不用你操心）**。

## 监控与审计三件套

| 服务 | 作用 | 记忆点 |
|---|---|---|
| CloudWatch | 监控性能指标、设置告警、看日志 | 看仪表盘、设警报 |
| CloudTrail | 记录谁在什么时候做了什么操作（API调用日志） | 谁动了我的资源 |
| Config | 跟踪资源**配置**变化历史，检查合规 | 配置有没有被改 |

三者容易混——CloudWatch管"性能好不好"，CloudTrail管"谁操作了"，Config管"配置变没变、合不合规"，三个问的是完全不同的问题。

## 事件驱动/集成服务

SQS/SNS/EventBridge对比、Fanout模式、EventBridge vs Kafka类比纠偏、AppSync的Schema/Resolver讲解+代码示例，都拆到了 [[CLF-C02 事件驱动服务对比｜SQS-SNS-EventBridge-AppSync]]（Gardener Fission建议，这部分内容自成体系）。

## 网络安全与存储补充问答

**NACL 和 Security Group 的流量经过顺序** — 外部请求到达EC2必须依次通过两道关卡：①NACL（子网大门）→②Security Group（实例小门）→EC2。如果①拒绝，流量直接丢弃，Security Group根本看不到这个请求。只有①放行，才轮到②决定放不放行。常见误判：NACL规则编号顺序配错被别的规则先匹配、入站/出站方向配反、NACL挂在子网上而不是EC2上。

**端口号是什么** — 相当于服务器（一栋楼）里的"房间号"：80=HTTP、443=HTTPS、22=SSH、3306=MySQL。

**"Security Group只配入站，出站也能响应"的考点** — Security Group是有状态的（Stateful）：入站规则放行某个连接后，会记住这次连接，对应返回流量自动放行，不需要额外配出站规则。NACL无状态，进出流量必须分别配置。

**Redshift 具体什么场景用** — 核心区分：RDS/DynamoDB处理OLTP（业务系统实时读写），Redshift处理OLAP（海量历史数据分析）。典型场景：BI报表、数据仓库汇总多系统数据分析、配合QuickSight/Tableau做可视化、海量日志分析。底层原因：RDS是行式存储适合取出/更新整条记录，Redshift是列式存储适合只扫描某几列做统计，效率高得多。很多公司RDS和Redshift同时用：RDS撑实时业务，Redshift定期同步数据做分析报表。

**AWS Auto Scaling 是不是独立服务** — 两个层级：各服务早自带独立伸缩机制（EC2 Auto Scaling、DynamoDB Auto Scaling、ECS Service Auto Scaling、Aurora Auto Scaling）；"AWS Auto Scaling"（大写完整名字）是后来推出的统一管理面板，本身不直接执行伸缩，而是调用各服务自己的机制。CLF-C02考试基本只考"EC2 Auto Scaling + ELB"这个最常见组合，不深挖两层区别。

**S3 + CloudFront 加速的搭建步骤**：
1. 静态资源上传到S3桶作为源站(Origin)
2. CloudFront创建Distribution，指定源站为该S3桶
3. 配置Origin Access Control(OAC)，让S3只信任来自该CloudFront分发的请求，防止绕过CloudFront直接访问S3 URL
4. 设置缓存行为(Cache Behavior)，配置哪些内容缓存多久(TTL)
5. （可选）绑定自定义域名，用ACM免费申请SSL证书走HTTPS
6. 部署，等待配置同步到全球边缘节点（几分钟到二十分钟）
7. 验证：对比直接访问S3 URL和访问CloudFront域名的延迟差异

**S3 文件能被分享访问，是不是因为配了 CloudFront** — 不是，两件不同的事：S3文件本身能被访问靠的是**权限设置**（桶/对象公开可读，或用**预签名URL**——带过期时间的临时链接，桶保持私有也能用，请求直接打到S3跟CloudFront无关）；CloudFront解决的是**访问速度**问题，让全球用户从最近边缘节点获取缓存副本。类比：只用S3分享像"文件放公司总部档案室，谁看都要跑一趟总部"；S3+CloudFront像"全球开分店，提前把副本送到离你最近的分店"。

## 是否都需要会写代码

| 服务 | 需要写代码吗 |
|---|---|
| S3、EC2基础用法、Cloud9 | 不需要，控制台点点鼠标 |
| CloudFormation | 需要写YAML/JSON模板 |
| CDK、Lambda | 需要，本质是编程 |
| EventBridge、AppSync | 基础配置多靠控制台，复杂逻辑仍需代码（通常是Lambda） |

**CLF-C02 只考概念层面**——知道每个服务是什么、解决什么问题、什么场景用哪个，不要求真的会写代码或操作。
