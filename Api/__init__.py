from fastapi import FastAPI , HTTPException 
from code import workflow 
from langchain_core.messages import HumanMessage
from pydantic import BaseModel 

class QuestionAnswer(BaseModel):
    questions : str 

app = FastAPI(title="langgraph")

@app.post("/chat")
def Chat_section(response:QuestionAnswer):
    try :
        content = workflow.invoke({
            'messages':[HumanMessage(content=response.questions)]
        })

        return content.content 
    except Exception as e :
        raise HTTPException(status_code=400 , detail=str(e)) 
