# from subgraph.graph_states import ResearcherState
# from main_graph.graph_states import AgentState
# from utils.utils import config, new_uuid
# from subgraph.graph_builder import researcher_graph
# from main_graph.graph_builder import InputState, graph
# from langgraph.types import Command
# import asyncio
# import uuid
# #!/usr/bin/env python3

# import asyncio
# import time
# import builtins

# thread = {"configurable": {"thread_id": new_uuid()}}
# #This is a question related to environmental context. tell me the data center PUE efficiency value in Dublin in 2021

# async def process_query(query):
#     inputState = InputState(messages=query)

#     async for c, metadata in graph.astream(input=inputState, stream_mode="messages", config=thread):
#         if c.additional_kwargs.get("tool_calls"):
#             print(c.additional_kwargs.get("tool_calls")[0]["function"].get("arguments"), end="", flush=True)
#         if c.content:
#             time.sleep(0.05)
#             print(c.content, end="", flush=True)

#     # interrupt_obj = graph.get_state(thread)[-1][0]
#     # print(vars(interrupt_obj)) 
#     # if len(graph.get_state(thread)[-1]) > 0:
#     #     if len(graph.get_state(thread)[-1][0].interrupts) > 0:
#     #         response = input("\nThe response may contain uncertain information. Retry the generation? If yes, press 'y': ")
#     #         if response.lower() == 'y':
#     #             async for c, metadata in graph.astream(Command(resume=response), stream_mode="messages", config=thread):
#     #                 if c.additional_kwargs.get("tool_calls"):
#     #                     print(c.additional_kwargs.get("tool_calls")[0]["function"].get("arguments"), end="")
#     #                 if c.content:
#     #                     time.sleep(0.05)
#     #                     print(c.content, end="", flush=True)
#     state = graph.get_state(thread)
#     if state and len(state[-1]) > 0 and hasattr(state[-1][0], "interrupt_id"):
#         response = input("\nInterrupt detected. Retry generation? (y/n): ")
#         if response.lower() == 'y':
#             async for c, metadata in graph.astream(Command(resume=response), stream_mode="messages", config=thread):
#                 if c.additional_kwargs.get("tool_calls"):
#                     print(c.additional_kwargs.get("tool_calls")[0]["function"].get("arguments"), end="")
#                 if c.content:
#                     time.sleep(0.05)
#                     print(c.content, end="", flush=True)


# async def main():
#     input = builtins.input
#     print("Enter your query (type '-q' to quit):")
#     while True:
#         query = input("> ")
#         if query.strip().lower() == "-q":
#             print("Exiting...")
#             break
#         await process_query(query)


# if __name__ == "__main__":
#     asyncio.run(main())
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid
from main_graph.graph_builder import InputState, graph
from langgraph.types import Command
from utils.utils import new_uuid
from datetime import datetime
app = FastAPI()
# Allow your React dev server origin
origins = [
    "http://localhost:5173",  # Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # You can use ["*"] for all origins (not safe for prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

thread = {"configurable": {"thread_id": new_uuid()}}

class QueryRequest(BaseModel):
    query: str

class Message(BaseModel):
    id: str
    role: str
    content: str
    timestamp: str
@app.post("/api/messages")
async def process_query_endpoint(request: QueryRequest):
    query = request.query
    
    # Example: Create a user message first
    user_message = Message(
        id=str(uuid.uuid4()),
        role="user",
        topic=query,
        content=query,
        timestamp=datetime.utcnow().isoformat()
    )

    # Simulate assistant response collection
    results = []

    # Here you collect assistant replies (simulate for now)
    assistant_content = ""
    async for c, metadata in graph.astream(input=InputState(messages=query), stream_mode="messages", config=thread):
        if c.content:
            # Create a message object for assistant reply
            assistant_content += c.content
    assistant_message = Message(
                id=str(uuid.uuid4()),
                role="assistant",
                topic=query,
                content=assistant_content,
                timestamp=datetime.utcnow().isoformat()
            )
    results.append(assistant_message)

    return {"results": [user_message] + results}
# @app.post("/api/messages")
# async def process_query_endpoint(request: QueryRequest):
#     query = request.query
#     inputState = InputState(messages=query)
#     results = []

#     async for c, metadata in graph.astream(input=inputState, stream_mode="messages", config=thread):
#         # Collect content and tool_calls for response
#         if c.additional_kwargs.get("tool_calls"):
#             tool_call_args = c.additional_kwargs.get("tool_calls")[0]["function"].get("arguments")
#             results.append({"tool_call": tool_call_args})
#         if c.content:
#             # Simulate delay for demonstration
#             await asyncio.sleep(0.05)
#             results.append({"content": c.content})

#     return {"results": results}

# If you want to keep the interactive mode, run uvicorn separately.
