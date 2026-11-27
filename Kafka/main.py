import asyncio
from consumer import run_consumer
from producer import run_producer
async def main():

    producers = [
        asyncio.create_task(run_producer("producer-1")),
        asyncio.create_task(run_producer("producer-2"))
    ]

    consumers = [
        asyncio.create_task(
            run_consumer("consumer-A1", "orders-analytics")
        ),
        asyncio.create_task(
            run_consumer("consumer-A2", "orders-analytics")
        ),
        asyncio.create_task(
            run_consumer("consumer-B1", "orders-warehouse")
        ),
        asyncio.create_task(
            run_consumer("consumer-B2", "orders-warehouse")
        )
    ]

    try:
        await asyncio.gather(*producers)

        print("All producers completed.")

        # Consumers continue running until interrupted
        await asyncio.gather(*consumers)

    finally:
        for task in consumers:
            task.cancel()

        await asyncio.gather(
            *consumers,
            return_exceptions=True
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Application stopped.")