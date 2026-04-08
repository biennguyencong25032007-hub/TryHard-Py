import pandas as pd
import numpy as np
import io

data = """ten,mon,diem,hoc_ky
An,Toan,8.5,1
An,Van,7.0,1
An,Anh,9.0,1
Binh,Toan,6.0,1
Binh,Van,8.0,1
Binh,Anh,7.5,1
Chi,Toan,9.5,1
Chi,Van,8.5,1
Chi,Anh,8.0,1"""

df = pd.read_csv(io.StringIO(data))

# 1. Điểm trung bình mỗi học sinh
dtb = df.groupby('ten')['diem'].mean().round(2)
print(dtb)
# 2. Học sinh điểm cao nhất
print("Cao nhất:", dtb.idxmax(), "-", dtb.max())

# 3. Điểm trung bình từng môn
print(df.groupby('mon')['diem'].mean().round(2))

# 4. Pivot table
bang = pd.pivot_table(
    df, values='diem',
    index='ten', columns='mon',
    aggfunc='mean'
)
print(bang)

# 5. Xếp loại dựa vào điểm trung bình
diem_tb = df.groupby('ten')['diem'].mean()
conditions = [diem_tb >= 8.5, diem_tb >= 7.0]
choices    = ['Gioi', 'Kha']
xep_loai = pd.Series(
    np.select(conditions, choices, default='TB'),
    index=diem_tb.index
)
print(xep_loai)