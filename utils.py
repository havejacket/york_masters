import networkx as nx
import matplotlib.pyplot as plt

#This method parses the rates table and extracts the basis cycle
#It also generates a visual currency graph
def parse_rates(DRAW_GRAPH=False):
    counts={}
    edges=0
    vertices=0

    #declare a NetworkX graph object
    G = nx.Graph()

    #This is real pair data from the Luno API, pasted here for ease of reading
    #The list of trade pairs changes perhaps once a year, so this data is in little danger of becoming stale
    pair_data = get_pair_data()

    #Iterate over the trade pairs, first parsing out the currencies
    #Annoyingly two of them use FOUR characters in their names, and need to be extracted explicitly
    for pair in pair_data["pairs"]:
        #c1 = currency 1
        #c2 = currency 2
        #each trade pair has two currencies
        #a trade goes FROM c1 TO c2
        if pair[:4]=="USDC":
            c1="USDC"
            c2=pair[4:]
        elif pair[3:]=="USDC":
            c1=pair[:3]
            c2="USDC"
        elif pair[:4]=="LINK":
            c1="LINK"
            c2=pair[4:]
        elif pair[3:]=="LINK":
            c1=pair[:3]
            c2="LINK"
        else:
            c1=pair[:3]
            c2=pair[3:]
        
        #add them to a tracking dictionary
        #and count the edges and vertices
        if not c1 in counts:
            counts[c1]=0
            vertices+=1
        if not c2 in counts:
            counts[c2]=0
            vertices+=1
        
        edges+=1
        counts[c1]+=1
        counts[c2]+=1
        
        #populate the graph, adding currencies as vertices 
        #with an edge between two that have a trade route
        #note that the weight is 1 because the profit calculation is done 
        #in other code

        #Recall that G = nx.Graph() from NetworkX
        G.add_edge(c1, c2, weight=1)
        G.add_edge(c2, c1, weight=1)

    #print a summary
    #print(vertices,"vertices, and",edges,"edges")
    #print("Expect",(edges-vertices+1),"cycles in the basis")

    #extract the cycle basis
    basis_cycles = nx.cycle_basis(G)
    #print("Basis cycles:")
    maxlen=0
    for c in basis_cycles:
        maxlen=max(maxlen, len(c))

    #print("Total number of cycles in the basis:", len(basis_cycles))
    #print("The longest basis cycle is", maxlen)
    

    #print(basis_cycles)

    if DRAW_GRAPH:
        #draw the graph
        nx.draw_networkx(G)
    return basis_cycles


def get_basis_cycles():
    creation_count=0
    basis_error=True
    basis = None
    while basis_error:
        creation_count+=1
        basis_error=False
        print("Basis iteration", creation_count)
        basis = parse_rates()
        maxlen=0
        
        for c in basis:
            maxlen=max(maxlen, len(c))
            if "XBT" not in c:
                basis_error=True
                print("XBT not found in", c)
                print("This is a fatal error, quitting now.")
                exit(1)
        if maxlen>3:
            basis_error=True
            print("Found a cycle with more than 3 currencies")
            exit(1)
        
    return basis

