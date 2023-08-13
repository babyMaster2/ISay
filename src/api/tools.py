import random

import aiofiles


async def get_random_name():
    filename = 'name.txt'
    async with aiofiles.open(filename, 'r', encoding='utf-8') as f:
        names = await f.readlines()
        name = random.choice(names)
        return name.strip()
