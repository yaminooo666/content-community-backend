# Content Community Backend

一个基于 FastAPI 和 SQLAlchemy 实现的内容社区后端，支持用户注册登录、发帖、更新、评论、点赞、分类、搜索与分页查询，并接入 Gemini API 自动生成帖子摘要；当帖子内容更新时，摘要会同步重算，调用失败时提供本地兜底摘要。

## Tech Stack
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Gemini API

## Highlights
1. 面向内容社区场景的完整后端实现：支持注册登录、发帖、更新、评论、点赞、分类、帖子详情、搜索与分页查询。
2. 集成帖子摘要自动生成能力：发帖时调用 Gemini API 生成摘要，更新帖子后自动重算，并为接口调用失败提供本地兜底逻辑。
3. 采用较完整的后端工程实践：使用 JWT 鉴权、Pydantic Schema、SQLAlchemy relationship、joinedload 查询优化，以及评论逻辑删除机制。


## Core Features

- User authentication with JWT
- Create, update and view posts
- Post list with search, author filter and pagination
- Category support for posts
- Comment creation, listing and logical deletion
- Vote count for posts
- Automatic summary generation with Gemini API
- Summary regeneration after post updates
- Fallback summary when AI generation fails

## How to Run

### 1. Clone the project
```bash
git clone <your-repo-url>
cd <your-project-folder>




## API Overview

### Auth
- `POST /login` - 用户登录

### Posts
- `POST /posts/` - 创建帖子并生成摘要
- `GET /posts/` - 获取帖子列表（支持分页、搜索、作者筛选）
- `GET /posts/{post_id}` - 获取单个帖子详情
- `PATCH /posts/{post_id}` - 更新帖子并重新生成摘要

### Comments
- `POST /posts/{post_id}/comments` - 创建评论
- `GET /posts/{post_id}/comments` - 获取某篇帖子的评论列表
- `DELETE /posts/{post_id}/comments/{comment_id}` - 逻辑删除评论

### Votes
- `POST /vote` - 点赞或取消点赞