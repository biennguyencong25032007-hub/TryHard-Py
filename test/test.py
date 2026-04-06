san_pham = ["Táo", "Cam", "Chuối", "Nho", "Dưa hấu", "Mít"]

dai_hon_3 = [sp for sp in san_pham if len(sp) > 3]
print(dai_hon_3)

print("dầu tiên: ", san_pham[0])
print("cuối cùng: ", san_pham[-1])

dao_nguoc = san_pham[::-1]
print("danh sách đảo ngược: ", dao_nguoc)