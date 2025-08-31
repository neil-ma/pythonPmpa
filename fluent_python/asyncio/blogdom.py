import asyncio
import socket
from keyword import kwlist

MAX_KEYWORD_LEN = 4


async def probe(domain: str) -> tuple[str, bool]:
    # 获取对asyncio事件循环的引用，供后续使用
    loop = asyncio.get_running_loop()
    try:
        # loop.getaddrinfo(…)是一个协程方法，返回一个包含五个参数的元组，这些参数用于通过socket连接到指定地址。
        # 本示例中无需使用该结果，只要能获取结果，就说明域名可解析；反之则不可解析
        # loop.getaddrinfo 的核心作用是将 “域名 + 端口” 或 “IP 地址 + 端口” 的组合，解析为底层网络连接所需的地址结构（如 IPv4/IPv6 地址、socket 类型等）。
        # 在异步编程场景中，它替代了标准库 socket 模块中阻塞式的 socket.getaddrinfo 函数，避免因 DNS 解析等耗时操作阻塞事件循环。
        await loop.getaddrinfo(domain, None)
        return (domain, True)
    except socket.gaierror:
        return (domain, False)


async def main() -> None:
    # 生成长度不超过MAX_KEYWORD_LEN的Python关键字
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
    # 生成以.dev为后缀的域名
    domains = (f'{name}.dev'.lower() for name in names)
    # 调用probe协程，为每个域名创建一个协程对象，并构建成列表
    coros = [probe(domain) for domain in domains]

    # asyncio.as_completed是一个生成器，它会按照协程完成的顺序（而非提交顺序），返回已完成的协程及其结果。
    # 这与我们在第20章示例20-4中看到的futures.as_completed类似
    for coro in asyncio.as_completed(coros):
        # 此时已知协程已完成（这是as_completed的特性），因此await表达式不会阻塞，但仍需通过它获取协程的结果。
        # 若协程抛出未处理的异常，此处会重新抛出该异常
        domain, found = await coro
        mark = '+' if found else ''
        print(f'{mark} {domain}')


if __name__ == '__main__':
    # asyncio.run会启动事件循环，直到事件循环退出后才返回结果。对于使用asyncio的脚本，
    # 这是一种常见模式：将main实现为协程，在if __name__ == '__main__':代码块中通过asyncio.run来驱动它
    asyncio.run(main())