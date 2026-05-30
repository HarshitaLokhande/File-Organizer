import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

from organizer import organize_files, undo_organization


class SmartOrganizerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Smart File Organizer")
        self.root.geometry("900x600")
        self.root.configure(bg="#0f172a")  # deep navy background

        self.folder_path = ""

        # ================= HEADER =================
        header = tk.Frame(root, bg="#0f172a")
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="SMART FILE ORGANIZER",
            font=("Segoe UI", 20, "bold"),
            fg="#38bdf8",
            bg="#0f172a"
        )
        title.pack(pady=15)

        subtitle = tk.Label(
            header,
            text="Organize • Clean • Restore • Manage Files Effortlessly",
            font=("Segoe UI", 10),
            fg="#94a3b8",
            bg="#0f172a"
        )
        subtitle.pack()

        # ================= MAIN LAYOUT =================
        main = tk.Frame(root, bg="#0f172a")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # ================= LEFT PANEL =================
        left = tk.Frame(main, bg="#111c2e", width=280)
        left.pack(side="left", fill="y", padx=(0, 15))

        left.pack_propagate(False)

        tk.Label(
            left,
            text="CONTROL PANEL",
            font=("Segoe UI", 12, "bold"),
            fg="#e2e8f0",
            bg="#111c2e"
        ).pack(pady=15)

        # Folder label
        self.path_label = tk.Label(
            left,
            text="No folder selected",
            wraplength=250,
            justify="left",
            fg="#94a3b8",
            bg="#111c2e",
            font=("Segoe UI", 9)
        )
        self.path_label.pack(pady=10)

        # Button style function
        def btn(master, text, color, cmd):
            return tk.Button(
                master,
                text=text,
                command=cmd,
                font=("Segoe UI", 10, "bold"),
                fg="white",
                bg=color,
                activebackground="#1e293b",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                height=2,
                width=24
            )

        btn(left, "📁 Select Folder", "#3b82f6", self.select_folder).pack(pady=8)
        btn(left, "🧹 Organize Files", "#22c55e", self.organize).pack(pady=8)
        btn(left, "↩ Undo", "#f59e0b", self.undo).pack(pady=8)
        btn(left, "📊 View Report", "#a855f7", self.show_report).pack(pady=8)

        # ================= RIGHT PANEL =================
        right = tk.Frame(main, bg="#0f172a")
        right.pack(side="left", fill="both", expand=True)

        tk.Label(
            right,
            text="LIVE CONSOLE",
            font=("Segoe UI", 12, "bold"),
            fg="#e2e8f0",
            bg="#0f172a"
        ).pack(anchor="w")

        self.output = scrolledtext.ScrolledText(
            right,
            font=("Consolas", 10),
            bg="#0b1220",
            fg="#38bdf8",
            insertbackground="white",
            relief="flat"
        )
        self.output.pack(fill="both", expand=True, pady=10)

        # Bottom status bar
        self.status = tk.Label(
            root,
            text="Ready",
            bg="#020617",
            fg="#94a3b8",
            anchor="w",
            font=("Segoe UI", 9)
        )
        self.status.pack(fill="x", side="bottom")

    # ================= LOG =================
    def log(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def set_status(self, text):
        self.status.config(text=text)

    # ================= SELECT FOLDER =================
    def select_folder(self):
        self.folder_path = filedialog.askdirectory()

        if self.folder_path:
            self.path_label.config(text=self.folder_path)
            self.log(f"📁 Selected: {self.folder_path}")
            self.set_status("Folder selected")

    # ================= ORGANIZE =================
    def organize(self):

        if not self.folder_path:
            messagebox.showerror("Error", "Please select a folder first!")
            return

        self.set_status("Organizing files...")
        self.log("\n🧹 Organizing files...")

        result = organize_files(self.folder_path)

        self.log(result)
        self.set_status("Organization complete")

    # ================= UNDO =================
    def undo(self):

        if not self.folder_path:
            messagebox.showerror("Error", "Please select a folder first!")
            return

        self.set_status("Undoing changes...")
        self.log("\n↩ Undoing...")

        result = undo_organization(self.folder_path)

        self.log(result)
        self.set_status("Undo complete")

    # ================= REPORT =================
    def show_report(self):

        report_path = os.path.join(self.folder_path, "report.txt")

        if os.path.exists(report_path):

            with open(report_path, "r", encoding="utf-8") as f:
                data = f.read()

            self.log("\n📊 REPORT:\n")
            self.log(data)

        else:
            self.log("❌ No report found")


# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartOrganizerGUI(root)
    root.mainloop()