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
git clone <https://github.com/yaminooo666/content-community-backend>
cd <content-community-backend>