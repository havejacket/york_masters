import json


def run_analysis(USE_LIQUIDITY=False, algorithm_version="08"):
    if USE_LIQUIDITY:
        filename=f"final_data/profit_liquidity_{algorithm_version}.csv"
        liquidity_string="with_liquidity"
    else:
        filename=f"final_data/profit_no_liquidity_{algorithm_version}.csv"
        liquidity_string="no_liquidity"

    f = open(f"{filename}", "r")

    cycles={}

    start_ts=0
    end_ts=0
    trades=0
    profitable_trades=0
    total_profit=0
    total_high_fee_profit=0
    total_low_fee_profit=0
    total_traded=0
    total_low_fee_trades=0
    total_high_fee_trades=0

    for raw in f:
        row=raw.split(",")
        trades+=1
        ts=row[0]
        if start_ts==0:
            start_ts=ts
        end_ts=ts
        cycle=row[1]
        
        profit=float(row[2])
        if USE_LIQUIDITY:
            traded=float(row[3])
        else:
            traded=1
        if cycle not in cycles:
            cycles[cycle]={}
            cycles[cycle]["total_trades"]=0
            cycles[cycle]["profitable_trades"]=0
            cycles[cycle]["profit"]=0
            cycles[cycle]["profit_highfee_adjusted"]=0
            cycles[cycle]["profit_lowfee_adjusted"]=0
            cycles[cycle]["best_trade"]=0
            cycles[cycle]["total_traded"]=0
            
            cycles[cycle]["profitable_low_fee_trades"]=0
            cycles[cycle]["profitable_high_fee_trades"]=0
        cycles[cycle]["total_trades"]+=1
        if profit>0:
            profitable_trades+=1
            
            cycles[cycle]["profitable_trades"]+=1
            cycles[cycle]["profit"]+=profit
            cycles[cycle]["best_trade"]=max(profit, cycles[cycle]["best_trade"])
            cycles[cycle]["total_traded"]+=traded
            

            #There are 3 trades in each cycle, so total fee is 3 * fee.
            #Highest fee is 0.1%. 
            high_fee_profit=profit-3*0.001*traded
            if high_fee_profit>0:
                cycles[cycle]["profit_highfee_adjusted"]+=high_fee_profit
                total_high_fee_profit+=high_fee_profit
                cycles[cycle]["profitable_high_fee_trades"]+=1
                total_high_fee_trades+=1
    
            #Lowest fee is 0.03%. 
            low_fee_profit=profit-3*0.0003*traded
            if low_fee_profit>0:
                cycles[cycle]["profit_lowfee_adjusted"]+=low_fee_profit
                total_low_fee_profit+=low_fee_profit
                cycles[cycle]["profitable_low_fee_trades"]+=1
                
                total_low_fee_trades+=1

            total_profit+=profit
            total_traded+=traded
          


    results={}
    results["cycles"]=cycles
    if USE_LIQUIDITY:
        type="Results WITH Liquidity"
    else:
        type="Results WITHOUT Liquidity"
    results["analysis_type"]=type
    results["total_trade_opportunities"]=trades
    results["profitable_trades"]=profitable_trades
    results["total_profit"]=total_profit
    results["total_traded"] =total_traded
    results["total_high_fee_profit"]=total_high_fee_profit
    results["total_low_fee_profit"]=total_low_fee_profit
    results["profitable_low_fee_trades"]=total_low_fee_trades
    results["profitable_high_fee_trades"]=total_high_fee_trades

    f = open(f"results/algo_{algorithm_version}_{liquidity_string}.json", "w")
    f.write(json.dumps(results))
    f.close()

def create_csv(algorithm_version, USE_LIQUIDITY):
    if USE_LIQUIDITY:
        liquidity_string="with_liquidity"
    else:
        liquidity_string="no_liquidity"
    filename = f"results/algo_{algorithm_version}_{liquidity_string}.json"

    f = open(filename, "r")
    data = json.load(f)
    f.close()

    def write_array(a, f):
        for e in a:
            f.write(str(e))
            f.write(",")
        f.write("\n")

    headers=[]
    for cycle in data["cycles"]:
        headers.append("route")
        for key in data["cycles"][cycle]:
            headers.append(key)
        break
    #print(headers)

    f=open(f"results/visual_{algorithm_version}_{liquidity_string}.csv", "w")
    write_array(headers, f)

    for cycle in data["cycles"]:
        route=[]
        route.append(cycle)
        for key in data["cycles"][cycle]:
            route.append(data["cycles"][cycle][key])
        write_array(route, f)
    f.close()



algorithm_version="test_21"
#run_analysis(USE_LIQUIDITY=False, algorithm_version=algorithm_version)
run_analysis(USE_LIQUIDITY=True, algorithm_version=algorithm_version)
create_csv(USE_LIQUIDITY=True, algorithm_version=algorithm_version)