#returns pair data as if from the Luno API
def get_pair_data():
    pair_data = {"pairs": {"USDCNGN": {"pair": "USDCNGN", "timestamp": 1662394005461, "bid": "698.51000000", "ask": "702.00000000", "last_trade": "698.51000000", "rolling_24_hour_volume": "1104.93000000", "status": "ACTIVE"}, "USDCZAR": {"pair": "USDCZAR", "timestamp": 1662394005461, "bid": "17.38000000", "ask": "17.40000000", "last_trade": "17.38000000", "rolling_24_hour_volume": "47517.48000000", "status": "ACTIVE"}, "BCHXBT": {"pair": "BCHXBT", "timestamp": 1662394005461, "bid": "0.00602100", "ask": "0.00659900", "last_trade": "0.00660000", "rolling_24_hour_volume": "385.46000000", "status": "ACTIVE"}, "BCHMYR": {"pair": "BCHMYR", "timestamp": 1662394005461, "bid": "553.00000000", "ask": "554.00000000", "last_trade": "554.00000000", "rolling_24_hour_volume": "408.59190000", "status": "ACTIVE"}, "LTCXBT": {"pair": "LTCXBT", "timestamp": 1662394005461, "bid": "0.00304600", "ask": "0.00304900", "last_trade": "0.00304500", "rolling_24_hour_volume": "380.23000000", "status": "ACTIVE"}, "LTCMYR": {"pair": "LTCMYR", "timestamp": 1662394005461, "bid": "271.00000000", "ask": "272.00000000", "last_trade": "272.00000000", "rolling_24_hour_volume": "1884.96470000", "status": "ACTIVE"}, "LTCNGN": {"pair": "LTCNGN", "timestamp": 1662394005461, "bid": "41505.00000000", "ask": "42499.00000000", "last_trade": "42498.00000000", "rolling_24_hour_volume": "35.33630000", "status": "ACTIVE"}, "LTCZAR": {"pair": "LTCZAR", "timestamp": 1662394005461, "bid": "1053.00000000", "ask": "1054.00000000", "last_trade": "1053.00000000", "rolling_24_hour_volume": "3558.02530000", "status": "ACTIVE"}, "UNIMYR": {"pair": "UNIMYR", "timestamp": 1662394005461, "bid": "28.63000000", "ask": "28.64000000", "last_trade": "28.64000000", "rolling_24_hour_volume": "20479.33000000", "status": "ACTIVE"}, "LINKMYR": {"pair": "LINKMYR", "timestamp": 1662394005461, "bid": "33.04000000", "ask": "33.06000000", "last_trade": "33.04000000", "rolling_24_hour_volume": "8534.12000000", "status": "ACTIVE"}, "XRPXBT": {"pair": "XRPXBT", "timestamp": 1662394005461, "bid": "0.00001652", "ask": "0.00001653", "last_trade": "0.00001652", "rolling_24_hour_volume": "400870.00000000", "status": "ACTIVE"}, "XRPMYR": {"pair": "XRPMYR", "timestamp": 1662394005461, "bid": "1.47620000", "ask": "1.47630000", "last_trade": "1.47620000", "rolling_24_hour_volume": "1069269.00000000", "status": "ACTIVE"}, "XRPNGN": {"pair": "XRPNGN", "timestamp": 1662394005461, "bid": "229.10000000", "ask": "229.95000000", "last_trade": "229.95000000", "rolling_24_hour_volume": "14649.00000000", "status": "ACTIVE"}, "XRPZAR": {"pair": "XRPZAR", "timestamp": 1662394005461, "bid": "5.71000000", "ask": "5.72000000", "last_trade": "5.72000000", "rolling_24_hour_volume": "1727347.00000000", "status": "ACTIVE"}, "ETHUSDC": {"pair": "ETHUSDC", "timestamp": 1662394005461, "bid": "1608.00000000", "ask": "1608.16000000", "last_trade": "1608.00000000", "rolling_24_hour_volume": "58.39550000", "status": "ACTIVE"}, "ETHXBT": {"pair": "ETHXBT", "timestamp": 1662394005461, "bid": "0.08068000", "ask": "0.08068900", "last_trade": "0.08068900", "rolling_24_hour_volume": "73.16000000", "status": "ACTIVE"}, "ETHEUR": {"pair": "ETHEUR", "timestamp": 1662394005461, "bid": "1608.87000000", "ask": "1619.98000000", "last_trade": "1605.30000000", "rolling_24_hour_volume": "2.28910000", "status": "ACTIVE"}, "ETHGBP": {"pair": "ETHGBP", "timestamp": 1662394005461, "bid": "1350.01000000", "ask": "1399.05000000", "last_trade": "1402.49000000", "rolling_24_hour_volume": "3.97310000", "status": "ACTIVE"}, "ETHAUD": {"pair": "ETHAUD", "timestamp": 1662394005461, "bid": "1900.00000000", "ask": "2998.11000000", "last_trade": "2998.11000000", "rolling_24_hour_volume": "0.00490000", "status": "ACTIVE"}, "ETHIDR": {"pair": "ETHIDR", "timestamp": 1662394005461, "bid": "23798000.00000000", "ask": "23799000.00000000", "last_trade": "23700000.00000000", "rolling_24_hour_volume": "1.99910000", "status": "ACTIVE"}, "ETHMYR": {"pair": "ETHMYR", "timestamp": 1662394005461, "bid": "7196.00000000", "ask": "7198.00000000", "last_trade": "7198.00000000", "rolling_24_hour_volume": "425.99760000", "status": "ACTIVE"}, "ETHNGN": {"pair": "ETHNGN", "timestamp": 1662394005461, "bid": "1110492.00000000", "ask": "1124890.00000000", "last_trade": "1110384.00000000", "rolling_24_hour_volume": "11.60993200", "status": "ACTIVE"}, "ETHZAR": {"pair": "ETHZAR", "timestamp": 1662394005461, "bid": "27926.00000000", "ask": "27937.00000000", "last_trade": "27935.00000000", "rolling_24_hour_volume": "548.65694800", "status": "ACTIVE"}, "XBTUSDC": {"pair": "XBTUSDC", "timestamp": 1662394005461, "bid": "19899.33000000", "ask": "19927.70000000", "last_trade": "19899.33000000", "rolling_24_hour_volume": "3.70160000", "status": "ACTIVE"}, "XBTEUR": {"pair": "XBTEUR", "timestamp": 1662394005461, "bid": "19876.30000000", "ask": "20049.92000000", "last_trade": "20035.23000000", "rolling_24_hour_volume": "1.44330000", "status": "ACTIVE"}, "XBTGBP": {"pair": "XBTGBP", "timestamp": 1662394005461, "bid": "17025.00000000", "ask": "17295.00000000", "last_trade": "17243.02000000", "rolling_24_hour_volume": "0.56340000", "status": "ACTIVE"}, "XBTAUD": {"pair": "XBTAUD", "timestamp": 1662394005461, "bid": "29228.75000000", "ask": "29298.96000000", "last_trade": "29237.98000000", "rolling_24_hour_volume": "1.71900000", "status": "ACTIVE"}, "XBTIDR": {"pair": "XBTIDR", "timestamp": 1662394005461, "bid": "296597000.00000000", "ask": "296598000.00000000", "last_trade": "296597000.00000000", "rolling_24_hour_volume": "0.89388100", "status": "ACTIVE"}, "XBTMYR": {"pair": "XBTMYR", "timestamp": 1662394005461, "bid": "89392.00000000", "ask": "89455.00000000", "last_trade": "89332.00000000", "rolling_24_hour_volume": "33.06784000", "status": "ACTIVE"}, "XBTNGN": {"pair": "XBTNGN", "timestamp": 1662394005461, "bid": "13900001.00000000", "ask": "13925009.00000000", "last_trade": "13900001.00000000", "rolling_24_hour_volume": "30.16924300", "status": "ACTIVE"}, "XBTUGX": {"pair": "XBTUGX", "timestamp": 1662394005461, "bid": "74515000.00000000", "ask": "74523000.00000000", "last_trade": "74486000.00000000", "rolling_24_hour_volume": "0.14917500", "status": "ACTIVE"}, "XBTZAR": {"pair": "XBTZAR", "timestamp": 1662394005461, "bid": "345858.00000000", "ask": "346179.00000000", "last_trade": "346205.00000000", "rolling_24_hour_volume": "169.45131600", "status": "ACTIVE"}}, "currencies": ["USDC", "NGN", "ZAR", "BCH", "XBT", "MYR", "LTC", "UNI", "LIN", "KMYR", "XRP", "ETH", "EUR", "GBP", "AUD", "IDR", "UGX"]}
    #print("Currency trade pairs from Luno API:")
    #print(pair_data)
    return pair_data

