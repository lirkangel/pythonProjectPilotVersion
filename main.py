import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends

from apis import apis_test
from config.cf import CONFIG
from conn import AppConnection

app = FastAPI(openapi_prefix='./')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'],
                   allow_credentials=True)


@app.on_event("startup")
async def init_connections():
    conn = AppConnection()
    await conn.init_connections()


@app.get('/healthcheck')
def health_check():
    return {
        'success': True
    }


app.include_router(
    apis_test.router,
    tags=["Account Job", "(internal only)"],
    # dependencies=[Depends(require_apikey)],
    responses={404: {
        "message": "Not found"
    }})

if __name__ == "__main__":
    uvicorn.run(app, host=CONFIG.FASTAPI_HOST, port=CONFIG.FASTAPI_PORT)
