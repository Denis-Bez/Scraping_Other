import asyncio
import time

async def main():
    var1 = 0
    for i in range(0, 2):
        var1 += 1
    print(var1)

if __name__ == '__main__':
    asyncio.run(main())