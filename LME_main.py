import pandas as pd
import numpy as np
from datetime import datetime

def LME_exec(door_attributes, demographics, test_door, sales_data, control_exclusions, from_date, to_date,
             unit_trend_w, unit_size_w, value_trend_w, value_size_w, demo_w, demo_wt_df, func_no):

  from_date = int(from_date)
  to_date = int(to_date)


  door_attributes_mask = door_attributes['Number'].isin(control_exclusions['Door ID'])
  door_attributes_df = door_attributes[~door_attributes_mask].reset_index(drop = True)

  if not demographics.empty:
    door_attributes_mask = door_attributes_df['Number'].isin(demographics['Name'])
    door_attributes_df = door_attributes_df[door_attributes_mask].reset_index(drop = True)
  door_attributes_df = door_attributes_df.rename(columns = {'Number':'Door.ID'})

  test_door_mask = test_door['Door ID'].isin(control_exclusions['Door ID'])
  test_door_df = test_door[~test_door_mask]
  test_door_mask = test_door['Door ID'].isin(door_attributes_df['Door.ID'])
  test_door_df = test_door[test_door_mask]
  test_door_df = test_door_df.sort_values(by='Door ID', ascending=True).reset_index(drop = True)
  test_door_df = test_door_df.rename(columns = {'Door ID':'Door.ID'})

  demo_attributes_mask = demographics['Name'].isin(control_exclusions['Door ID'])
  demographics_df = demographics[~demo_attributes_mask].reset_index(drop = True)
  demographics_df = demographics_df.rename(columns = {'Name':'Door.ID'})
  demographics_df = demographics_df.drop(['City','State','Trade Area Size'],axis = 1)

  all_selected_ids_df = pd.DataFrame()
  all_selected_ids_df['Sell Thru Location Id'] = door_attributes_df['Door.ID']

  sales_data_df = sales_data[['Sell Thru Location Id','Reporting Period Fiscal Year/Week','Sales Units','Sales Dollars']]

  sales_data_df_copy = sales_data_df.copy()

  sales_data_df_copy['Sales Units'] = sales_data_df_copy['Sales Units'].replace('#EMPTY', 0)
  sales_data_df_copy['Sales Units'] = pd.to_numeric(sales_data_df_copy['Sales Units'])
  sales_data_df_copy['Sales Dollars'] = sales_data_df_copy['Sales Dollars'].replace('#EMPTY', 0)
  sales_data_df_copy['Sales Dollars'] = pd.to_numeric(sales_data_df_copy['Sales Dollars'])

  merged_df = pd.merge(all_selected_ids_df, sales_data_df_copy, on='Sell Thru Location Id')

  unit_sale_df = merged_df.pivot_table(values='Sales Units', index='Sell Thru Location Id', columns='Reporting Period Fiscal Year/Week', aggfunc='sum')
  unit_sale_df = unit_sale_df.reset_index()

  value_sale_df = merged_df.pivot_table(values='Sales Dollars', index='Sell Thru Location Id', columns='Reporting Period Fiscal Year/Week', aggfunc='sum')
  value_sale_df = value_sale_df.reset_index()

  from_date_loc = unit_sale_df.columns.get_loc(from_date)
  to_date_loc = unit_sale_df.columns.get_loc(to_date)

  unit_sale_df =  unit_sale_df.iloc[:, [0] + list(range(from_date_loc, to_date_loc+1))]
  unit_sale_df.columns.name = None
  unit_sale_df = unit_sale_df.rename(columns={'Sell Thru Location Id':'Door.ID'})


  value_sale_df =  value_sale_df.iloc[:, [0] + list(range(from_date_loc, to_date_loc+1))]
  value_sale_df.columns.name = None
  value_sale_df = value_sale_df.rename(columns={'Sell Thru Location Id':'Door.ID'})

  if func_no == 1:
      res = synthetic(test_door_df, unit_sale_df, value_sale_df, demographics_df, demo_wt_df, unit_trend_w, unit_size_w, value_trend_w, value_size_w, demo_w)
  elif func_no == 2:
      res = sequential(test_door_df, unit_sale_df, value_sale_df, demographics_df, demo_wt_df, unit_trend_w, unit_size_w, value_trend_w, value_size_w, demo_w)
  
  res = res[['Door.ID','final.rank']]

  res = res.sort_values(by=['final.rank'], ascending=True)
  res['door.type'] = 'Control Door'

  res_df = pd.merge(res,door_attributes_df[['Door.ID','Address','City','State','Zip','Country']], how = 'left', on = 'Door.ID')
  res_df = res_df.rename(columns = {'final.rank':'Scores'})

  test_door_df_copy = test_door_df.copy()
  test_door_df_copy['Scores'] = 0
  test_door_df_copy['door.type'] = 'Test Door'

  tdf = pd.merge(test_door_df_copy,door_attributes_df[['Door.ID','Address','City','State','Zip','Country']], how = 'left', on = 'Door.ID')

  final_result = pd.concat([tdf,res_df],axis = 0)  
  
  no_of_rows = len(test_door_df)*2

  return final_result.head(no_of_rows)

