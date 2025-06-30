from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Calculator Server", host="0.0.0.0", port=8050)


# Simple tool
@mcp.tool()
def add_numbers(number1: int, number2: int) -> str:
    """Addes two numbers together.

    Args:
        number1: first number
        number2: second number
    Returns:
        Textual representation of the sum of the two numbers in the format "The sum is: <sum>".
    Example:
        add_numbers(3, 5) -> "The sum is: 8"
    """
    return f"The sum is: {number1 + number2}"


# Run the server
if __name__ == "__main__":
    transport = "sse"  # Change to "stdio" for stdio transport
    if transport == "sse":
        print("Starting MCP server with SSE transport...")
        mcp.run(transport="sse")
    elif transport == "stdio":
        print("Starting MCP server with stdio transport...")
        mcp.run(transport="stdio")
    else:
        raise ValueError(f"Unsupported transport: {transport}. Use 'sse' or 'stdio'.")
