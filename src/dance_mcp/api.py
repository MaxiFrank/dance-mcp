from fastapi import FastAPI, Request
from agent.orchestration import dance_graph
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chats")
async def chats(request: Request):
    try:
        body = await request.json()
        user_input = body.get("message", "")
        graph = dance_graph.set_up_graph()
        print("=== Graph execution starting ===")
        response = await graph.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )
        print("=== Graph execution completed ===")
        print("Final response:", str(response))
        print("Response messages count:", len(response.get("messages", [])))
        return response
    except Exception as e:
        return {"error": str(e)}

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("src.dance_mcp.api:app", host="0.0.0.0", port=8000, reload=True)

