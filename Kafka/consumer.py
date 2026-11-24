
import json
from confluent_kafka import Consumer, KafkaException

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "orders-processing-group",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
    "enable.auto.offset.store": False
})

consumer.subscribe(["orders"])

print("Consumer started. Waiting for orders...")

try:
    while True:
        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            raise KafkaException(message.error())

        try:
            order = json.loads(message.value().decode("utf-8"))

            print("\nProcessing order:")
            print(json.dumps(order, indent=4))

            # Simulate successful business processing.
            print(f"Order {order['order_id']} processed successfully.")

            # Commit only after successful processing.
            consumer.commit(
                message=message,
                asynchronous=False
            )

            print(
                f"Committed offset {message.offset() + 1} "
                f"for partition {message.partition()}"
            )

        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            print(f"Invalid JSON message: {error}")
            # Do not commit. We will add DLQ handling later.

except KeyboardInterrupt:
    print("\nConsumer stopped.")

finally:
    consumer.close()
