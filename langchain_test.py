import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import BaseTool
from langgraph.graph import StateGraph, MessagesState, END
from dotenv import load_dotenv
load_dotenv()

# Le serveur MCP doit être démarré avant : uv run server.py
MCP_URL = "http://localhost:8000/sse"

def should_call_tools(state: MessagesState) -> str:
    """Retourne 'tools' si le dernier message contient des tool_calls, sinon END."""
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    return END


async def main():
    llm = ChatMistralAI(model="mistral-large-latest")

    client = MultiServerMCPClient(
        {
            "demo": {
                "url": MCP_URL,
                "transport": "sse",
            }
        }
    )
    tools = await client.get_tools()
    print(f"Outils chargés : {[t.name for t in tools]}\n")

    llm_with_tools = llm.bind_tools(tools)

    # --- Nœuds ---
    async def call_model(state: MessagesState) -> dict:
        response = await llm_with_tools.ainvoke(state["messages"])
        return {"messages": [response]}

    tools_by_name: dict[str, BaseTool] = {t.name: t for t in tools}

    async def tool_node(state: MessagesState) -> dict:
        """Exécute les tool_calls du dernier message et retourne des ToolMessages avec content string."""
        last_message = state["messages"][-1]
        tool_messages = []
        for tool_call in last_message.tool_calls:
            tool = tools_by_name[tool_call["name"]]
            result = await tool.ainvoke(tool_call["args"])
            tool_messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                    name=tool_call["name"],
                )
            )
        return {"messages": tool_messages}

    # --- Graphe ---
    graph = (
        StateGraph(MessagesState)
        .add_node("model", call_model)
        .add_node("tools", tool_node)
        .set_entry_point("model")
        .add_conditional_edges("model", should_call_tools, {"tools": "tools", END: END})
        .add_edge("tools", "model")
        .compile()
    )

    # --- Invocation ---
    response = await graph.ainvoke(
        {"messages": [{"role": "user", "content": "Combien font 12 + 30 ?"}]}
    )

    for message in response["messages"]:
        print(f"[{message.type}] {message.content}")

if __name__ == "__main__":
    asyncio.run(main())
