import pytest
from fastmcp import Client
from server import add, multiply, meaning_of_life, mcp


# ─────────────────────────────────────────────
# Tests unitaires (appel direct des fonctions)
# ─────────────────────────────────────────────

# --- add ---

def test_add_positive_numbers():
    assert add(2, 3) == "5"

def test_add_negative_numbers():
    assert add(-4, -6) == "-10"

def test_add_mixed_sign():
    assert add(-3, 7) == "4"

def test_add_zeros():
    assert add(0, 0) == "0"

def test_add_returns_string():
    result = add(1, 1)
    assert isinstance(result, str)


# --- multiply ---

def test_multiply_positive_floats():
    assert multiply(2.0, 3.0) == 14.0  # (2*3)+8 = 14

def test_multiply_by_zero():
    assert multiply(0.0, 5.0) == 8.0  # (0*5)+8 = 8

def test_multiply_negative_values():
    assert multiply(-2.0, 3.0) == 2.0  # (-2*3)+8 = 2

def test_multiply_integers_as_floats():
    assert multiply(4.0, 4.0) == 24.0  # (4*4)+8 = 24

def test_multiply_returns_float():
    result = multiply(1.0, 1.0)
    assert isinstance(result, float)


# --- meaning_of_life ---

def test_meaning_of_life_returns_expected():
    assert meaning_of_life() == "Manger des frites"

def test_meaning_of_life_returns_string():
    assert isinstance(meaning_of_life(), str)

def test_meaning_of_life_not_empty():
    assert len(meaning_of_life()) > 0


# ─────────────────────────────────────────────
# Tests d'intégration (via client FastMCP)
# ─────────────────────────────────────────────

async def test_mcp_tool_add():
    async with Client(mcp) as client:
        result = await client.call_tool("add", {"a": 10, "b": 5})
    assert result.content[0].text == "15"


async def test_mcp_tool_add_negative():
    async with Client(mcp) as client:
        result = await client.call_tool("add", {"a": -3, "b": -2})
    assert result.content[0].text == "-5"


async def test_mcp_tool_multiply():
    async with Client(mcp) as client:
        result = await client.call_tool("multiply", {"a": 3.0, "b": 4.0})
    # (3*4)+8 = 20.0
    assert float(result.content[0].text) == 20.0


async def test_mcp_tool_multiply_by_zero():
    async with Client(mcp) as client:
        result = await client.call_tool("multiply", {"a": 0.0, "b": 99.0})
    assert float(result.content[0].text) == 8.0


async def test_mcp_tool_meaning_of_life():
    async with Client(mcp) as client:
        result = await client.call_tool("meaning_of_life", {})
    assert result.content[0].text == "Manger des frites"


async def test_mcp_list_tools_contains_all():
    async with Client(mcp) as client:
        tools = await client.list_tools()
    tool_names = {t.name for t in tools}
    assert {"add", "multiply", "meaning_of_life"}.issubset(tool_names)


async def test_mcp_tool_add_has_description():
    async with Client(mcp) as client:
        tools = await client.list_tools()
    add_tool = next(t for t in tools if t.name == "add")
    assert add_tool.description is not None and len(add_tool.description) > 0

