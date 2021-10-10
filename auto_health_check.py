from datetime import datetime

import pytz

from tortoise import Tortoise, run_async

from db import Student
from app import health_check


async def init_db():
    await Tortoise.init(db_url='sqlite://db.sqlite',
                        modules={'module': ['db.model']}, timezone='Asia/Shanghai')


async def main():
    await init_db()

    # 获取今天的日期
    now = datetime.now(tz=pytz.timezone('Asia/Shanghai'))
    date = datetime(now.year, now.month, now.day)

    # 找出上次打卡时间比今天小的数据，打卡
    for stu in await Student.filter(last_check__lt=date):
        succ, _ = health_check(stu.id, stu.name)

        if succ:
            print(stu.name, '打卡成功')
            Student.get(id=stu.id).update(last_check=datetime.utcnow())

    await Tortoise.close_connections()


if __name__ == '__main__':
    run_async(main())
