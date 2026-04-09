from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> str:
    """Add two numbers"""
    return f"{a + b}"

@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return (a * b)+8

@mcp.tool
def meaning_of_life() -> str:
    """Return the meaning of life"""
    return "Manger des frites"

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0")