# CLF-C02 Event-Driven Services Comparison | SQS-SNS-EventBridge-AppSync

> **Purpose**: A comparative explanation of AWS's event-driven/messaging integration services (the SQS queue, SNS pub/sub, the EventBridge event bus, and the AppSync GraphQL gateway), including analogy corrections and code examples. Split out from [[EN-CLF-C02 Core Services Q&A]] (per a Gardener Fission recommendation — this content forms a self-contained unit, independent of the rest of that note).

## Table of Contents

- [Messaging & Decoupling Services Compared (SQS / SNS / EventBridge)](#messaging--decoupling-services-compared-sqs--sns--eventbridge)
- [Amazon EventBridge in Detail](#amazon-eventbridge-in-detail)
- [AWS AppSync](#aws-appsync)

---

## Messaging & Decoupling Services Compared (SQS / SNS / EventBridge)

| Service | Model | Core purpose |
|---|---|---|
| SQS | Queue | Message buffering — a single message is processed by exactly one consumer |
| SNS | Pub/Sub | Message broadcast — pushed to all subscribers, not stored |
| EventBridge | Event bus | Content-based rule routing — can integrate both native AWS events and third-party SaaS |

**Why use a message queue / pub-sub instead of calling APIs directly**:
- **Decoupling**: the order service doesn't need to know downstream services exist; adding a new downstream consumer just means subscribing
- **Smoothing traffic spikes**: when a sudden flood of requests arrives, SQS absorbs it first, and consumers process it at their own pace
- **Fault tolerance**: if a downstream service temporarily goes down, the message stays waiting in the queue — nothing is lost

A common combination (the **Fanout pattern**): the order service sends a message to an SNS Topic → it's broadcast to multiple SQS queues → each downstream service subscribes and consumes independently, without blocking one another.

**EventBridge's advantage over SNS**: it can do conditional routing based on event content (e.g. `status: cancelled`), forwarding only matching events to the corresponding target. SNS can't do this kind of content-based routing — it can only broadcast indiscriminately to every subscriber.

## Amazon EventBridge in Detail

**Amazon EventBridge** (formerly Event Bus) — an event-bus service. A publisher (e.g. S3) puts an event onto the bus, and subscribers (Lambda, etc.) are automatically notified based on rules — the two sides are fully decoupled and unaware of each other.

**Analogy correction**: it's not a webhook (a webhook is point-to-point, with A hardcoding B's address) — it's closer to **Kafka's producer/consumer model** (same pub/sub decoupling philosophy). But there are key differences from Kafka:

| | Kafka | EventBridge |
|---|---|---|
| Subscription method | Subscribe by topic name | Subscribe via **content-based pattern matching** — more like "content routing" |
| Message retention | Persisted, consumers can replay history and control their offset | **No history retained** — events are pushed the instant they happen, no replay mechanism |
| Positioning | General-purpose message queue / stream-processing infrastructure | The "glue" for AWS service events, without Kafka's high-throughput stream-processing role |

In one line: the pub/sub decoupling idea is the same, but Kafka is a "persisted message log," while EventBridge is a "real-time event router — once it's passed, it's gone." Scenarios that need "messages that can't be lost and can be re-consumed" should use SQS or AWS MSK (the managed Kafka service), not EventBridge.

![[Sources/ScreenShot_2026-08-20_112128_114.png]]
*The official Event Bus diagram: an Event enters the bus from a source, gets matched against different Rules, and is routed to different Targets; EventBridge is the serverless implementation of this model — it used to be called Amazon CloudWatch Events.*

## AWS AppSync

**AWS AppSync** — A managed GraphQL API service that wraps multiple data sources (databases, Lambda, REST APIs) into a single unified query endpoint, letting the frontend fetch data spread across different sources in one request.

![[Sources/ScreenShot_2026-08-20_112243_031.png]]
*AppSync's official configuration options: API types split into GraphQL API (single data source) and Merged API (multiple teams' own APIs merged into one); supported data sources include DynamoDB/OpenSearch/Lambda/HTTP/EventBridge/RDS; caching has three tiers — None/full-request/per-resolver — but turning on caching means it's no longer serverless (you have to pick an instance type).*

**Do you have to write both a Schema and a Resolver?** It's not either/or — they stack: the **Schema is always required** (no exceptions — it defines what queries/data types the API has); the **Resolver depends on the situation**: for simple scenarios (connecting directly to DynamoDB/Aurora Serverless), AppSync's wizard auto-generates it (using the VTL template language, basically no hand-writing needed); for complex scenarios (calling a third-party API, combining multiple data sources, custom business logic), you have to write your own Lambda function to serve as the resolver.

**Code example**:

Schema (declaring "there's an Order type, and clients can query it via getOrder"):
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

A Lambda Resolver for the complex scenario (pull the base info from DynamoDB + call a third-party API for shipping status, combine them, and return in one response):
```python
def handler(event, context):
    order_id = event['arguments']['id']
    order = get_order_from_dynamodb(order_id)
    order['status'] = call_shipping_api(order_id)
    return order
```

Client call (a single request; AppSync runs the Resolver above behind the scenes and assembles the data):
```graphql
query {
  getOrder(id: "12345") {
    customerName
    items
    status
  }
}
```
