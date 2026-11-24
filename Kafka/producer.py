
import json
from confluent_kafka import Producer

producer = Producer({
    "bootstrap.servers": "localhost:9092",
    "client.id": "orders-producer",
    "acks": "all",
    "enable.idempotence": True
})


def delivery_report(error, message):
    if error:
        print(f"Delivery failed: {error}")
    else:
        print(
            f"Delivered | "
            f"topic={message.topic()} | "
            f"partition={message.partition()} | "
            f"offset={message.offset()} | "
            f"key={message.key().decode()}"
        )


orders = [
    {
        "order_id": 101,
        "customer_id": "customer-1",
        "amount": 2500,
        "status": "PLACED"
    },
    {
        "order_id": 102,
        "customer_id": "customer-2",
        "amount": 1800,
        "status": "PLACED"
    },
    {
        "order_id": 103,
        "customer_id": "customer-1",
        "amount": 3200,
        "status": "PLACED"
    },
    {
        "order_id": 104,
        "customer_id": "customer-3",
        "amount": 900,
        "status": "PLACED"
    }
]


for order in orders:
    producer.produce(
        topic="orders",
        key=order["customer_id"].encode("utf-8"),
        value=json.dumps(order).encode("utf-8"),
        on_delivery=delivery_report
    )

    # Serve delivery callbacks and allow queued messages to progress.
    producer.poll(0)

remaining = producer.flush(10)

if remaining:
    print(f"{remaining} message(s) were not delivered before timeout.")