door_attributes = pd.DataFrame(pd.read_excel("original files/door_attributes.xlsx", sheet_name = "Sheet1"))
demographics = pd.DataFrame(pd.read_excel("original files/demo ori.xlsx", sheet_name = "Sheet1"))
test_door = pd.DataFrame(pd.read_excel("original files/test door-noCountry.xlsx", sheet_name = "Sheet1"))

# converting the sales_data csv file to a pickle file for faster reading
sales_data = pd.read_csv("original files/sales_data.csv")
sales_data.to_pickle("original files/sales_data.pkl")
sales_data = pd.read_pickle("original files/sales_data.pkl")

control_exclusions = pd.DataFrame(pd.read_excel("original files/control exclusion-noCountry.xlsx", sheet_name = "Sheet1"))

from_date = '201547'
to_date = '201551'

unit_trend_w = 0.05
unit_size_w = 0.25
value_trend_w = 0.15
value_size_w = 0.35
demo_w = 0.20


demo_wt_df = pd.DataFrame(np.zeros((1, 43)))
demo_wt_df.columns = ['Total Population','Pop Total 15+','Pop Male 15+','Pop Female 15+','Total Households','Avg Family HH Size','Pop Density','Med Age Total','Med Age Male','Med Age Female','Med Age Caucasian','Med Age Caucasian M','Med Age Caucasian F','Med Age Hispanic','Med Age Hispanic M','Med Age Hispanic F','Med Age African-Am','Med Age African-Am M','Med Age African-Am F','Med Age Asian-Am','Med Age Asian-Am M','Med Age Asian-Am F','Pct Married','Pct Caucasian','Pct Hispanic','Pct African-American','Pct Asian-American','Med HH Income Total','Med HH Income Hispanic','Per Capita Income','Pct College or Higher Total','Pct College or Higher Male','Pct College or Higher Female','Pct College or Higher Hispanic','Pct White Collar','Pct Blue Collar','Pct Service & Farm','Pct Total in College','Pct Male in College','Pct Female in College','Avg Commute Time','Avg Length of Residence','Housing Occupancy Pct']

demo_wt_df['Total Population'] = 0.1
demo_wt_df['Pop Total 15+'] = 0.7
demo_wt_df['Pop Male 15+'] = 0.2


func_no = int(input("Enter 1 for synthetic or 2 for sequential: "))


res = LME_exec(door_attributes, demographics, test_door, sales_data, control_exclusions, from_date, to_date,
             unit_trend_w, unit_size_w, value_trend_w, value_size_w, demo_w, demo_wt_df, func_no)

now = datetime.now()

# create a formatted string with date and time
dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")

# save the dataframe to an excel file with the current date and time in the file name
file_name = f"LME_output_{dt_string}.xlsx"
res.to_excel(file_name, index=False)

print("File Saved Successfully!")



