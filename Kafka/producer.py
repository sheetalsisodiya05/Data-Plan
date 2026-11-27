import asyncio
from confluent_kafka.aio import AIOProducer
import json
async def transactional_produce(topic):
    producer = AIOProducer({
        "bootstrap.servers":"localhost:9092",
        "transactional.id" : "my-transactional-producer"
    })

    await producer.init_transactions()

    try:
        await producer.begin_transaction()

        futures = []
        for i in range(12):
            message ={
                'user_id' : f'user_id-{i}',
                'name' : f"user{i}@example.com",
                'active':True,
                'metadata':{
                    'source':"python-producer",
                    'version':1
                }

            }

            serialize_message = json.dumps(
                message ,
                indent=4,
            ).encode('utf-8')
            future = await producer.produce(topic=topic , value= serialize_message)
            futures.append(future)
        await producer.flush()
        await asyncio.gather(*futures)

        await producer.commit_transaction()
    except Exception as e:
        await producer.abort_transaction()
        raise

    finally :
        await producer.close()
asyncio.run(transactional_produce('my-topic'))