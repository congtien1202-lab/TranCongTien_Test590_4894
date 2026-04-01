import tkinter as tk
from tkinter import messagebox

def encrypt_rail_fence(text, key):
    rail = [['\n' for i in range(len(text))]
                  for j in range(key)]
    dir_down = False
    row, col = 0, 0
    
    for i in range(len(text)):
        if (row == 0) or (row == key - 1):
            dir_down = not dir_down
        rail[row][col] = text[i]
        col += 1
        if dir_down:
            row += 1
        else:
            row -= 1
            
    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return "".join(result)

def decrypt_rail_fence(cipher, key):
    rail = [['\n' for i in range(len(cipher))]
                  for j in range(key)]
    dir_down = None
    row, col = 0, 0
    
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        rail[row][col] = '*'
        col += 1
        if dir_down:
            row += 1
        else:
            row -= 1
            
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if ((rail[i][j] == '*') and
               (index < len(cipher))):
                rail[i][j] = cipher[index]
                index += 1
                
    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        if (rail[row][col] != '\n'):
            result.append(rail[row][col])
            col += 1
        if dir_down:
            row += 1
        else:
            row -= 1
    return "".join(result)

# --- Giao diện UI ---
def handle_encrypt():
    text = entry_input.get()
    try:
        key = int(entry_key.get())
        if key < 2: raise ValueError
        result = encrypt_rail_fence(text, key)
        entry_output.delete(0, tk.END)
        entry_output.insert(0, result)
    except ValueError:
        messagebox.showerror("Lỗi", "Key phải là số nguyên lớn hơn 1")

def handle_decrypt():
    cipher = entry_input.get()
    try:
        key = int(entry_key.get())
        if key < 2: raise ValueError
        result = decrypt_rail_fence(cipher, key)
        entry_output.delete(0, tk.END)
        entry_output.insert(0, result)
    except ValueError:
        messagebox.showerror("Lỗi", "Key phải là số nguyên lớn hơn 1")

# Khởi tạo cửa sổ
root = tk.Tk()
root.title("Rail Fence Cipher - Lab UI")
root.geometry("400x350")

tk.Label(root, text="RAIL FENCE CIPHER", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Nhập văn bản:").pack()
entry_input = tk.Entry(root, width=40)
entry_input.pack(pady=5)

tk.Label(root, text="Nhập Key (số hàng):").pack()
entry_key = tk.Entry(root, width=10)
entry_key.pack(pady=5)

frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

btn_encrypt = tk.Button(frame_btn, text="Mã hóa", command=handle_encrypt, bg="lightblue")
btn_encrypt.pack(side=tk.LEFT, padx=10)

btn_decrypt = tk.Button(frame_btn, text="Giải mã", command=handle_decrypt, bg="lightgreen")
btn_decrypt.pack(side=tk.LEFT, padx=10)

tk.Label(root, text="Kết quả:").pack()
entry_output = tk.Entry(root, width=40, fg="blue")
entry_output.pack(pady=5)

root.mainloop()