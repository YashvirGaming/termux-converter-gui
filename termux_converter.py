import os
import customtkinter as ctk
from tkinter import filedialog
from colorama import Fore, init

init(autoreset=True)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class TermuxConverter(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Termux Converter • Yashvir Gaming")
        self.geometry("780x480")
        self.configure(fg_color="#0d0d0d")

        self.label = ctk.CTkLabel(
            self,
            text="🔥 Termux Checker Converter 🔥",
            font=("Consolas", 24, "bold"),
            text_color="lime"
        )
        self.label.pack(pady=20)

        self.textbox = ctk.CTkTextbox(
            self,
            width=650,
            height=240,
            font=("Consolas", 14),
            fg_color="#1a1a1a",
            text_color="lime"
        )
        self.textbox.pack(pady=10)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=15)

        self.button_check = ctk.CTkButton(
            btn_frame,
            text="Check & Convert",
            command=self.convert,
            fg_color="#00ff00",
            hover_color="#008000"
        )
        self.button_check.grid(row=0, column=0, padx=10)

        self.button_browse = ctk.CTkButton(
            btn_frame,
            text="Browse Script",
            command=self.browse_script,
            fg_color="#00ccff",
            hover_color="#006699"
        )
        self.button_browse.grid(row=0, column=1, padx=10)

        self.script_path = None

    def log(self, msg, color=Fore.LIGHTGREEN_EX):
        self.textbox.insert("end", f"{color}{msg}{Fore.RESET}\n")
        self.textbox.see("end")

    def browse_script(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            self.script_path = file_path
            self.log(f"📂 Selected script: {file_path}", Fore.CYAN)

    def ensure_files(self):
        for fname in ["combos.txt", "proxies.txt"]:
            if not os.path.exists(fname):
                open(fname, "w").close()
                self.log(f"[AUTO] Created missing {fname}", Fore.YELLOW)
            else:
                self.log(f"[OK] {fname} found", Fore.GREEN)

    def patch_script(self, src_file):
        with open(src_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        patched_lines = []
        for line in lines:
            if "input(" in line and "combo" in line.lower():
                patched_lines.append('combos_path = "combos.txt"\n')
                continue
            if "input(" in line and "proxy" in line.lower():
                patched_lines.append('proxies_path = "proxies.txt"\n')
                continue
            if ".strip()" in line:
                patched_lines.append(line.replace(".strip()", ".rstrip(\"\\n\")"))
                continue
            patched_lines.append(line)

        new_file = src_file.replace(".py", "_termux.py")
        with open(new_file, "w", encoding="utf-8") as f:
            f.writelines(patched_lines)

        return new_file

    def convert(self):
        self.textbox.delete("1.0", "end")
        self.ensure_files()

        if self.script_path:
            self.log(f"\n✨ Converting script: {self.script_path}", Fore.YELLOW)
            new_file = self.patch_script(self.script_path)
            self.log("➡ Removed drag & drop logic", Fore.LIGHTCYAN_EX)
            self.log("➡ Hardcoded combos.txt & proxies.txt paths", Fore.LIGHTCYAN_EX)
            self.log("➡ Replaced .strip() with .rstrip(\"\\n\")", Fore.LIGHTCYAN_EX)
            self.log(f"➡ Saved as: {new_file}", Fore.LIGHTCYAN_EX)
            self.log("\n✅ Conversion completed successfully!", Fore.LIGHTGREEN_EX)
        else:
            self.log("\n⚠ No script selected. Browse one to convert.", Fore.RED)


if __name__ == "__main__":
    app = TermuxConverter()
    app.mainloop()
