import tkinter as tk
from tkinter import ttk, messagebox
from User import User
from Product import Product
from orderitems import OrderItemsManager
from Order import Order
from app import StoreApp

# ایجاد یک نمونه از StoreApp
storeapp = StoreApp()  # این الان داده‌ها را هنگام راه‌اندازی بارگذاری می‌کند

class StoreGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ورود به فروشگاه آنلاین")
        self.root.geometry("600x500")  # اندازه پنجره کمی بزرگتر شد
        self.current_user = None
        self.build_login_ui()

    def build_login_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("400x300")  # تنظیم مجدد اندازه برای صفحه ورود

        tk.Label(self.root, text="نام کاربری:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=2)

        tk.Label(self.root, text="رمز عبور:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=2)

        tk.Button(self.root, text="ورود", command=self.handle_login).pack(pady=10)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = storeapp.login(username, password)

        if user:
            self.current_user = user
            if user.is_admin():
                self.build_admin_ui()
            else:
                self.build_customer_ui()
        else:
            messagebox.showerror("ورود ناموفق", "نام کاربری یا رمز عبور نامعتبر است")

    def build_customer_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("600x500")  # تنظیم اندازه برای نمای مشتری

        tk.Label(self.root, text=f"خوش آمدید، {self.current_user.username}! موجودی شما: {self.current_user.balance} تومان").pack(pady=5)

        # Treeview برای لیست محصولات
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Price", "Stock"), show="headings")
        self.tree.heading("ID", text="شناسه محصول")
        self.tree.heading("Name", text="نام")
        self.tree.heading("Price", text="قیمت")
        self.tree.heading("Stock", text="موجودی")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # پر کردن محصولات
        self.load_products_into_treeview()

        # انتخاب محصول و تعداد
        tk.Label(self.root, text="شناسه محصول برای خرید را وارد کنید:").pack()
        self.product_id_entry = tk.Entry(self.root)
        self.product_id_entry.pack()

        tk.Label(self.root, text="تعداد:").pack()
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.pack()

        tk.Button(self.root, text="ثبت سفارش", command=self.place_order).pack(pady=10)
        tk.Button(self.root, text="خروج", command=self.build_login_ui).pack(pady=5)

    def load_products_into_treeview(self):
        # پاک کردن ورودی‌های موجود
        for item in self.tree.get_children():
            self.tree.delete(item)
        # پر کردن مجدد با داده‌های فعلی
        for product_id, product in storeapp.products.items():
            self.tree.insert("", "end", iid=product.id, values=(product.id, product.name, product.price, product.stock))

    def place_order(self):
        pid = self.product_id_entry.get()

        try:
            qty = int(self.quantity_entry.get())
            if qty <= 0:
                raise ValueError("تعداد باید مثبت باشد.")
        except ValueError as e:
            messagebox.showerror("خطا", f"تعداد نامعتبر: {e}")
            return

        # آماده‌سازی آیتم‌های سبد خرید (فعلاً برای سادگی از یک محصول پشتیبانی می‌کند)
        cart = [{"product_id": pid, "quantity": qty}]

        # فراخوانی متد place_order از StoreApp
        result_message = storeapp.place_order(self.current_user.username, cart)
        messagebox.showinfo("نتیجه سفارش", result_message)

        # به‌روزرسانی رابط کاربری پس از سفارش
        self.product_id_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.current_user = storeapp.users.get(self.current_user.username)  # بارگذاری مجدد کاربر برای دریافت موجودی به‌روز شده
        self.build_customer_ui()  # بازسازی برای نمایش موجودی و موجودی به‌روز شده

    def build_admin_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("600x550")  # تنظیم اندازه برای نمای مدیر

        tk.Label(self.root, text=f"خوش آمدید مدیر، {self.current_user.username}").pack(pady=10)

        # لیست محصولات برای مدیر
        self.admin_tree = ttk.Treeview(self.root, columns=("ID", "Name", "Price", "Stock", "Category"), show="headings")
        self.admin_tree.heading("ID", text="شناسه محصول")
        self.admin_tree.heading("Name", text="نام")
        self.admin_tree.heading("Price", text="قیمت")
        self.admin_tree.heading("Stock", text="موجودی")
        self.admin_tree.heading("Category", text="دسته‌بندی")
        self.admin_tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.load_admin_products_into_treeview()

        # فیلدهای ورودی برای افزودن محصول جدید
        tk.Label(self.root, text="افزودن محصول جدید:").pack(pady=5)

        tk.Label(self.root, text="نام محصول:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        tk.Label(self.root, text="قیمت:").pack()
        self.price_entry = tk.Entry(self.root)
        self.price_entry.pack()

        tk.Label(self.root, text="موجودی:").pack()
        self.stock_entry = tk.Entry(self.root)
        self.stock_entry.pack()

        tk.Label(self.root, text="دسته‌بندی:").pack()
        self.cat_entry = tk.Entry(self.root)
        self.cat_entry.pack()

        tk.Button(self.root, text="افزودن محصول", command=self.add_product).pack(pady=10)
        tk.Button(self.root, text="خروج", command=self.build_login_ui).pack(pady=5)

    def load_admin_products_into_treeview(self):
        # پاک کردن ورودی‌های موجود
        for item in self.admin_tree.get_children():
            self.admin_tree.delete(item)
        # پر کردن مجدد با داده‌های فعلی
        for product_id, product in storeapp.products.items():
            self.admin_tree.insert("", "end", iid=product.id, values=(product.id, product.name, product.price, product.stock, product.category))

    def add_product(self):
        try:
            name = self.name_entry.get()
            price = float(self.price_entry.get())
            stock = int(self.stock_entry.get())
            category = self.cat_entry.get()
        except ValueError:
            messagebox.showerror("خطا", "ورودی نامعتبر")
            return

        # تولید Product ID ساده (در یک سیستم واقعی ممکن است قوی‌تر باشد)
        new_product_id = f"P{len(storeapp.products) + 1}"
        while new_product_id in storeapp.products: # اطمینان از منحصر به فرد بودن
            new_product_id = f"P{len(storeapp.products) + 1}"

        new_product = Product(new_product_id, name, price, stock, category)

        if storeapp.add_product(new_product):
            messagebox.showinfo("موفقیت", f"محصول {name} با موفقیت اضافه شد.")
            self.name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.stock_entry.delete(0, tk.END)
            self.cat_entry.delete(0, tk.END)
            self.load_admin_products_into_treeview() # به‌روزرسانی لیست محصولات مدیر
        else:
            messagebox.showerror("خطا", f"افزودن محصول {name} با مشکل مواجه شد.")

# اجرای برنامه
if __name__ == "__main__":
    root = tk.Tk()
    app = StoreGUI(root)
    root.mainloop()