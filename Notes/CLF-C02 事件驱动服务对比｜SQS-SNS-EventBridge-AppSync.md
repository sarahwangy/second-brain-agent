# CLF-C02 事件驱动服务对比｜SQS-SNS-EventBridge-AppSync

> **Purpose**: AWS 事件驱动/消息集成服务（SQS队列、SNS发布订阅、EventBridge事件总线、AppSync GraphQL网关）的对比讲解，含类比纠偏和代码示例。从 [[CLF-C02 核心服务讲解问答]] 拆分出来（Gardener Fission建议，这部分内容自成体系，不依赖笔记里其他章节）。

## 目录

- [消息与解耦服务对比（SQS / SNS / EventBridge）](#消息与解耦服务对比sqs--sns--eventbridge)
- [Amazon EventBridge 详解](#amazon-eventbridge-详解)
- [AWS AppSync](#aws-appsync)

---

## 消息与解耦服务对比（SQS / SNS / EventBridge）

| 服务 | 模式 | 核心用途 |
|---|---|---|
| SQS | 队列 | 消息暂存，一条消息只被一个消费者处理一次 |
| SNS | 发布/订阅 | 消息广播，推给所有订阅者，不存储 |
| EventBridge | 事件总线 | 基于事件内容做规则路由，可对接AWS原生事件和第三方SaaS |

**为什么用消息队列/发布订阅而不是直接调用API**：
- **解耦**：下单服务不需要知道下游服务的存在，新增下游只需订阅
- **削峰填谷**：瞬间大量请求涌入时，SQS先接住，消费者按能力慢慢处理
- **容错**：下游服务临时挂掉，消息还在队列里等着，不会丢失

常见组合（**Fanout模式**）：下单服务发消息到SNS Topic → 广播给多个SQS队列 → 各下游服务各自订阅消费，互不阻塞。

**EventBridge 相比 SNS 的优势**：可以根据事件内容（比如`status: cancelled`）做条件路由，只把符合条件的事件转发给对应目标；SNS做不到这种按内容分流，只能无差别广播给所有订阅者。

## Amazon EventBridge 详解

**Amazon EventBridge**（原名Event Bus）— 事件总线服务。发布者（比如S3）往总线上发事件，订阅者（Lambda等）根据规则被自动通知，两边完全解耦、互不知道对方存在。

**类比修正**：不是webhook（webhook是点对点、A硬编码B的地址），更接近 **Kafka的producer/consumer模型**（发布-订阅、解耦思想一致）。但跟Kafka有关键区别：

| | Kafka | EventBridge |
|---|---|---|
| 订阅方式 | 按topic名字订阅 | 按**事件内容做模式匹配**（pattern matching），更像"内容路由" |
| 消息保留 | 持久化存储，consumer可回放历史、控制offset | **不保留历史**，事件发生即时推送，没有回放机制 |
| 定位 | 通用消息队列/流处理基础设施 | AWS服务事件的"胶水"，没有Kafka的海量吞吐/流处理定位 |

一句话：发布-订阅解耦思想一样，但Kafka是"持久化消息日志"，EventBridge是"实时事件路由器，过了就没了"。需要"消息不能丢、能重新消费"的场景该用SQS或AWS MSK（Kafka托管版），不该用EventBridge。

![[Sources/ScreenShot_2026-08-20_112128_114.png]]
*Event Bus 官方示意图：Event从source进入总线，按不同Rule匹配后路由给不同Target；EventBridge是这个模型的无服务器实现，之前叫Amazon CloudWatch Events。*

## AWS AppSync

**AWS AppSync** — 托管GraphQL API服务，把多个数据源（数据库、Lambda、REST API）包装成统一查询入口，前端一次请求能同时拿到分散在不同数据源的数据。

![[Sources/ScreenShot_2026-08-20_112243_031.png]]
*AppSync 官方配置项：API类型分GraphQL API(单数据源)和Merged API(多个团队各自API合并成一个)；支持的数据源包括DynamoDB/OpenSearch/Lambda/HTTP/EventBridge/RDS；缓存分None/全量/按resolver三档，但开缓存就不是serverless了（要选实例类型）。*

**Schema 和 Resolver 是不是都要写**：不是二选一，是叠加关系——**Schema 一定要写**（没有例外，定义了API有哪些查询/数据类型，是必须的）；**Resolver 看情况**：简单场景（直接对接DynamoDB/Aurora Serverless）AppSync向导自动生成（用VTL模板语言，基本不用手写）；复杂场景（调第三方API、拼接多数据源、自定义业务逻辑）就得自己写Lambda函数当resolver。

**代码示例**：

Schema（声明"有一个Order类型，客户端可以用getOrder查询"）：
```graphql
type Order {
  id: ID!
  customerName: String
  items: [String]
  status: String
}

type Query {
  getOrder(id: ID!): Order
}
```

复杂场景的 Lambda Resolver（从DynamoDB取基础信息+调第三方API查物流状态，拼好一次性返回）：
```python
def handler(event, context):
    order_id = event['arguments']['id']
    order = get_order_from_dynamodb(order_id)
    order['status'] = call_shipping_api(order_id)
    return order
```

客户端调用（只发一次请求，AppSync后台自动跑上面的Resolver拼数据）：
```graphql
query {
  getOrder(id: "12345") {
    customerName
    items
    status
  }
}
```
