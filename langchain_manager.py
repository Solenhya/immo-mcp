import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage, SystemMessage, BaseMessage
from langchain_core.tools import BaseTool
from langgraph.graph import StateGraph, MessagesState, END
from dotenv import load_dotenv
load_dotenv()

# Le serveur MCP doit être démarré avant : uv run server.py
MCP_URL = "http://localhost:8080/sse"



class WorkFlowState(MessagesState):
    pass



class LangchainManager:

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.llm = None
        self.llm_tools = None
        self.graph = None

    @classmethod
    async def create(cls, model_name: str):
        instance = cls(model_name)
        await instance.init_model()
        return instance

    async def init_model(self):
        self.llm = ChatMistralAI(model=self.model_name)
        self.client = MultiServerMCPClient(
            {
                "dev": {
                    "url": MCP_URL,
                    "transport": "sse",
                }
            }
        )
        self.tools = await self.client.get_tools()
        self.tools_by_name: dict[str, BaseTool] = {t.name: t for t in self.tools}
        self.graph = (
            StateGraph(MessagesState)
            .add_node("model", self.call_model)
            .add_node("tools", self.tool_node)
            .set_entry_point("model")
            .add_conditional_edges("model", self.should_call_tools, {"tools": "tools", END: END})
            .add_edge("tools", "model")
            .compile()
        )
    
    def get_model_tools(self):
        if self.llm_tools is None:
            self.llm_tools = self.llm.bind_tools(self.tools)
        return self.llm_tools
    
        # --- Nœuds ---
    async def call_model(self,state: MessagesState) -> dict:
        """Appelle le modèle avec les messages en contexte et retourne un dict avec une liste de messages (incluant potentiellement des tool_calls)."""
        response = await self.get_model_tools().ainvoke(state["messages"])
        return {"messages": [response]}

    async def tool_node(self,state: MessagesState) -> dict:
        """Exécute les tool_calls du dernier message et retourne des ToolMessages avec content string."""
        last_message = state["messages"][-1]
        tool_messages = []
        for tool_call in last_message.tool_calls:
            tool = self.tools_by_name[tool_call["name"]]
            result = await tool.ainvoke(tool_call["args"])
            print(f"Resultat brut de l'appel à l'outil '{tool_call['name']}': {result}")
            result = result[0] if isinstance(result, list) and len(result) == 1 else result

            if isinstance(result, dict) and "text" in result:
                result = result["text"]
            print(f"Resultat de l'appel à l'outil '{tool_call['name']}': {result}")
            tool_messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                    name=tool_call["name"],
                ))
        return {"messages": tool_messages}
    
    def should_call_tools(self, state: WorkFlowState) -> str:
        """Retourne 'tools' si le dernier message contient des tool_calls, sinon END."""
        last_message = state["messages"][-1]
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "tools"
        return END

    async def run(self, initial_messages: list[BaseMessage]):
        response = await self.graph.ainvoke(
            {"messages": initial_messages}
        )

        for message in response["messages"]:
            print(f"[{message.type}] {message.content}")

        return response["messages"]
    
async def main():
    langchain_manager = await LangchainManager.create(model_name="mistral-large-latest")
    prompt = f"""Tu es un expert immobilier. Utilise systématiquement l'outil estimer_prix pour donner des chiffres précis plutôt que de faire des suppositions."""
    initial_messages = [
        SystemMessage(prompt)
    ]
    running = True
    while running:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            running = False
            continue

        initial_messages.append(HumanMessage(content=user_input))
        response = await langchain_manager.run(initial_messages)
        initial_messages = list(response)

if __name__ == "__main__":
    asyncio.run(main())