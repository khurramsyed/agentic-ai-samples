import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()


async def main():
    async with sse_client("http://localhost:8050/sse") as (reader, writer):
        async with ClientSession(reader, writer) as session:
            # Call the add_numbers tool
            await session.initialize()

            tools_result = await session.list_tools()
            print("available tools:", tools_result.tools)

            for tool in tools_result.tools:
                print(f"  - {tool.name} , {tool.description}")

            result = await session.call_tool(
                "add_numbers", arguments={"number1": 3, "number2": 5}
            )
            print("Tool call result:", result)


if __name__ == "__main__":
    asyncio.run(main())
