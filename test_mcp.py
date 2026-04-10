# Les tests sont organisés dans le dossier tests/ :
#   tests/test_data_access.py      — src/dataAccess.py
#   tests/test_data_processing.py  — src/dataProcessing.py
#   tests/test_prediction_model.py — src/prediction_model.py
#   tests/test_server.py           — src/server.py (intégration MCP)
#
# Lancer tous les tests :  pytest

# ─────────────────────────────────────────────
# Test de connexion au serveur MCP live
# Le serveur MCP doit être démarré avant : uv run src/server.py
# ─────────────────────────────────────────────
import asyncio
from fastmcp import Client

MCP_URL = "http://localhost:8080/mcp/"


async def test_connection():
    """Teste la connexion au serveur MCP via SSE et liste les outils disponibles."""
    print(f"\nConnexion au serveur MCP : {MCP_URL}")
    async with Client(MCP_URL) as client:
        tools = await client.list_tools()
        print(f"Connexion réussie — {len(tools)} outil(s) disponible(s) :")
        for tool in tools:
            print(f"  • {tool.name} : {tool.description}")
    return tools


async def test_predict_price_live():
    """Appelle l'outil predict_price sur le serveur live."""
    async with Client(MCP_URL) as client:
        result = await client.call_tool("predict_price", {
            "surface_reelle_bati": 80.0,
            "surface_terrain": 120.0,
            "nombre_pieces_principales": 4,
            "type_local": "Maison",
        })
    print(f"\nRésultat predict_price : {result}")
    return result


if __name__ == "__main__":
    asyncio.run(test_connection())
    asyncio.run(test_predict_price_live())

import httpx
r = httpx.get('http://localhost:8080/sse', timeout=3)
print('Status:', r.status_code)