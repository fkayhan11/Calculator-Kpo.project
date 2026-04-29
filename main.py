import tkinter as tk
from view import CalculatorView


def main():
    root = tk.Tk()
    CalculatorView(root)
    root.mainloop()


if __name__ == "__main__":
    main()

    # Lab 3 kapsamında hesap makinesi projesi Factory Method tasarım kalıbı ile geliştirildi.
    # Buton oluşturma işlemleri doğrudan View sınıfından ayrılarak ButtonFactory sınıfına taşındı.
    # Bu sayede arayüz kodu daha sade, düzenli ve genişletilebilir hale getirildi.
    # Yeni buton türleri veya renkleri eklemek gerektiğinde yalnızca ButtonFactory üzerinde değişiklik yapmak yeterlidir.