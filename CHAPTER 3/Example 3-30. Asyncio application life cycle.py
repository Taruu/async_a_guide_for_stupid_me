import asyncio
from asyncio import StreamReader, StreamWriter


async def echo(reader: StreamReader, writer: StreamWriter):
    print("New connection")
    try:
        while data := await reader.readline(): #wait line in coro format
            writer.write(data.upper())
            await writer.drain() #Wait until it is appropriate to resume writing to the stream
        print("Leaving Connection")
    except asyncio.CancelledError:
        print("Connection dropped")


async def main(host="127.0.0.1", port=8888):
    server = await asyncio.start_server(echo, host, port)
    async with server:
        await server.serve_forever() # make a coroutine


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Bye!")