import pandas as pd

f1 = input("第一个标注者的文件路径:")
f2 = input("第二个标注者的文件路径:")

file1 = f1
file2 = f2

def remove_spaces(cell):
    if isinstance(cell, str):
        return cell.replace(" ", "")
    return cell

df1 = pd.read_excel(file1,na_values=' ').applymap(remove_spaces)
df2 = pd.read_excel(file2,na_values=' ').applymap(remove_spaces)

# Combine the rows from the two DataFrames
combined_rows = list(zip(df1.values, df2.values))

# Create a new DataFrame with the desired row arrangement and add check and final rows
merged_data = []
for pair in combined_rows:
    row_sy, row_yl = pair
    merged_data.append(row_sy)
    merged_data.append(row_yl)
    check_row = [3 if (val_sy == val_yl or pd.isna(val_sy) and pd.isna(val_yl)) else 2 if (pd.notna(val_sy) and pd.notna(val_yl)) else 1 for val_sy, val_yl in zip(row_sy, row_yl)]
    check_row[0] = "check"
    merged_data.append(check_row)
    final_row = [val_sy if check == 3 else None for check, val_sy in zip(check_row, row_sy)]
    final_row[0] = "final"
    merged_data.append(final_row)

# Create the merged DataFrame with proper column names
columns = df1.columns
merged_df = pd.DataFrame(merged_data, columns=columns)

output = input("最终输出的文件路径:")
# Output the merged DataFrame to a new Excel file without index
merged_df.to_excel(output, index=False)
print("输出成功！")
