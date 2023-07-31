## 此次数据有HST和WXY两个人的数据
import pandas as pd
import numpy as np
df_hst = pd.read_excel('./Chin_Subj_Coding_HST_20230712.xlsx') # 第一个编码者的文件
df_wxy = pd.read_excel('./Chin_Subj_Coding_WXY_20230712.xlsx') # 第二个编码者的文件

columns = df_hst.columns.tolist()
df_merged = pd.DataFrame()

ce_counter = 1  # CE列计数器

for col in columns:
    if col == 'Coder':
        df_merged['Coder'] = 'HST_WXY' # 两个人名字的合并
    else:
        # 添加 HST 数据集的列
        df_merged[col + '_HST'] = df_hst[col]  
        df_merged[col + '_WXY'] = df_wxy[col]
        # 添加 WXY 数据集的列
        if col in ['Subjects_Group', 'Educational_Attainment_info', 'Ethnicity_info',
                   'Subjects_Area_info', 'Subjects_Recruitment_Area', 'Subjects_Recruitment_Method_info']:
            df_merged['CE' + str(ce_counter)] = ''
            ce_counter += 1
        else:
            df_merged[col + '_WXY'] = df_wxy[col]

df_merged['Coder'] = 'HST_WXY' # 两个人名字的合并
df = df_merged.applymap(lambda x: x.strip() if isinstance(x, str) else x)

columns = ['Subjects_Group', 'Educational_Attainment_info', 'Ethnicity_info',
           'Subjects_Area_info', 'Subjects_Recruitment_Area', 'Subjects_Recruitment_Method_info']
column_dict = {col: 'CE' + str(idx + 1) for idx, col in enumerate(columns)}

for col in column_dict.keys():
    col_hst = col + '_HST' #  填写第一个人的名字
    col_wxy = col + '_WXY' # 填写第二个人的名字
    # df[column_dict[col]] = np.where(col_hst == col_wxy, 1, 3)
    for index, row in df.iterrows():
        col1_value = row[col_hst]
        col2_value = row[col_wxy]
    
        # 将空值填充为特定的值
        col1_value = col1_value if pd.notnull(col1_value) else "__NULL__"
        col2_value = col2_value if pd.notnull(col2_value) else "__NULL__"

        if col1_value == col2_value: # 完全一致是3，不一致是1
            df.at[index, column_dict[col]] = 3
        else:
            df.at[index, column_dict[col]] = 1

df.to_excel('merged_data.xlsx', index=False)


# ce_counter = 1
# # 对比特定列的内容并填写 CE 列
# for col in ['Subjects_Group', 'Educational_Attainment_info', 'Ethnicity_info',
#             'Subjects_Area_info', 'Subjects_Recruitment_Area', 'Subjects_Recruitment_Method_info']:
#     col_hst = col + '_HST' # 需修改名字
#     col_wxy = col + '_WXY' # 需修改名字
#     df_merged['CE' + str(ce_counter)] = (df_merged[col_hst]) == df_merged[col_wxy].apply(lambda x: 1 if x else 3)
#     ce_counter += 1

# df = pd.read_excel('merged_data.xlsx') # 最终输出结果是1和3，还需要人工全部看一遍
# df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
# df.to_excel('merged_data.xlsx', index=False)