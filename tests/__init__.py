import asyncio
from pprint import pprint

import random


async def coro(tag):
    print(">", tag)
    await asyncio.sleep(random.uniform(1, 3))
    print("<", tag)
    return tag


loop = asyncio.get_event_loop()

group1 = asyncio.gather(*[coro("group 1.{}".format(i)) for i in range(1, 6)])
group2 = asyncio.gather(*[coro("group 2.{}".format(i)) for i in range(1, 4)])
group3 = asyncio.gather(*[coro("group 3.{}".format(i)) for i in range(1, 10)])

all_groups = asyncio.gather(group1, group2, group3)

results = loop.run_until_complete(all_groups)

loop.close()

pprint(results)


"""
Inicio 10
Inicio 80
Inicio 100
Inicio 300
Inicio 20
Inicio 30
Inicio 40
Inicio 50
Inicio 60
Inicio 70
Inicio 130
Inicio 220
Inicio 340
Inicio 240
Inicio 280
Inicio 360
Inicio 320
Inicio 380
Inicio 400
Inicio 420
Inicio 500
Inicio 550
Inicio 620
Inicio 105600
Inicio 268910
Inicio 322170
Inicio 327690
Inicio 297130
Inicio 367520
Inicio 312530
Inicio 386940
Inicio 291550
Inicio 454100
Inicio 504230
Inicio 774361
Inicio 871720
Inicio 728880
Inicio 945360
Inicio 730
Inicio 450390
Inicio 1515950
Inicio 239140
Inicio 346110
Inicio 407530
Inicio 40990
Fin 220
Fin 80
Fin 70
Fin 322170
Fin 240
Fin 300
Fin 320
Fin 60
Fin 620
Fin 30
Fin 360
Fin 367520
Fin 407530
Fin 40990
Fin 312530
Fin 268910
Fin 500
Fin 40
Fin 945360
Fin 327690
Fin 400
Fin 297130
Fin 550
Fin 100
Fin 291550
Fin 20
Fin 504230
Fin 871720
Fin 450390
Fin 730
Fin 10
Fin 1515950
Fin 50
Fin 105600
Fin 454100
Fin 386940
Fin 728880
Fin 420
Fin 380
Fin 280
Fin 340
Fin 346110
Fin 774361
Fin 239140
Fin 130
"""