import tkinter as tk


class UIComponents:

    @staticmethod
    def create_display(
            parent,
            textvariable,
            font_family="Arial",
            font_size=30,
            bg="white",
            fg="black",
            border_color="#d0d0d0",
            font_weight="bold"
    ):

        display = tk.Label(
            parent,
            textvariable=textvariable,
            font=(font_family, font_size, font_weight),
            bg=bg,
            fg=fg,
            anchor="e",
            relief="ridge",
            bd=5,
            highlightthickness=1,
            highlightbackground=border_color,
            highlightcolor=border_color,
            height=2
        )

        return display

    @staticmethod
    def create_popup(
            title,
            geometry="300x200",
            parent=None
    ):

        popup = tk.Toplevel(parent) if parent is not None else tk.Toplevel()

        popup.title(title)
        popup.geometry(geometry)
        popup.resizable(False, False)

        return popup

    @staticmethod
    def create_section_frame(
            parent,
            bg="#f5f5f5"
    ):

        frame = tk.Frame(
            parent,
            bg=bg
        )

        return frame
