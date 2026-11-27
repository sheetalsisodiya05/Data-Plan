import asyncio
from confluent_kafka.aio import AIOConsumer
import json

TOPIC = "orders-multi"

async def run_consumer(consumer_name,group_id):
    consumer = AIOConsumer({
    'bootstrap.servers':'localhost:9092',
    'group.id': group_id,
    'enable.auto.commit':False,
    'enable.auto.offset.store' : 'false',
    'auto.offset.reset': 'earliest',
    "isolation.level": "read_committed"
   })

    async def on_assign(consumer,partitions):
        print(f"Partition assigned :{partitions}")


    async def on_revoke(consumer,partitions):
        print(f"Partition revoked:{partitions}")
        await consumer.commit()

    async def on_lost(consumer, partitions):
        print(f"partitions lost:{partitions}")

    await consumer.subscribe([TOPIC],on_assign=on_assign,on_revoke=on_revoke,on_lost= on_lost)

    try:
        while True:
            msg = await consumer.poll(timeout = 1.0)
            if msg is not None and not msg.error():
                
                print(f'message consumed :{consumer_name} | Group: {group_id} | Partition: {msg.partition()} | Offset: {msg.offset()} |  {json.loads(msg.value().decode('utf-8'))}')
                await consumer.store_offsets(message= msg)
                await consumer.commit(asynchronous = False)
    except Exception as e:
        pass
    finally :
        await consumer.unsubscribe()
        await consumer.close()
# asyncio.run(main())