from fastapi import FastAPI, Request
from agent.orchestration import dance_graph
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
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
        response = await graph.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )
        return response
    except Exception as e:
        return {"error": str(e)}
