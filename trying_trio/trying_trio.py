import trio


async def main():
    async with trio.open_nursery() as nursery:


trio.run(main)
