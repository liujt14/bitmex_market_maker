import sys
import time
import datetime
from market_maker.market_maker import OrderManager
from market_maker import bitmex
from market_maker.settings import settings
from market_maker.utils import log, constants, errors, math


logger = log.setup_custom_logger('root')


class CustomOrderManager(OrderManager):
    """A sample order manager for implementing your own custom strategy"""

    def place_orders(self) -> None:
        # implement your custom strategy here
        # my strategy
        for i in range(0, 10):
            i += 1
            bitmex_usd = bitmex.BitMEX(base_url=settings.BASE_URL, symbol="XBTUSD",
                                        apiKey=settings.API_KEY, apiSecret=settings.API_SECRET,
                                        orderIDPrefix=settings.ORDERID_PREFIX, postOnly=settings.POST_ONLY,
                                        timeout=settings.TIMEOUT)
            bitmex_u18 = bitmex.BitMEX(base_url=settings.BASE_URL, symbol="XBTU18",
                                         apiKey=settings.API_KEY, apiSecret=settings.API_SECRET,
                                         orderIDPrefix=settings.ORDERID_PREFIX, postOnly=settings.POST_ONLY,
                                         timeout=settings.TIMEOUT)
            buy_orders = []
            sell_orders = []
            # get ticker data
            # ticker data structure ticker = {
            #         "last": instrument['lastPrice'],
            #         "buy": bid,
            #         "sell": ask,
            #         "mid": (bid + ask) / 2
            #     }
            usd_ticker = bitmex_usd.ticker_data()
            u18_ticker = bitmex_u18.ticker_data()
            current_time = datetime.datetime.fromtimestamp(int(time.time()))
            logger.info("datetime: %s, last price of XBTUSD is %.*f" % (current_time, usd_ticker['last']))
            logger.info("last price of XBTU18 is %.*f" % u18_ticker['last'])
            time.sleep(1)
            usd_ticker_after = bitmex_usd.ticker_data()
            u18_ticker_after = bitmex_u18.ticker_data()
            after_datetime = datetime.datetime.fromtimestamp(int(time.time()))
            logger.info("datetime: %s, last price of XBTUSD is %.*f" % (after_datetime, usd_ticker_after['last']))
            logger.info("last price of XBTU18 is %.*f" % u18_ticker_after['last'])
            delta_usd = (usd_ticker_after['last']-usd_ticker['last'])*100/usd_ticker
            delta_u18 = (u18_ticker_after['last']-u18_ticker['last'])*100/u18_ticker
            if (delta_usd-delta_u18) > 5:
                buy_orders.append({'price': u18_ticker_after['sell'], 'orderQty': 100, 'side': "Buy"})

            # populate buy and sell orders, e.g.
            # buy_orders.append({'price': 999.0, 'orderQty': 100, 'side': "Buy"})
            # sell_orders.append({'price': 1001.0, 'orderQty': 100, 'side': "Sell"})

            self.converge_orders(buy_orders, sell_orders)


def run() -> None:
    order_manager = CustomOrderManager()

    # Try/except just keeps ctrl-c from printing an ugly stacktrace
    try:
        order_manager.run_loop()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()