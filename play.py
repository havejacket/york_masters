
import os
from pytest import mark
from luno_python.client import Client
from datetime import date, datetime
import sched, time

# Get environment variables
key = os.getenv('LUNO_KEY')
secret = os.environ.get('LUNO_SECRET')

#schedule to tick every second
s = sched.scheduler(time.time, time.sleep)


def get_market_data():
    currencies=[]
    tickers = client.do('GET','/api/1/tickers')
    pairs = tickers["tickers"]
    market_data={}
    market_data["pairs"]={}
    market_data["currencies"]=currencies
    for t in pairs:
        pair=t["pair"]
        market_data["pairs"][pair]=t
        #print(pair, t["last_trade"])
        if "USDC" in pair:
            if "USDC" not in currencies:
                currencies.append("USDC")
            
            if pair[:4]=="USDC":
                other=pair[4:]
                currencies.append(other)
        else:
            cx=["",""]
            cx[0]=pair[:3]
            cx[1]=pair[3:]
            for c in cx:
                if c not in currencies:
                    currencies.append(c)
    return market_data

currencies=['USDC', 'BCH', 'XBT', 'MYR', 'LTC', 'NGN', 'ZAR', 'UNI', 'LIN', 'KMYR', 'XRP', 'ETH', 'EUR', 'GBP', 'AUD', 'IDR', 'UGX']
currencies=['USDC', 'NGN', 'ZAR', 'BCH', 'XBT', 'MYR', 'LTC', 'UNI', 'LIN', 'KMYR', 'XRP', 'ETH', 'EUR', 'GBP', 'AUD', 'IDR', 'UGX']

client = Client(api_key_id=key, api_key_secret=secret)

#res = c.get_ticker(pair='XBTZAR')
#print (res)


def do_trade(sc):

    data=get_market_data()
    #print(data)

    #step1 buy XBT
    start_cash=1e6
    xbt_zar=float(data["pairs"]["XBTZAR"]["ask"])
    #print(xbt_zar)
    xbt=start_cash/xbt_zar
    #print(f"i have {xbt} bitcoins")
    eth_xbt=float(data["pairs"]["ETHXBT"]["ask"])
    #print(eth_xbt)
    eth=xbt/eth_xbt
    #print(f"I have {eth} Etherium")
    eth_zar=float(data["pairs"]["ETHZAR"]["ask"])
    #print(eth_zar)
    end_cash=eth*eth_zar
    #print(f"I started with {start_cash} and I finished with {end_cash}")
    #print(f"I made a profit of", end_cash-start_cash)
    fee = start_cash*0.001*3
    now = datetime.now()
    nowtime = now.strftime("%d/%m/%Y %H:%M:%S")
    f = open("trades_01.csv", "a")
    print(nowtime,start_cash, xbt, eth, end_cash, abs(end_cash-start_cash), fee, sep=",", file=f)
    f.close()
    sc.enter(1, 1, do_trade, (sc,))

s.enter(1, 1, do_trade, (s,))
s.run()