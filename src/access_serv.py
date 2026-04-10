import asyncio
from fastmcp import Client

async def main():
    client = Client("http://localhost:8000/sse")

    async with client:
        # Lister les outils disponibles
        tools = await client.list_tools()
        print("Outils disponibles :")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")

        # Appeler l'outil 'add'
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"\nadd(5, 3) = {result}")

if __name__ == "__main__":
    asyncio.run(main())
