from httpx import AsyncClient
from flags import main, BASE_URL, save_flag
import asyncio


async def get_flag(ac: AsyncClient, cc: str) -> bytes:
    # https://www.fluentpython.com/data/flags/CN/CN.gif
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    # httpx.AsyncClient 实例的get方法会返回一个ClientResponse对象，该对象同样是一个异步上下文管理器
    resp = await ac.get(url, timeout=6.1, follow_redirects=True)
    return resp.read()


async def download_one(ac: AsyncClient, cc: str) -> str:
    image = await get_flag(ac, cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc


async def supervisor(cc_list: list[str]):
    # AsyncClient是一个异步HTTP客户端、上下文管理器
    async with AsyncClient() as client:
        to_do = [download_one(client, cc) for cc in sorted(cc_list)]
        res = await asyncio.gather(*to_do)
    return len(res)


# 为了被main调用，该函数必须是普通函数
def download_many(cc_list: list[str]) -> int:
    # 将协程放入事件队列中
    return asyncio.run(supervisor(cc_list))


if __name__ == '__main__':
    main(download_many)
