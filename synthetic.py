def synthetic(test_door,
unit_sale,
value_sale,
demographics,
demo_weights,
unit_trend_w = 0.05,
unit_sse_w = 0.25,
value_trend_w = 0.15,
value_sse_w = 0.35,
demo_w = 0.2):
    # demographics
    if not demographics.empty:
     test_demo=pd.merge(test_door, demographics.loc[:,:], how='inner', on = "Door.ID")
    test_mean = pd.DataFrame(test_demo[test_demo.select_dtypes(include=np.number).columns].mean(axis=0),columns=['mean']).transpose()
    demo_matrix= demographics_cal(demographics,test_mean,demo_weights)
    # Units 
    test_unit_sales=pd.merge(test_door, unit_sale.loc[:,:], how='inner', on = "Door.ID")
    unit_sales_mean = pd.DataFrame(test_unit_sales[test_unit_sales.select_dtypes(include=np.number).columns].mean(axis=0),columns=['mean']).transpose()
#     unit_sale = unit_sale.drop('Country', axis=1)
    unit_sales_mean=unit_sales_mean.drop('Door.ID', axis=1)
    unit_sales_mean_list=unit_sales_mean.values.tolist()[0]
    unit_sales_value = sales_calculate(unit_sse_w, unit_trend_w, unit_sale, unit_sales_mean_list)
    
    # Values
    test_value_sales=pd.merge(test_door, value_sale.loc[:,:], how='inner', on = "Door.ID")
    value_sales_mean = pd.DataFrame(test_value_sales[test_value_sales.select_dtypes(include=np.number).columns].mean(axis=0),columns=['mean']).transpose()
#     value_sale = value_sale.drop('Country', axis=1)
    value_sales_mean=value_sales_mean.drop('Door.ID', axis=1)
    value_sales_mean_list=value_sales_mean.values.tolist()[0]
    value_sales_value = sales_calculate(value_sse_w, value_trend_w, value_sale, value_sales_mean_list)
    
    #Scores
    scores = pd.DataFrame({'Door.ID': unit_sale['Door.ID']})
    if not demographics.empty:
        scores["unit sale rank"] = unit_sales_value["final_rank"]
        scores["value sale rank"] =value_sales_value["final_rank"]
        scores["demographics rank"] = demo_matrix["Final.rank"]*demo_w
        scores["final.rank"] = scores["unit sale rank"] + scores["value sale rank"] + scores["demographics rank"]
    else:
        scores["unit sale rank"] <- unit_sales_value["final_rank"]
        scores["value sale rank"] <- value_sales_value["final_rank"]
        scores["final.rank"] <- scores["unit sale rank"] + scores["value sale rank"] 
        
    return scores
