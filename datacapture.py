"""
Collecting all data from poloniex for future use in back testing.
"""

import asyncio
from autobahn.asyncio.wamp import ApplicationSession
from autobahn.asyncio.wamp import ApplicationRunner
from asyncio import coroutine
import time, datetime


class PoloniexComponent(ApplicationSession):

    def onConnect(self):
        self.join(self.config.realm)

    async def onJoin(self, details):
        def on_event(*i):
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
            print(st, i)
            file = open("logs/ticks.log", "a")
            file.write(st + " " + str(i) + "\n")
            file.close()

        def on_usdt_btc(*i, seq):
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
            print(st, seq, i)
            file = open("logs/usdt_eth.log", "a")
            file.write(st + " " + str(seq) + " " + str(i) + "\n")
            file.close()

        def on_usdt_eth(*i, seq):
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
            print(st, seq, i)
            file = open("logs/usdt_btc.log", "a")
            file.write(st + " " + str(seq) + " " + str(i) + "\n")
            file.close()

        def on_btc_eth(*i, seq):
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
            print(st, seq, i)
            file = open("logs/btc_eth.log", "a")
            file.write(st + " " + str(seq) + " " + str(i) + "\n")
            file.close()

        try:
            await self.subscribe(on_event, 'trollbox')
            await self.subscribe(on_event, 'ticker')
            await self.subscribe(on_usdt_btc, 'USDT_BTC')
            await self.subscribe(on_usdt_eth, 'USDT_ETH')
            await self.subscribe(on_btc_eth, 'BTC_ETH')
        except Exception as e:
            print("Could not subscribe to topic:", e)






    def onDisconnect(self):
        asyncio.get_event_loop().stop()


def main():
    runner = ApplicationRunner("wss://api.poloniex.com:443", "realm1")
    runner.run(PoloniexComponent)


if __name__ == "__main__":
    main()