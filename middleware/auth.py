from fastapi import HTTPException
from starlette.requests import Request


async def require_apikey(request: Request):
    role = request.headers.get('finizi-api-key')
    if role != 'service':
        raise HTTPException(status_code=401, detail="Permission denied! Invalid role!")
