s = input("Nhập chuỗi: ")
is_palindrome = True

for i in range(len(s)//2):
    if s[i] != s[len(s)-1-i]:
        is_palindrome = False
        break

print("Là chuỗi đối xứng" if is_palindrome else "Không phải")