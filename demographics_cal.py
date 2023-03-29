def demographics_cal(demo_data, selected_door, demo_weightages):
  row_count = demo_data.shape[0]

  selected_door_repeated = pd.concat([selected_door]*row_count, ignore_index=True)

  subtracted_df = pd.concat([demo_data['Door.ID'], abs(selected_door_repeated.iloc[:, 3:] - demo_data.iloc[:, 3:])], axis=1)

  demo_weightages_repeated = pd.concat([demo_weightages]*row_count, ignore_index=True)

  rank_df = pd.concat([subtracted_df['Door.ID'],(subtracted_df.iloc[:, 1:].rank(method='first'))*demo_weightages_repeated.iloc[:,1:]],axis = 1) 

  rank_df['Final.rank'] = rank_df.iloc[:,1:].sum(axis=1)

  return rank_df


# demo_data = pd.DataFrame(pd.read_excel("demo_data.xlsx", sheet_name="Sheet1"))
# selected_door = pd.DataFrame(pd.read_csv("selected_door_DemographicsCalculation.csv"))
# demo_weightages = pd.DataFrame(pd.read_csv("demo_wt_DemoCalculations.csv"))

# result = demographics_cal(demo_data, selected_door, demo_weightages)

# result.to_excel('res.xlsx', index = False)
