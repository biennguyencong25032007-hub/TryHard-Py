import json

class CanBo:
    def __init__(self, ho_ten, tuoi, gioi_tinh, dia_chi):
        self.ho_ten    = ho_ten
        self.tuoi      = tuoi
        self.gioi_tinh = gioi_tinh
        self.dia_chi   = dia_chi

    def to_dict(self):
        return {
            "ho_ten":    self.ho_ten,
            "tuoi":      self.tuoi,
            "gioi_tinh": self.gioi_tinh,
            "dia_chi":   self.dia_chi,
            "loai":      self.__class__.__name__,
        }

    def __repr__(self):
        return f"CanBo({self.ho_ten}, {self.tuoi}, {self.gioi_tinh}, {self.dia_chi})"

    @classmethod
    def from_dict(cls, d):
        return cls(d["ho_ten"], d["tuoi"], d["gioi_tinh"], d["dia_chi"])


class CongNhan(CanBo):
    def __init__(self, ho_ten, tuoi, gioi_tinh, dia_chi, bac_tho):
        super().__init__(ho_ten, tuoi, gioi_tinh, dia_chi)
        self.bac_tho = bac_tho

    def to_dict(self):
        d = super().to_dict()
        d["bac_tho"] = self.bac_tho
        return d

    def __repr__(self):
        return f"CongNhan({self.ho_ten}, {self.tuoi}, {self.gioi_tinh}, {self.dia_chi}, bac_tho={self.bac_tho})"

    @classmethod
    def from_dict(cls, d):
        return cls(d["ho_ten"], d["tuoi"], d["gioi_tinh"], d["dia_chi"], d["bac_tho"])


LOAI_MAP = {
    "CanBo": CanBo,
    "CongNhan": CongNhan,
}

# === LƯU ===
danh_sach = [
    CanBo("Nguyễn An", 30, "Nam", "Hà Nội"),
    CongNhan("Trần Bình", 25, "Nam", "TP.HCM", 5),
]

data = [cb.to_dict() for cb in danh_sach]

with open("canbo.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# === TẢI ===
with open("canbo.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

# Khôi phục đúng loại theo "loai"
ds_loaded = [LOAI_MAP[d["loai"]].from_dict(d) for d in raw]

for cb in ds_loaded:
    print(cb)
    