import asyncio
from confluent_kafka.aio import AIOProducer
import json
TOPIC = "orders-multi"
async def run_producer(producer_name):
    producer = AIOProducer({
        "bootstrap.servers":"localhost:9092",
        "transactional.id" : f"{producer_name}-tx",
        "enable.idempotence":True,
        "acks":"all"
    })

    await producer.init_transactions()

    try:
        await producer.begin_transaction()

        futures = []
        for i in range(12):
            message = {
                "producer": producer_name,
                "order_id": f"{producer_name}-{i}",
                "amount": 100 + i,
                "status": "created"
            }


            serialize_message = json.dumps(message ,indent=4,).encode('utf-8')
            future = await producer.produce(topic=TOPIC , value= serialize_message)
            futures.append(future)
        await producer.flush()
        await asyncio.gather(*futures)

        await producer.commit_transaction()
    except Exception as e:
        await producer.abort_transaction()
        raise

    finally :
        await producer.close()
# asyncio.run(transactional_produce('my-topic'))