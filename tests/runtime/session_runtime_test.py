import asyncio
from mfdballm.runtime import SessionRuntime


async def main():

    runtime = SessionRuntime()

    result = await runtime.run([
        {"role": "user", "content": "Hello"}
    ])

    print("RUNTIME RESULT:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
