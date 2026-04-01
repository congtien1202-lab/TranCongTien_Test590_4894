import tkinter as tk
from tkinter import messagebox
import random

# --- Thuật toán RSA cơ bản ---
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    d = 0
    x1, x2 = 0, 1
    y1, y2 = 1, 0
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2 - temp1 * x1
        y = y2 - temp1 * y1
        
        x2, x1 = x1, x
        y2, y1 = y1, y
    
    if temp_phi == 1:
        return y2 % phi

def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))

# --- Xử lý Giao diện ---
def handle_generate_keys():
    try:
        p = int(entry_p.get())
        q = int(entry_q.get())
        if not (is_prime(p) and is_prime(q)):
            messagebox.showerror("Lỗi", "P và Q phải là số nguyên tố!")
            return
        
        global public_key, private_key
        public_key, private_key = generate_keypair(p, q)
        
        lbl_pub.config(text=f"Public Key (e, n): {public_key}")
        lbl_priv.config(text=f"Private Key (d, n): {private_key}")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ cho P và Q")

def handle_encrypt():
    try:
        msg = entry_msg.get()
        e, n = public_key
        cipher = [pow(ord(char), e, n) for char in msg]
        entry_result.delete(0, tk.END)
        entry_result.insert(0, ",".join(map(str, cipher)))
    except NameError:
        messagebox.showerror("Lỗi", "Hãy tạo Key trước!")

def handle_decrypt():
    try:
        cipher_str = entry_msg.get()
        d, n = private_key
        cipher = [int(x) for x in cipher_str.split(",")]
        plain = [chr(pow(char, d, n)) for char in cipher]
        entry_result.delete(0, tk.END)
        entry_result.insert(0, "".join(plain))
    except Exception as e:
        messagebox.showerror("Lỗi", "Dữ liệu giải mã không hợp lệ hoặc thiếu Key!")

# --- Khởi tạo UI ---
root = tk.Tk()
root.title("RSA Cipher UI")
root.geometry("500x550")

tk.Label(root, text="THUẬT TOÁN RSA", font=("Arial", 16, "bold")).pack(pady=10)

# Phần nhập P, Q
frame_pq = tk.Frame(root)
frame_pq.pack()
tk.Label(frame_pq, text="Số nguyên tố P:").grid(row=0, column=0)
entry_p = tk.Entry(frame_pq, width=10); entry_p.grid(row=0, column=1, padx=5)
tk.Label(frame_pq, text="Số nguyên tố Q:").grid(row=1, column=0)
entry_q = tk.Entry(frame_pq, width=10); entry_q.grid(row=1, column=1, padx=5)

tk.Button(root, text="Tạo Cặp Key", command=handle_generate_keys, bg="yellow").pack(pady=10)

lbl_pub = tk.Label(root, text="Public Key: (Chưa có)", fg="green")
lbl_pub.pack()
lbl_priv = tk.Label(root, text="Private Key: (Chưa có)", fg="red")
lbl_priv.pack()

# Phần nhập thông điệp
tk.Label(root, text="\nNhập thông điệp (hoặc dãy số mã hóa):").pack()
entry_msg = tk.Entry(root, width=50)
entry_msg.pack(pady=5)

frame_action = tk.Frame(root)
frame_action.pack(pady=10)
tk.Button(frame_action, text="Mã hóa (Dùng Pub)", command=handle_encrypt, bg="lightblue").pack(side=tk.LEFT, padx=10)
tk.Button(frame_action, text="Giải mã (Dùng Priv)", command=handle_decrypt, bg="lightpink").pack(side=tk.LEFT, padx=10)

tk.Label(root, text="Kết quả:").pack()
entry_result = tk.Entry(root, width=50, font=("Arial", 10, "bold"))
entry_result.pack(pady=10)

root.mainloop()