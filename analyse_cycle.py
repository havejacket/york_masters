from utils import get_trade_routes

def run_analysis(USE_LIQUIDITY=False, algorithm_version="08", cycle="->XBT->MYR->BCH"):
    if USE_LIQUIDITY:
        filename=f"final_data/profit_liquidity_{algorithm_version}.csv"
        liquidity_string="with_liquidity"
    else:
        filename=f"final_data/profit_no_liquidity_{algorithm_version}.csv"
        
        liquidity_string="no_liquidity"

    f = open(f"{filename}", "r")
    cycle_clean=cycle.replace("->","_")



    out_file = open(f"final_data/routes/{cycle_clean}-{algorithm_version}.csv", "w")
    #nowtime,route_string, profit, final_start_value, end_value, result, percentage
    out_file.write("timestamp,route,profit,final_start_value,end_value,result,percentage\n")
    previous_dedupe=""
    dedupe_count=0
    for raw in f:
        dedupe=raw[21:]
        row=raw.split(",")               
        file_cycle=row[1]       
        profit=float(row[2])

        if file_cycle==cycle:
            if profit>0:
                if dedupe!=previous_dedupe or 1==1:

                    out_file.write(raw)
                    #out_file.write("\n")
                else:
                    dedupe_count+=1
                previous_dedupe = dedupe
    
    f.close()
    out_file.close()
    print("Removed",dedupe_count,"duplicates")

if __name__ == '__main__':
    algorithm_version= "24"
    for route in get_trade_routes():
        cycle=""
        for currency in route:
            cycle+=f"->{currency}"
        run_analysis(USE_LIQUIDITY= True,algorithm_version= algorithm_version,cycle = cycle)
    
