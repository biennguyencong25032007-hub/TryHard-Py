def sinhvien(ten, mssv, diem_toan, diem_ly, diem_hoa):
    diem_tb = (diem_toan + diem_ly + diem_hoa) / 3
    if diem_tb >= 9:
        xep_loai = "Xuất sắc"
    elif diem_tb >= 8:
        xep_loai = "Giỏi"
    elif diem_tb >= 7:
        xep_loai = "Khá"
    elif diem_tb >= 5:
        xep_loai = "Trung bình"
    else:
        xep_loai = "Yếu"

    return {
        "ten": ten, "mssv": mssv,
        "diem_toan": diem_toan, "diem_ly": diem_ly, "diem_hoa": diem_hoa,
        "diem_tb": round(diem_tb, 2),   # ← làm tròn 2 chữ số
        "xep_loai": xep_loai
    }

# ── Hàm in đẹp ───────────────────────────────
def in_sinh_vien(sv):
    print(f"┌{'─'*30}┐")
    print(f"│ Tên  : {sv['ten']:22s}│")
    print(f"│ MSSV : {sv['mssv']:22s}│")
    print(f"│ Toán : {sv['diem_toan']:<22}│")
    print(f"│ Lý   : {sv['diem_ly']:<22}│")
    print(f"│ Hóa  : {sv['diem_hoa']:<22}│")
    print(f"│ TB   : {sv['diem_tb']:<22}│")
    print(f"│ Loại : {sv['xep_loai']:22s}│")
    print(f"└{'─'*30}┘")

sv = sinhvien("Nguyen Van A", "123456", 8, 7, 9)
in_sinh_vien(sv)