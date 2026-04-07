from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> str:
    """Add two numbers"""
    return f"{a + b}"

if __name__ == "__main__":
    mcp.run(transport="sse")