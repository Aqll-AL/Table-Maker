import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape

class TableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Table to PDF")
        self.root.geometry("1000x700")
        self.root.configure(bg="black")
        self.entries = []

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Modern.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10,
            background="#2d89ef",
            foreground="white",
            borderwidth=0
        )
        style.map(
            "Modern.TButton",
            background=[("active", "#1e5fa3")]
        )

        control_frame = tk.Frame(root, bg="black")
        control_frame.pack(pady=20)

        tk.Label(
            control_frame,
            text="Rows:",
            bg="black",
            fg="white",
            font=("Segoe UI", 11)
        ).grid(row=0, column=0, padx=5)
        
        self.rows_entry = tk.Entry(
            control_frame,
            width=6,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.rows_entry.grid(row=0, column=1, padx=5)

        tk.Label(
            control_frame,
            text="Columns:",
            bg="black",
            fg="white",
            font=("Segoe UI", 11)
        ).grid(row=0, column=2, padx=5)

        self.cols_entry = tk.Entry(
            control_frame,
            width=6,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.cols_entry.grid(row=0, column=3, padx=5)

        ttk.Button(
            control_frame,
            text="Create Table",
            style="Modern.TButton",
            command=self.create_table
        ).grid(row=0, column=4, padx=15)

        self.table_frame = tk.Frame(root, bg="black")
        self.table_frame.pack(pady=10)

        ttk.Button(
            root,
            text="Save as PDF",
            style="Modern.TButton",
            command=self.save_pdf
        ).pack(pady=25)

    def create_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.entries.clear()

        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
            return

        for r in range(rows):
            row_entries = []
            for c in range(cols):
                e = tk.Entry(
                    self.table_frame,
                    width=15,
                    bg="#1e1e1e",
                    fg="white",
                    insertbackground="white",
                    relief="ridge"
                )
                e.grid(row=r, column=c, padx=3, pady=3)
                row_entries.append(e)
            self.entries.append(row_entries)

    def save_pdf(self):
        if not self.entries:
            messagebox.showerror("Error", "Create a table first")
            return

        table_data = []
        for row in self.entries:
            table_data.append([cell.get() for cell in row])

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )

        if not file_path:
            return

        pdf = SimpleDocTemplate(
            file_path,
            pagesize=landscape(A4),
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20
        )

        num_cols = len(table_data[0])
        col_widths = [120] * num_cols

        table = Table(table_data, colWidths=col_widths)

        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
        ]))

        pdf.build([table])
        messagebox.showinfo("Success", "PDF saved successfully!")

root = tk.Tk()
app = TableApp(root)
root.mainloop()
