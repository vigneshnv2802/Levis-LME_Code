import pandas as pd
import numpy as np

def sales_calculate(size_wt, trend_wt, sales_data, test_vector):

  # Convert the DataFrame to a list
  my_list = test_vector.values.tolist()[0]
  my_list_series=pd.Series(my_list) 

  column_count=len(sales_data.axes[1])

  # checking dimensions of both dataframe 
  if (column_count- len(test_vector.axes[1])== 1):
      print("continue")
  else:
      print("error")

  sales_data["SSE"]=np.sum( np.power(sales_data.iloc[:, 1:] - my_list,2), axis=1)

  # Correlation
  sales_data["Correlation"]=''
  for i in range(0,row_count):
      sales_data_list = sales_data.iloc[i,1:column_count].tolist()
      test_vector = my_list_series.tolist()
      corr = pd.Series(sales_data_list).corr(pd.Series(test_vector))
      sales_data.iloc[i, column_count+1] = corr


  # Ranking 
  sales_data['SSE.rank'] = sales_data['SSE'].rank(method='first', na_option='keep')
  sales_data['Correlation.rank'] = sales_data['Correlation'].rank(method='first', na_option='keep')
  sales_data['final_rank'] =(sales_data['SSE.rank'] *size_wt)+(sales_data['Correlation.rank'] *trend_wt)

  return sales_data


# sales_data = pd.read_excel("unit_sales_file.xlsx")
# test_vector = pd.read_excel('test_vector_file.xlsx',header = None)
# size_wt=0.25
# trend_wt=0.35

# print(sales_calculate(size_wt, trend_wt, sales_data, test_vector))
