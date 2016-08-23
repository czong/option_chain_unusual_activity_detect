#from pandas.io.data import Options
from pandas_datareader.data import Options
import ipdb
import numpy as np
import pandas as pd
from optionchain import OptionChain as option

symbol_list = ['aapl','NTES','BABA','VRX','SBUX']

for symbol in symbol_list:
    oc = Options(symbol,'yahoo')
    ipdb.set_trace()
    data = oc.get_all_data()
    call = pd.DataFrame(oc.calls)
    put = pd.DataFrame(oc.puts)

    # call expect price
    call_strike_price = call.strike.apply(float)
    call_premium_price = call.p.replace('-',np.NaN)
    call_premium_price = call_premium_price.apply(float)
    call_expect_price = call_strike_price+call_premium_price
    call_open_interest = call.oi.apply(float)
    # put expect price 
    put_strike_price = put.strike.apply(float)
    put_premium_price = put.p.replace('-',np.NaN)
    put_premium_price = put_premium_price.apply(float)
    put_expect_price = put_strike_price-put_premium_price
    put_open_interest = put.oi.apply(float)

    option_new_df = pd.DataFrame([call.expiry,call_expect_price,call_open_interest,put_expect_price,put_open_interest]).transpose()
    option_new_df.columns = ['expire_date','call_expect_price','call_open_interest','put_expect_price','put_open_interest']
    ipdb.set_trace()
    for group in option_new_df.groupby('expire_date'):
        expire_date = group[0]
        group_df = group[1]
        option_expect_price = ((group_df.call_expect_price*group_df.call_open_interest).sum()+(group_df.put_expect_price*group_df.put_open_interest).sum())/(group_df.call_open_interest+group_df.put_open_interest).sum()
        print '%s, %s: %.2f'%(symbol,expire_date,option_expect_price)


