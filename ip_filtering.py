import tkinter as tk
from tkinter import filedialog, messagebox, font

class LineCounter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.line = []

    def read(self):
        with open(self.file_name, "r") as f:
            self.line = f.readlines()

    def feth_ip_add(self):
        self.ip_add = list(map(lambda x: x.split(" ")[0], self.line))
        return self.ip_add

    def ip_filter(self, num):
        self.less_20 = list(filter(lambda x: int(x.split(".")[0]) < num, self.ip_add))

    def ratio(self):
        return len(self.less_20) / len(self.ip_add) if self.ip_add else 0

class IPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Address Filter")
        self.root.geometry("700x600")  # Increased window size
        self.root.configure(bg="#f0f4f8")

        # Font
        self.text_font = font.Font(family="Helvetica", size=12)

        # File label
        self.file_label = tk.Label(root, text="No file selected", bg="#f0f4f8", font=self.text_font)
        self.file_label.pack(pady=10)

        self.load_button = tk.Button(root, text="📂 Select Log File", command=self.load_file, font=self.text_font, width=20, bg="#4caf50", fg="white")
        self.load_button.pack(pady=10)

        # Filter number entry
        self.num_label = tk.Label(root, text="Enter filter number (e.g., 30):", bg="#f0f4f8", font=self.text_font)
        self.num_label.pack()

        self.num_entry = tk.Entry(root, font=self.text_font, width=10)
        self.num_entry.pack(pady=5)

        # Radio button frame
        self.show_ips_var = tk.IntVar(value=1)  # default Yes
        radio_frame = tk.Frame(root, bg="#f0f4f8")
        tk.Label(radio_frame, text="Show IPs in output:", bg="#f0f4f8", font=self.text_font).pack(side=tk.LEFT)
        tk.Radiobutton(radio_frame, text="Yes", variable=self.show_ips_var, value=1, bg="#f0f4f8", font=self.text_font).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(radio_frame, text="No", variable=self.show_ips_var, value=0, bg="#f0f4f8", font=self.text_font).pack(side=tk.LEFT, padx=5)
        radio_frame.pack(pady=10)

        # Process button
        self.process_button = tk.Button(root, text="⚙️ Process", command=self.process_file, font=self.text_font, width=15, bg="#2196f3", fg="white")
        self.process_button.pack(pady=10)

        # Output text (read-only)
        self.output_text = tk.Text(root, height=20, width=80, font=self.text_font, state="disabled", bg="#ffffff")
        self.output_text.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.line_counter = LineCounter(file_path)
            self.line_counter.read()
            self.file_label.config(text=f"Loaded: {file_path.split('/')[-1]}")

    def process_file(self):
        if not hasattr(self, 'line_counter') or not self.line_counter:
            messagebox.showerror("Error", "Please load a file first.")
            return

        try:
            num = int(self.num_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        self.line_counter.feth_ip_add()
        self.line_counter.ip_filter(num)
        ratio = self.line_counter.ratio()
        total_ips = len(self.line_counter.ip_add)
        filtered_ips = self.line_counter.less_20

        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)

        self.output_text.insert(tk.END, f"📊 Total IPs: {total_ips}\n")
        self.output_text.insert(tk.END, f"✅ Filtered IPs (first octet < {num}): {len(filtered_ips)}\n")
        self.output_text.insert(tk.END, f"📈 Ratio: {ratio:.2f}\n")

        if self.show_ips_var.get() == 1:
            self.output_text.insert(tk.END, "\nFiltered IP List:\n")
            for ip in filtered_ips:
                self.output_text.insert(tk.END, f"• {ip}\n")

        self.output_text.config(state="disabled")  # Make it read-only

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = IPApp(root)
    root.mainloop()