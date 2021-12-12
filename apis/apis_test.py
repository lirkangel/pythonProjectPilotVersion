import logzero
from random import randint
from typing import Any

from fastapi import APIRouter
from passlib.context import CryptContext

from conn import AppConnection
from models.apis_model import AuthBody

router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post("/test")
async def test_api(payload: Any):
    logzero.logger.info(payload)
    return payload


@router.post("/login")
async def login_api(payload: Any):
    logzero.logger.info(payload)
    return True


@router.post("/logout")
async def logout_api(payload: Any):
    logzero.logger.info(payload)
    return True


@router.get("/me")
async def self_information_api(payload: Any):
    logzero.logger.info(payload)
    return True


@router.post("/generate_accounts")
async def generate_account_api(payload: int):
    conn = AppConnection().mysql
    query_sql = "INSERT INTO accounts(username,password) values (%s, %s)"
    for x in range(0, payload):
        some = AuthBody(username=f'0{randint(99999999, 999999999)}', password=pwd_context.hash('123456'))
        await conn.query(query_sql, [some.username, some.password])
    return True
