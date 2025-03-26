from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.connection import engine
from models.user import Base as UserBase
from models.userProfile import Base as UserProfileBase
from models.follow import Base as FollowBase
from models.category import Base as CategoryBase
from models.chatMessage import Base as ChatMessageBase
from models.comment import Base as CommentBase
from models.community import Base as CommunityBase
from models.communityComment import Base as CommunityCommentBase
from models.communityPost import Base as CommunityPostBase
from models.communityReply import Base as CommunityReplyBase
from models.communityUser import Base as CommunityUserBase
from models.personalChat import Base as PersonalChatBase
from models.post import Base as PostBase
from models.reply import Base as ReplyBase
from models.report import Base as ReportBase
from models.savedThread import Base as SavedThreadBase
from routes.login_route import login_router
from routes.user_route import profile_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

UserBase.metadata.create_all(bind=engine) 
UserProfileBase.metadata.create_all(bind=engine)    

app.include_router(login_router, prefix="/user", tags=["User"])
app.include_router(profile_router, prefix="/profile", tags=["UserProfile"])

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Server"}
