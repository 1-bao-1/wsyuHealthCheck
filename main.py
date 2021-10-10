"""
打卡接口v2.0实现思路
增加数据库，把打卡功能另起一个脚本，仅当用户访问特殊的端点或传入特殊的参数后才进行打卡。
数据库字段：
id: varchar(11) primary key
name: varchar(10)
addr: varchar default '武汉市'
valid: tinyint default true -- 判断用户是否为有效用户

智慧首义打卡接口v1.0 2021年10月9日21:36:58
不实现信息入库操作，只由用户请求接口并打卡。
slowapi 的要提供的参数名必须是 request 和 response
"""
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


from app import InvalidRequestParamException, check_request_params, health_check


app = FastAPI()


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={
        'code': 429,
        'message': '请求过于频繁'
    })


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


@app.get('/')
@limiter.limit("1/second")
async def root(request: Request):
    return {
        'message': '欢迎使用智慧首义打卡接口v1.0。访问 /check endpoint 获取更多信息。'
    }


@app.exception_handler(InvalidRequestParamException)
async def invalid_request_param_handler(request: Request, exc: InvalidRequestParamException):
    return JSONResponse(status_code=exc.code, content={
        'code': exc.code,
        'message': exc.message
    })


@app.get('/check')
@limiter.limit("5/minute")
async def check(request: Request, name: str = '', id: str = ''):
    check_request_params(name, id)

    return health_check(id, name)
