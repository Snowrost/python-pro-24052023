from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import user_info, participant_info, feedback_info, check_info
from api.endpoints import meeting_info, custom_item_info

app = FastAPI()

origins = [
    "http://localhost:3000",  # Add your React frontend URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_info.router, prefix="/users",)
app.include_router(meeting_info.router, prefix="/meetings")
app.include_router(participant_info.router, prefix="/participant")
app.include_router(feedback_info.router, prefix="/feedback")
app.include_router(custom_item_info.router, prefix="/custom")
app.include_router(check_info.router, prefix="/check")
