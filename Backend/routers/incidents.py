from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
import os
import json
from ..llm import get_llm
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

class IncidentRecord(BaseModel):
    id: str
    type: str
    location: str
    severity: str
    startTime: str
    description: str
    affectedEntities: List[str]
    status: str

@router.post("/generate", response_model=List[IncidentRecord])
def generate_incidents():
    try:
        llm = get_llm()
        
        prompt = "Act as a Supply Chain Risk Analyst and generate a JSON array of 5 realistic logistics/transportation disruptions (e.g., strikes, port closures) causing outrage; return strictly valid JSON with fields: id, type, location, severity, startTime, description, affectedEntities, status output ONLY the JSON.."
        
        message = HumanMessage(content=prompt)
        response = llm.invoke([message])
        
        # Initial parsing attempt
        content = response.content
        
        # Try to parse JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
            
        data = json.loads(content.strip())
        
        return data

    except Exception as e:
        print(f"Error generating incidents: {e}")
        # Return empty list or error
        raise HTTPException(status_code=500, detail=str(e))
