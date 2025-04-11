from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.connection import engine
from models.user import Base as UserBase
from models.userProfile import Base as UserProfileBase
from models.follow import Base as FollowBase
from models.chatMessage import Base as ChatMessageBase
from models.comment import Base as CommentBase
from models.community import Base as CommunityBase
from models.communityComment import Base as CommunityCommentBase
from models.communityPost import Base as CommunityPostBase
from models.communityReply import Base as CommunityReplyBase
from models.communityUser import Base as CommunityUserBase
from models.personalChat import Base as PersonalChatBase
from models.vote import Base as VoteBase
from models.post import Base as PostBase
from models.commentVote import Base as CommentVoteBase
from models.reply import Base as ReplyBase
from models.voteReply import Base as ReplyVoteBase
from models.report import Base as ReportBase
from models.bookmark import Base as BookmarkBase   
from models.followThread import Base as FollowThreadBase   
from routes.login_route import login_router
from routes.user_route import profile_router
from routes.post_route import post_router
from routes.vote_route import vote_router
from routes.bookmark_route import bookmark_router
from routes.followedThread_route import followThread_router
from routes.comment_route import comment_router
from routes.commentVote_route import commentVote_router
from routes.reply_route import reply_router
from routes.replyVote_route import replyVote_router
from routes.follow_route import follow_router
from routes.chatMessage_route import chat_router
from routes.personalChat_route import personalChat_router

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
PostBase.metadata.create_all(bind=engine)    
VoteBase.metadata.create_all(bind=engine)    
BookmarkBase.metadata.create_all(bind=engine)    
FollowThreadBase.metadata.create_all(bind=engine)    
CommentBase.metadata.create_all(bind=engine)    
CommentVoteBase.metadata.create_all(bind=engine)    
ReplyBase.metadata.create_all(bind=engine)    
ReplyVoteBase.metadata.create_all(bind=engine)    
FollowBase.metadata.create_all(bind=engine)    
ChatMessageBase.metadata.create_all(bind=engine)    
PersonalChatBase.metadata.create_all(bind=engine)    

app.include_router(login_router, prefix="/user", tags=["User"])
app.include_router(profile_router, prefix="/profile", tags=["UserProfile"])
app.include_router(post_router, prefix="/post", tags=["Post"])
app.include_router(vote_router, prefix="/vote", tags=["Vote"])
app.include_router(bookmark_router, prefix="/bookmark", tags=["Bookmark"])
app.include_router(followThread_router, prefix="/thread", tags=["FollowThread"])
app.include_router(comment_router, prefix="/comment", tags=["Comment"])
app.include_router(commentVote_router, prefix="/voteComment", tags=["CommentVote"])
app.include_router(reply_router, prefix="/reply", tags=["Reply"])
app.include_router(replyVote_router, prefix="/voteReply", tags=["ReplyVote"])
app.include_router(follow_router, prefix="/follow", tags=["Follower"])
app.include_router(chat_router, prefix="/chat", tags=["ChatMessage"])
app.include_router(personalChat_router, prefix="/lastMessage", tags=["PersonalChat"])

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Server"}
