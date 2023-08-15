import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import os
from ttkthemes import ThemedStyle

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tabela de Fornecedores")
        self.geometry("800x600")

        style = ThemedStyle(self)
        style.set_theme("clearlooks")  # Escolha um tema claro

        self.create_widgets()
        
    def create_widgets(self):
        self.header_label = ttk.Label(self, text="Tabela de Fornecedores", font=("Helvetica", 16))
        self.header_label.pack(pady=(10, 0))  # Aumentar o espaçamento superior
        
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(anchor="nw", padx=10, pady=(0, 5))  # Ancorar os botões na parte superior esquerda

        self.select_button = ttk.Button(self.buttons_frame, text="Selecionar Arquivo CSV", command=self.select_csv)
        self.select_button.pack(side="top", pady=(5, 0))  # Ajustar espaçamento
        
        self.menu_button_frame = tk.Frame(self)
        self.menu_button_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        self.create_menu_buttons()

        self.file_info_frame = ttk.Frame(self, padding=10)
        self.file_info_frame.pack(anchor="ne", padx=10, pady=(0, 5))  # Ancorar as informações à direita

        self.file_name_label = ttk.Label(self.file_info_frame, text="Nome do arquivo: ", font=("Roboto", 10), anchor="e")
        self.file_name_label.pack(side="right")
        
        self.file_size_label = ttk.Label(self.file_info_frame, text="Tamanho do arquivo: ", font=("Roboto", 10), anchor="e")
        self.file_size_label.pack(side="right", padx=10)
        
        self.file_modified_label = ttk.Label(self.file_info_frame, text="Data de modificação: ", font=("Roboto", 10), anchor="e")
        self.file_modified_label.pack(side="right")

        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_frame.grid_rowconfigure(0, weight=1)  # Configurar a altura da linha
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("Material", "Soma de Saldo", "Último UM pedido", "Data de remessa mais recente", "Primeiro Fornecedor"), show="headings", style="Custom.Treeview")
        self.tree.heading("Material", text="Material")
        self.tree.heading("Soma de Saldo", text="Soma de Saldo")
        self.tree.heading("Último UM pedido", text="Último UM pedido")
        self.tree.heading("Data de remessa mais recente", text="Data de remessa mais recente")
        self.tree.heading("Primeiro Fornecedor", text="Primeiro Fornecedor")

        column_widths = (0.2, 0.2, 0.2, 0.2, 0.2)  # Porcentagens das larguras das colunas
        for col, width in zip(self.tree["columns"], column_widths):
            self.tree.column(col, stretch=False)
            self.tree.column(col, width=int(self.tree.winfo_reqwidth() * width))
        self.tree.grid(row=0, column=0, sticky="nsew")  # Grid da tabela
        
        self.scrollbar_y = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        self.tree_frame.grid_columnconfigure(0, weight=1)  # Redimensionar com a janela
        self.tree_frame.grid_rowconfigure(0, weight=1)  # Redimensionar com a janela

        self.bind("<Configure>", self.on_window_resize)

        self.tree_height = 5  # Defina a altura desejada (em número de linhas)
        self.tree.bind("<Configure>", self.on_tree_resize)

        self.loaded_file_info = {}

    def create_menu_buttons(self):
        menu_buttons = [
            ("Botão 1", self.on_button1_click),
            ("Botão 2", self.on_button2_click),
            ("Botão 3", self.on_button3_click)
            # Adicione mais botões conforme necessário
        ]
        
        for text, command in menu_buttons:
            button = ttk.Button(self.menu_button_frame, text=text, command=command)
            button.pack(side="left", padx=5)

    def on_button1_click(self):
        print("Botão 1 clicado")

    def on_button2_click(self):
        print("Botão 2 clicado")

    def on_button3_click(self):
        print("Botão 3 clicado")

    def select_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
        if file_path:
            self.load_data(file_path)
            self.update_loaded_file_info(file_path)
    
    def update_loaded_file_info(self, file_path):
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_modified = os.path.getmtime(file_path)
        
        self.loaded_file_info["name"] = file_name
        self.loaded_file_info["size"] = file_size
        self.loaded_file_info["modified"] = file_modified
        
        self.update_file_info_labels()

    def update_file_info_labels(self):
        self.file_name_label.config(text=f"Nome do arquivo: {self.loaded_file_info.get('name', '')}")
        self.file_size_label.config(text=f"Tamanho do arquivo: {self.format_file_size(self.loaded_file_info.get('size', 0))}")
        
        modified_time = self.loaded_file_info.get('modified', 0)
        self.file_modified_label.config(text=f"Data de modificação: {self.format_timestamp(modified_time)}")

    def format_timestamp(self, timestamp):
        import datetime
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    def format_file_size(self, size_in_bytes):
        size_kb = size_in_bytes / 1024
        return f"{size_kb:.2f} KB"

    def load_data(self, file_path):
        # Carregar dados do CSV usando pandas
        data = pd.read_csv(file_path)

        self.tree.delete(*self.tree.get_children())  # Limpar dados anteriores

        for index, row in data.iterrows():
            material = row.get("Material", "")
            saldo = row.get("Soma de Saldo", "")
            ultimo_um_pedido = row.get("Último UM pedido", "")
            remessa_recente = row.get("Data de remessa mais recente", "")
            primeiro_fornecedor = row.get("Primeiro Fornecedor", "")
            
            self.tree.insert("", "end", values=(material, saldo, ultimo_um_pedido, remessa_recente, primeiro_fornecedor))
        
    def on_window_resize(self, event):
        self.update_column_widths()

    def update_column_widths(self):
        total_width = self.tree.winfo_width()
        column_widths = (0.2, 0.2, 0.2, 0.2, 0.2)  # Porcentagens das larguras das colunas
        for col, width in zip(self.tree["columns"], column_widths):
            self.tree.column(col, width=int(total_width * width))

    def on_tree_resize(self, event):
        self.tree_height_pixels = self.tree_height * self.tree.winfo_reqheight()
        self.tree.config(height=self.tree_height_pixels)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
