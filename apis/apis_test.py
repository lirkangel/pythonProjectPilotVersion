import random
import string
from random import randint
from typing import Any

from fastapi import APIRouter, Request, HTTPException, status
from logzero import logger
from passlib.context import CryptContext

from conn import AppConnection
from models.apis_model import AuthRequest
from utils.funcs import get_path

router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post("/test")
async def test_api(payload: Any):
    logger.info(payload)
    return payload


@router.post("/create")
async def test_api(user: Request):
    a = await user.json()
    conn = AppConnection().mysql
    username = get_path(a, 'username')
    password = pwd_context.hash(get_path(a, 'password'))
    query_sql = "SELECT * FROM accounts WHERE username=%s"
    res = await conn.query(query_sql, username)
    if len(res) != 0:
        logger.info("account already exist")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'account already exist',
        )
    some = AuthRequest(username=username, password=password, email=get_path(a, 'email'))
    query_sql = "INSERT INTO accounts(username,password, email) values (%s, %s, %s)"
    await conn.query(query_sql, [some.username, some.password, some.email])
    return user


@router.post("/login")
async def login_api(payload: Any):
    logger.info(payload)
    return True


@router.post("/logout")
async def logout_api(payload: Any):
    logger.info(payload)
    return True


@router.get("/me")
async def self_information_api(payload: Any):
    logger.info(payload)
    return True


@router.post("/generate_accounts")
async def generate_account_api(payload: int):
    conn = AppConnection().mysql
    query_sql = "INSERT INTO accounts(username,password,email) values (%s, %s, %s)"
    for x in range(0, payload):
        some = AuthRequest(username=f'0{randint(99999999, 999999999)}', password=pwd_context.hash('123456'),
                           email=f'{random_char(10)}@{random_char(5)}.com')
        await conn.query(query_sql, [some.username, some.password, some.email])
    return True


def random_char(char_num):
    return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))
