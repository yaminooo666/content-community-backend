from fastapi import FastAPI
from database import engine,Base
from routers import posts,auth,vote,comments


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(comments.router)



