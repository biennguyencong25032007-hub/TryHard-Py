class SinhVien:
    def __init__(self, ten, mssv, diem_toan, diem_ly, diem_hoa):
        self.ten       = ten
        self.mssv      = mssv
        self.diem_toan = diem_toan
        self.diem_ly   = diem_ly
        self.diem_hoa  = diem_hoa
   
    def tinh_tb(self):
        return (self.diem_toan + self.diem_ly + self.diem_hoa) / 3
    
    def __str__(self):
        return f"{self.mssv} | {self.ten:15s} | TB: {self.tinh_tb():.1f}"
    
class QuanLySV:
    def __init__(self):
        self.ds = []  
    
    def them(self, sv):
        self.ds.append(sv)
        print(f"đã thêm : {sv.ten}")
        
    def hien_thi(self):
        for sv in self.ds:
            print(sv)
        
    def tim_kiem(self, ten):
          return [sv for sv in self.ds
                if ten.lower() in sv.ten.lower()] 
    
    def gioi_nhat(self):
        return max(self.ds, key=lambda sv: sv.tinh_tb())
    
    
ql = QuanLySV()
ql.them(SinhVien("Nguyen Van A", "001", 8, 7, 9))
ql.them(SinhVien("Tran Thi B",  "002", 5, 6, 4))
ql.them(SinhVien("Le Van C",    "003", 9, 9, 10))

print("\n── Danh sách ──")
ql.hien_thi()

print("\n── Tìm 'van' ──")
for sv in ql.tim_kiem("van"):
    print(sv)

print("\n── Giỏi nhất ──")
print(ql.gioi_nhat())