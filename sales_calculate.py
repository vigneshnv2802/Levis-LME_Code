def sales_calculate(size_wt, trend_wt, sales_data, test_vector):

  # Convert the list to series
  my_list_series=pd.Series(test_vector) 

  sales_data_copy = sales_data.copy()

  row_count=len(sales_data_copy.axes[0])

  column_count=len(sales_data_copy.axes[1])

  # checking dimensions of both dataframe 
  if (column_count- len(test_vector)== 1):
      print("continue")
  else:
      print("error")

  sales_data_copy["SSE"]=np.sum( np.power(sales_data_copy.iloc[:, 1:] - test_vector,2), axis=1)

  # Correlation
  sales_data_copy["Correlation"]=''
  for i in range(0,row_count):
      sales_data_list = sales_data_copy.iloc[i,1:column_count].tolist()
      test_vector = my_list_series.tolist()
      corr = pd.Series(sales_data_list).corr(pd.Series(test_vector))
      sales_data_copy.iloc[i, column_count+1] = -corr


  # Ranking 
  sales_data_copy['SSE.rank'] = sales_data_copy['SSE'].rank(method='first')
  sales_data_copy['Correlation.rank'] = sales_data_copy['Correlation'].rank(method='first')
  sales_data_copy['final_rank'] =(sales_data_copy['SSE.rank'] *size_wt)+(sales_data_copy['Correlation.rank'] *trend_wt)

  return sales_data_copy

# sales_data = pd.read_excel("unit_sales_file.xlsx")
# print(sales_data)
# test_vector = [1030, 842, 913, 925, 972]
# print(test_vector)
# trend_wt = 0.05
# size_wt = 0.25
# # test_vector = pd.DataFrame(test_v, columns = None)

# print(sales_calculate(size_wt, trend_wt, sales_data, test_vector))
