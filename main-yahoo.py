#from pandas.io.data import Options
from pandas_datareader.data import Options
import ipdb
import numpy as np
import pandas as pd
from optionchain import OptionChain as option

symbol_list = ['aapl','NTES','BABA','VRX','SBUX']

for symbol in symbol_list:
    oc = Options(symbol,'yahoo')
    temp = []
    for expire_date in  oc.expiry_dates:
        call = oc.get_call_data(expiry = expire_date)
        call.reset_index(['Strike','Expiry','Type','Symbol'],inplace=True)
        call = call.loc[call.IsNonstandard==False,:]
        put = oc.get_put_data(expiry=expire_date)
        put.reset_index(['Strike','Expiry','Type','Symbol'],inplace=True)
        put = put.loc[put.IsNonstandard==False,:]
        

        call_amount = ((call.Strike+call.Last)*call.Open_Int).sum()
        call_expect_price = call_amount/call.Open_Int.sum()
        put_amount = ((put.Strike+put.Last)*put.Open_Int).sum()
        put_expect_price = put_amount/put.Open_Int.sum()

        option_expect_price = (call_amount+put_amount)/(call.Open_Int.sum()+put.Open_Int.sum())
        temp.append([expire_date,call_amount,call_expect_price,put_amount,put_expect_price,option_expect_price])
        #temp.append({'expire_date':expire_date,'call_amount':call_amount,'call_expect_price':call_expect_price,'put_amount':put_amount,'put_expect_price':put_expect_price,'option_expect_price':option_expect_price})

    ipdb.set_trace()
    temp = pd.DataFrame(temp,columns=['expire_date','call_amount','call_expect_price','put_amount','put_expect_price','option_expect_price'])


    # call expect price
    call_premium_price = call.p.replace('-',np.NaN)
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


