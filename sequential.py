def sequential(test_door, unit_sale, value_sale, demographics, demo_wt, unit_trend_w, unit_size_w, value_trend_w, value_size_w, demo_w):
  test_unit_file = test_door.merge(unit_sale, how = 'left', on = 'Door.ID')

  test_value_file = test_door.merge(value_sale, how = 'left', on = 'Door.ID')

  test_demo_file = test_door.merge(demographics, how = 'left', on = 'Door.ID')  

  unit_sale_join = pd.merge(unit_sale, test_door,  how="outer", on="Door.ID" , indicator = True)
  control_unit_file = unit_sale_join[~(unit_sale_join._merge == 'both')].drop('_merge', axis = 1).reset_index(drop = True)

  value_sale_join = pd.merge(value_sale, test_door, on = "Door.ID", how = "outer", indicator = True)
  control_value_file = value_sale_join[~(value_sale_join._merge == 'both')].drop('_merge', axis = 1).reset_index(drop = True)

  demo_join = pd.merge(demographics, test_door, on = "Door.ID", how = "outer", indicator = True)
  control_demo_file = demo_join[~(demo_join._merge == 'both')].drop('_merge', axis = 1).reset_index(drop = True)

  seq_score_df = pd.DataFrame(control_unit_file['Door.ID'])
  
  score = pd.DataFrame(control_unit_file['Door.ID'])

  for i in range(len(test_door)):
    # preserving the score dataframe to its original state after each iteration
    score_temp = score.copy()

    # calculating the unit sale rank
    selected_door_unit = test_unit_file.values.tolist()[i][1:] 
    unit_sale_rank = sales_calculate(unit_size_w, unit_trend_w, control_unit_file, selected_door_unit)
    score_temp['unit sale rank'] = unit_sale_rank['final_rank']

    # calculating the value sale rank
    selected_door_value = test_value_file.values.tolist()[i][1:] 
    value_sale_rank = sales_calculate(value_size_w, value_trend_w, control_value_file, selected_door_value)
    score_temp['value sale rank'] = value_sale_rank['final_rank']

    # calculating the demographics rank
    if not demographics.empty:
      selected_door_demo = pd.DataFrame(test_demo_file.loc[i, :])
      selected_door_demo = selected_door_demo.T
      demographics_rank = demographics_cal(control_demo_file, selected_door_demo, demo_wt)
      score_temp['demo rank'] = demographics_rank['Final.rank']
      score_temp['demo rank'] = score_temp['demo rank'] * demo_w
      col_name = 'testdoor' + "-" + str(test_unit_file['Door.ID'][i])

    seq_score_df[col_name] = score_temp.iloc[:,1:].sum(axis = 1)
    
  seq_score_df['final.rank'] = seq_score_df.iloc[:,1:].sum(axis = 1)
    
  return seq_score_df