#calculates the possible trade routes from the cycle basis
def get_routes():
    #get the basis cycles with testing for the types we expect
    basis = get_basis_cycles()
    
    #store the routes in a forward direction
    route_data_forward=[]
    #loop over the cycles to make sure each one starts with XBT
    for cycle in basis:
        start_index=0
        if "XBT" not in cycle:
            print("Error XBT not in cycle", cycle)
            exit(1)
            
        while cycle[start_index]!="XBT":
            start_index+=1
            if start_index==3:
                start_index=0
        loop1=[]
        for x in range(3):
            loop1.append(cycle[start_index])
            start_index+=1
            if start_index==3:
                start_index=0
        route_data_forward.append(loop1)
    
    
    #add routes in reverse
    #example: XBT->ETH->ZAR (forward)
    #XBT->ZAR->ETH (reverse)

    route_data_reverse=[]
    for cycle in route_data_forward:
        new_cycle=[]
        new_cycle.append(cycle[0])
        new_cycle.append(cycle[2])
        new_cycle.append(cycle[1])
        route_data_reverse.append(new_cycle)
    
    
    #combine the two lists
    all_routes=route_data_forward+route_data_reverse


    #return the routes
    return all_routes

#returns all the trade routes
def get_trade_routes():
    #examples of trade route data
    #route_data_forward = [['XBT', 'MYR', 'BCH'], ['XBT', 'MYR', 'LTC'], ['XBT', 'MYR', 'XRP'], ['XBT', 'MYR', 'ETH'], ['XBT', 'USDC', 'ZAR'], ['XBT', 'LTC', 'ZAR'], ['XBT', 'XRP', 'ZAR'], ['XBT', 'ETH', 'ZAR'], ['XBT', 'USDC', 'NGN'], ['XBT', 'LTC', 'NGN'], ['XBT', 'XRP', 'NGN'], ['XBT', 'ETH', 'NGN'], ['XBT', 'ETH', 'IDR'], ['XBT', 'ETH', 'AUD'], ['XBT', 'ETH', 'GBP'], ['XBT', 'ETH', 'EUR'], ['XBT', 'ETH', 'USDC']]
    #route_data_reverse = [['XBT', 'BCH', 'MYR'], ['XBT', 'LTC', 'MYR'], ['XBT', 'XRP', 'MYR'], ['XBT', 'ETH', 'MYR'], ['XBT', 'ZAR', 'USDC'], ['XBT', 'ZAR', 'LTC'], ['XBT', 'ZAR', 'XRP'], ['XBT', 'ZAR', 'ETH'], ['XBT', 'NGN', 'USDC'], ['XBT', 'NGN', 'LTC'], ['XBT', 'NGN', 'XRP'], ['XBT', 'NGN', 'ETH'], ['XBT', 'IDR', 'ETH'], ['XBT', 'AUD', 'ETH'], ['XBT', 'GBP', 'ETH'], ['XBT', 'EUR', 'ETH'], ['XBT', 'USDC', 'ETH']]
    all_routes=get_routes()
    
    return all_routes


#get_trade_routes()