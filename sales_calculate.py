def sales_calculate(size_wt, trend_wt, sales_data, test_vector):
    row_count=len(sales_data.axes[0])
    column_count=len(sales_data.axes[1])
    if ( column_count- len(test_vector.axes[1])==3):
        print("continue")
    else:
        print("error")
    #SSE
    sales_data["SSE"]=np.sum( np.power(sales_data.iloc[:, 3:] - my_list,2), axis=1)
    # Correlation
    sales_data["Correlation"]=''
    for i in range(0,row_count):
        sales_data_list=sales_data.iloc[i,3:17].tolist()
        test_vector_list=my_list_series.tolist()
        corr= pd.Series(sales_data_list).corr(pd.Series(test_vector_list))
        sales_data.iloc[i,18]=corr
    # Ranking 
    sales_data['SSE.rank'] = sales_data['SSE'].rank(method='first', na_option='keep')
    sales_data['Correlation.rank'] = sales_data['Correlation'].rank(method='first', na_option='keep')
    sales_data['final_rank'] =(sales_data['SSE.rank'] *size_wt)+(sales_data['Correlation.rank'] *trend_wt)
    return sales_data
