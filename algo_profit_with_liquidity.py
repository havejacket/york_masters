import  logging, traceback
from datetime import datetime
import time
from utils import get_trade_routes, get_pair_data
from archive.mock_stream import get_next_pricing, get_next_ts
from archive.data_extraction import get_top_n

now = datetime.now()
filetime = now.strftime("%d-%m-%Y %H-%M-%S")

nowtime = now.strftime("%d/%m/%Y %H:%M:%S")

price_data=[]
profit_data=[]
bad_routes=[]

def make_money(algorithm_version="00", mock=False, all_routes=[]):
    #make some variable global; this was initially used to do mock trades
    #but has since been deprecated
    #retaining the format for backwards compatibility

    global profit_data
    global price_data
    global bad_routes
  
    #get the list of currency pairs on Luno
    pair_data = get_pair_data()

    #create a dictionary to hold trade data
    trade_data={}

    #iterate over the 34 trade routes in Luno
    for route in all_routes:       
        #stages allows the iterative calculation of liquidity
        #stages will hold the three stages of the triangular arbitrage
        stages=[]
        #initial and final trade values - used to calculate profit
        start_value=1
        final_start_value=start_value
        end_value=start_value 

        #used for debugging and testing: allows the analysis of a single route
        #all the way through
        showRoute= False #route==['XBT', 'ZAR', 'ETH']
            
        if showRoute:
            print(f"Route: {route}")
        
        for x in range(len(route)):
            #reset this leg of triangular arbitrage
            stage={}            
            #add the stage
            stages.append(stage)
            #a visual form of the trade, used for logging only
            output_trade=[]
            #the first currency
            c1=route[x]

            #optional debugging
            if showRoute:
                print(f"\tI have {end_value} of {c1}")

            #determining which direction on the trade pair
            #must be used to calculate this stage of the triangular arbitrage
            #start by assuming it is forward
            forward = True
            #build up the trading pair name
            if x+1==len(route):
                c2=route[0]
            else: 
                c2=route[x+1]
            #set the name into a variable
            trade=f"{c1}{c2}"            
            output_trade=[c1,c2]
            #look up the trading name in Luno's list of pairs
            if not trade in pair_data["pairs"]:
                #if it does not exist, then it must be a reverse trade
                trade=f"{c2}{c1}"
                forward=False
                output_trade=[c2,c1]
            #define the stages
            stage["c1"]=c1
            stage["c2"]=c2
            stage["trade"]=output_trade

            #check if we have capture this trade pair already
            if not trade in trade_data:
                
                #call the Luno API for trade data
                #this is rate limited to 300 TPS
                data = get_top_n(trade)
                
                #log the price data
                price_file = open(f"final_data/pricing_{algorithm_version}_{filetime}.csv", "a")
                #by default the top 100 are returned
                #trim this down- we only want the most recent one                
                asks=data["asks"][0]
                bids=data["bids"][0]
                data["asks"]=[asks]
                data["bids"]=[bids]
                data["trade"]=trade
                data["ts"]=nowtime
                #store the price data to local file
                print(data, file=price_file)
                price_file.close()

                trade_data[trade]=data
            else:
                #if we already retrieved this data then we will use that
                #this helps reduce API calls
                data = trade_data[trade]
            
            #extract Luno data for use in calculating profit
            ask = float(data["asks"][0]["price"])
            ask_volume=float(data["asks"][0]["volume"])
            bid = float(data["bids"][0]["price"])
            bid_volume = float(data["bids"][0]["volume"])

            #the direction is used to decide what pricing to use
            if forward:
                price=bid
                stage["direction"]="forward"
                stage["verb"]="sell"
                stage["price"] = price
                if bid_volume<end_value:
                    #the trade is throttled and the values are revised accordingly
                    if showRoute:
                        print(f"\tThrottled! I can only sell {bid_volume} of {c1} even though I have {end_value}")
                    end_value=bid_volume
                    #revise the start_value
                end_value*=price
            else:
                #reverse direction we use the other pricing
                price=ask
                stage["direction"]="reverse"
                stage["verb"]="buy"
                stage["price"] = price

                #and do the calculation differently
                potential_volume = end_value/price
                if ask_volume<potential_volume:
                    if showRoute:
                        print(f"\tThrottled! I can only buy {ask_volume} of {c2}, not the {potential_volume} that I can afford :(")

                    #throttle this to the available volume
                    end_value=ask_volume 
                else:
                    #no throttling needed, the available is more than is needed
                    end_value=potential_volume
            
            if showRoute:
                print(f"\tI now have {end_value} of {c2}\n")
    
        #the final value of the trade is calculated    
        final_start_value=end_value

        #to determine the start value needed to finish with this end value
        #simply iterate over the trade route in reverse:
        for x in range(len(stages)-1,-1,-1):
            stage=stages[x]
            if stage["verb"]=="sell":
                final_start_value/=stage["price"]
                #print(f"I needed {final_start_value} of {stage['c1']}")
            else:
                final_start_value*=stage["price"]
                #print(f"I needed {final_start_value} of {stage['c1']}")
        
        #final profit
        profit=end_value-final_start_value

        #debugging
        if showRoute:
            if profit>0:
                print(f"Profit", profit)
            else:
                print(f"Loss")
            
        #some output formatting for the profit file
        route_string=""
        for c in route:
            route_string=f"{route_string}->{c}"
        
        #result as profit or losee
        result=""
        #profit as a percentage
        percentage=0
        if profit>0:
            result="profit"
            percentage = 100 * profit/final_start_value
        
        #write the profit calculation to file
        f = open(f"final_data/profit_liquidity_{algorithm_version}.csv", "a")
        print(nowtime,route_string, profit, final_start_value, end_value, result, percentage, sep=",", file=f)
        f.close()
        

#the core function that gathers data from Luno and calculates profit
def run_algo(algorithm_version="00", mock=True, required_trades=10):
    #get the time for the creation of the initial file
    global nowtime
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    print("date and time =", dt_string)

    #track total trades agains input requirement
    trade_count=0

    #determine the cycle basis once    
    all_routes = get_trade_routes()

    #loop until the total trades have been collected
    while trade_count<required_trades:    
        try:
            now = datetime.now()
            nowtime = now.strftime("%d/%m/%Y %H:%M:%S")
            make_money(algorithm_version=algorithm_version, all_routes=all_routes)
            trade_count+=1
        except Exception as e:
            logging.error(traceback.format_exc())
            
        time.sleep(5)  #prevent hitting the Luno API limit of 300 calls per min

#entry point
if __name__ == '__main__':
    run_algo(algorithm_version="test_21", mock=False, required_trades=5)

