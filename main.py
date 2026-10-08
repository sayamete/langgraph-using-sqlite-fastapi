from langgraph.graph import StateGraph ,START,END
from model import chat_model
from typing  import TypedDict , Annotated
from langchain_core.messages import  HumanMessage
from langgraph.graph.message import add_messages
class ChatState(TypedDict):
    messages : Annotated[list,add_messages]

graph = StateGraph(ChatState)

def chatModel(state:ChatState):
    response = chat_model.invoke(state['messages'])
    return {'messages' : [response.content]}

graph.add_node('chat_model',chatModel)

graph.add_edge(START,'chat_model')
graph.add_edge('chat_model',END)


workflow = graph.compile()
workflow

from fastapi import FastAPI , HTTPException 
from pydantic import BaseModel 

class QuestionAnswer(BaseModel):
    questions : str 

app = FastAPI(title="langgraph")

from fastapi.responses import FileResponse

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/chat")
def Chat_section(response:QuestionAnswer):
    try :
        content = workflow.invoke({
            'messages':[HumanMessage(content=response.questions)]
        })

        return content 
    except Exception as e :
        raise HTTPException(status_code=400 , detail=str(e)) 
