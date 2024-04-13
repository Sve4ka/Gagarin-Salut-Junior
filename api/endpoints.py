from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx
import db.db as db


app = FastAPI()


# ======================= получение токена доступа по !имейлу! и паролю естесна
class LoginData(BaseModel):
    email: str
    password: str
    device: str


@app.post("/get-access-token/")
async def get_access_token(login_data: LoginData):
    url = "https://mc.dev.rand.agency/api/v1/"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=login_data.dict(), headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        access_token = response.json()
        db.add_db("UPDATE user_table SET access_token=%s WHERE id_user=%s",
                  access_token, db.search_id_user_by_email(login_data.dict()["email"]))
        return access_token


# ==================================== поиск страницы
class PageData(BaseModel):
    name: str = Field(default="")
    slug: str
    birthday_at: str = Field(default="")
    died_at: str = Field(default="")
    slugs: list
    published_page: int
    page: dict


@app.post("/api/page/search/")
async def search_page(data: PageData, token: get_access_token):
    url = "https://mc.dev.rand.agency/api/page/search"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": token
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data.dict(), headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


#  ===================================== добавление комментария на страничку
class CommentData(BaseModel):
    page_id: int
    image_base64: str
    fio: str
    email: str = Field(default="")
    text: str
    relation_role: str
    checked: bool
    hasEmail: bool


@app.post("/api/comment/")
async def add_comment(comment_data: CommentData, token: get_access_token):
    url = "https://mc.dev.rand.agency/api/comment"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": token
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=comment_data.dict(), headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error")
        return response.json()