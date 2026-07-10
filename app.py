import uvicorn
from pathlib import Path
import traceback

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from backend import run_travel_agent

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="TripMate AI Travel Booking Agent",
    description="An AI-powered travel booking agent that helps users plan and book their trips seamlessly.",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory = str(BASE_DIR / "static")),
    name= "static"
)

templates = Jinja2Templates(directory = str(BASE_DIR / "templates"))

class TravelRequest(BaseModel):
    message: str
    thread_id : str | None = None

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context = {}
    )


@app.post("/api/travel")
async def travel_planner(request: TravelRequest):
    try:
        user_data = request.message.strip()

        if not user_data:
            return JSONResponse(
                status_code = 400,
                content = {
                    "success": False,
                    "message": "User input is empty. Please provide a valid travel query."
                }
            )

        result = run_travel_agent(user_data, request.thread_id)

        return JSONResponse(
            status_code = 200,
            content = {
                "success": True,
                "thread_id": result["thread_id"],
                "answer": result["answer"],
                "flight_results": result["flight_results"],
                "hotel_results": result["hotel_results"],
                "itinerary": result["itinerary"],
                "llm_calls": result["llm_calls"]
                }
            )
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()

        return JSONResponse(
            status_code = 500,
            content={
                "success": False,
                "error": str(e)
    }
        )


@app.get("/api/health")
async def health_check():
    return JSONResponse(
        status_code = 200,
        content = {
            "success": True,
            "message": "API is healthy and running."
        }
    )

@app.get("/faicon.ico")
async def faicon():
    return JSONResponse(
     content = {}
 )

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host = "127.0.0.1",
        port = 8000,
        reload = True
    )













