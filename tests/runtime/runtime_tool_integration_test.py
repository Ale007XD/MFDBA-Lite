import asyncio

from mfdballm.runtime import SessionRuntime


async def main():

    runtime = SessionRuntime()

    r = await runtime.run([
        {"role": "user", "content": "hello"}
    ])

    print("RUNTIME RESPONSE:", r)


asyncio.run(main())
