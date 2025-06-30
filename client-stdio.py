import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

nest_asyncio.apply()


async def main():
    server_params = StdioServerParameters(command="python", args=["server.py"])

    async with stdio_client(server_params) as (reader, writer):
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
