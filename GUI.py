import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.colorchooser import askcolor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import json
import os


def clean_folder(folder_path, file_extension):
    for filename in os.listdir(folder_path):
        if filename.endswith(file_extension):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
class CircleGridApp:
    def __init__(self, root):
        current_directory = os.getcwd()

        ttool_audio_directory = os.path.join(current_directory, "tttool")
        if os.path.exists(ttool_audio_directory):
            clean_folder(ttool_audio_directory, ".gme")
        self.root = root
        self.root.title("Circle Grid Generator")

        self.border_thickness = tk.StringVar(value="2")
        self.circle_text_position = tk.StringVar(value="top_left")
        self.circle_border_color = "#000000"
        self.circle_text_entries = []
        self.saved_data = {}

        self.create_widgets()
    def create_widgets(self):
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=frame, anchor="nw")

        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        center_frame = ttk.Frame(frame)
        center_frame.pack(expand=True, pady=20)

        circle_frame = ttk.Frame(center_frame)
        circle_frame.pack()

        self.create_circle_grid(circle_frame)

        ttk.Label(center_frame, text="Circle Text Position:").pack(pady=(10, 0))
        ttk.Radiobutton(center_frame, text="Top Left", variable=self.circle_text_position, value="top_left").pack()
        ttk.Radiobutton(center_frame, text="Center", variable=self.circle_text_position, value="center").pack()

        load_frame = ttk.Frame(center_frame)
        load_frame.pack(pady=20)

        ttk.Button(load_frame, text="Load CSV", command=self.load_csv).pack()

        text_entry_frame = ttk.Frame(center_frame)
        text_entry_frame.pack(pady=(20, 0))

        self.create_text_entries(text_entry_frame)

        ttk.Label(center_frame, text="Border Thickness:").pack(pady=(20, 0))
        ttk.Entry(center_frame, textvariable=self.border_thickness).pack()

        ttk.Button(center_frame, text="Choose Circle Border Color", command=self.choose_circle_border_color).pack(pady=20)
        ttk.Button(center_frame, text="Generate PDF", command=self.generate_pdf).pack()

        frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def choose_circle_border_color(self):
        color = askcolor()[1]
        if color:
            self.circle_border_color = color

    def create_circle_grid(self, parent):
        for _ in range(6):
            circle_row = ttk.Frame(parent)
            circle_row.pack()

            for _ in range(4):
                circle = ttk.Label(circle_row, text="O", font=("Helvetica", 16))
                circle.pack(side=tk.LEFT, padx=10)

    def create_text_entries(self, parent):
        for _ in range(6):
            entry_row = ttk.Frame(parent)
            entry_row.pack()

            for _ in range(4):
                entry = ttk.Entry(entry_row)
                entry.pack(side=tk.LEFT, padx=10, pady=10)
                self.circle_text_entries.append(entry)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            with open(file_path, "r") as file:
                lines = file.readlines()

            for i, line in enumerate(lines[:6]):
                values = line.strip().split(";")
                for j, value in enumerate(values[:4]):
                    self.circle_text_entries[i * 4 + j].delete(0, tk.END)
                    self.circle_text_entries[i * 4 + j].insert(0, value)

    def generate_pdf(self):
        filename = "circle_grid.pdf"
        border_thickness = float(self.border_thickness.get())
        circle_text_position = self.circle_text_position.get()

        self.saved_data = {"circles": []}

        for number, entry in enumerate(self.circle_text_entries, start=1):
            text = entry.get().strip()
            if text:
                circle_data = {
                    "number": number,
                    "text": text,
                    "x": 0,
                    "y": 0
                }
                self.saved_data["circles"].append(circle_data)

        page_width, page_height = A4
        circle_diameter = 4 * cm
        circle_spacing = 0.6 * cm
        margin_top =1.35 * cm
        margin_left = 1.6 * cm
        circle_radius = circle_diameter / 2

        for circle_data in self.saved_data["circles"]:
            number = circle_data["number"]
            row = (number - 1) // 4
            col = (number - 1) % 4
            circle_data["x"] = margin_left + circle_radius + col * (circle_diameter + circle_spacing)
            circle_data["y"] = page_height - margin_top - circle_radius - row * (circle_diameter + circle_spacing)

        c = canvas.Canvas(filename, pagesize=A4)

        for circle_data in self.saved_data["circles"]:
            x = circle_data["x"]
            y = circle_data["y"]

            c.setStrokeColor(self.circle_border_color)
            c.setLineWidth(border_thickness)
            c.circle(x, y, circle_radius)

            number_text = str(circle_data["number"])
            text_width = c.stringWidth(number_text, "Helvetica", 12)
            text_x = x - circle_radius - text_width + 28
            text_y = y + circle_radius - 26
            if circle_text_position == "center":
                text_x = x - text_width / 2
                text_y = y - text_width / 2
            c.setFont("Helvetica", 12)
            c.drawString(text_x, text_y, number_text)

        c.showPage()
        c.save()

        json_filename = "circle_data.json"
        with open(json_filename, "w") as json_file:
            json.dump(self.saved_data, json_file, indent=4)

        filename_data = "circle_grid_data.pdf"
        c = canvas.Canvas(filename_data, pagesize=A4)
        c.setFont("Helvetica", 12)

        for circle_data in self.saved_data["circles"]:
            number = circle_data["number"]
            text = circle_data["text"]
            c.drawString(2 * cm, page_height - (number) * 1.2 * cm, f"{number}: {text}")
        for circle_data in self.saved_data["circles"]:
            circle_data["x"] = circle_data["x"]
            circle_data["y"] = circle_data["y"]

        c.showPage()
        c.save()

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CircleGridApp(root)
    root.mainloop()