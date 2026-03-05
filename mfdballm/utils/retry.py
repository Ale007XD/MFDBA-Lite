import asyncio

async def retry(fn, retries=3):

    for i in range(retries):

        try:
            return await fn()

        except Exception:

            if i == retries - 1:
                raise

            await asyncio.sleep(1)
