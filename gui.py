from logic import Model
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

class CustomTree(ttk.Treeview):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self["columns"] = ("Material", "Soma de Saldo", "Último UM pedido", "Data de remessa mais recente", "Primeiro Fornecedor")
        self["show"] = "headings"
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview", highlightthickness=0, bd=0)
        self.configure(style="Custom.Treeview")

        for col in self["columns"]:
            self.heading(col, text=col)

class Application(tk.Tk):
    def __init__(self, model):
        super().__init__()

        self.model = model

        self.title("Tabela de Fornecedores")
        self.geometry("800x600")

        # Defina as cores de fundo e de texto
        dark_blue = "#001f3f"  # Azul escuro
        light_blue = "#add8e6"  # Azul claro
        button_bg_color = "#4682b4"  # Azul-ardósia médio para o fundo dos botões
        title_bg_color = "#87ceeb"  # Azul-ardósia claro para o fundo dos títulos

        self.configure(bg=dark_blue)  # Define a cor de fundo geral da janela
        self.create_widgets(dark_blue, light_blue, button_bg_color, title_bg_color)

    def create_buttons_frame(self, button_bg_color):
        self.buttons_frame = tk.Frame(self, bg=button_bg_color)
        self.buttons_frame.pack(anchor="nw", padx=10, pady=(0, 5))

        # Adicione uma imagem ao botão
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "csv.png")
        select_image = Image.open(image_path)
        select_image = select_image.resize((30, 30), resample=Image.BICUBIC)
        select_image = ImageTk.PhotoImage(select_image)

        # Configure um estilo para os botões antes de criar o botão
        style = ttk.Style()
        style.configure("Custom.TButton", background=button_bg_color, foreground="white")

        self.select_button = ttk.Button(self.buttons_frame, text="Selecionar Arquivo CSV", command=self.select_csv, image=select_image, compound="left", style="Custom.TButton")
        self.select_button.image = select_image
        self.select_button.pack(side="top", pady=(5, 0))

    def create_widgets(self, bg_color, fg_color, button_bg_color, title_bg_color):
        self.create_header(title_bg_color)
        self.create_buttons_frame(button_bg_color)
        self.create_menu_button_frame(button_bg_color)
        self.create_file_info_frame(title_bg_color)
        self.create_tree_frame(bg_color)

        self.bind("<Configure>", self.on_window_resize)
        self.tree.bind("<Configure>", self.on_tree_resize)

    def create_header(self, bg_color):
        self.header_label = ttk.Label(self, text="Tabela de Fornecedores", font=("Arial", 16, "bold"), background=bg_color, foreground="#ffffff")
        self.header_label.pack(pady=(10, 0))

    def create_menu_button_frame(self, button_bg_color):
        self.menu_button_frame = tk.Frame(self, bg=button_bg_color)
        self.menu_button_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        self.create_menu_buttons(button_bg_color)

    def create_file_info_frame(self, bg_color):
        self.file_info_frame = ttk.Frame(self, style="Custom.TFrame")
        self.file_info_frame["style"] = "Custom.TFrame"
        self.file_info_frame.pack(anchor="ne", padx=10, pady=(0, 5))

        self.file_name_label = ttk.Label(self.file_info_frame, text="Nome do arquivo: ", font=("Roboto", 10), anchor="e", style="Custom.TLabel")
        self.file_name_label.grid(row=0, column=0, sticky="e")

        self.file_size_label = ttk.Label(self.file_info_frame, text="Tamanho do arquivo: ", font=("Roboto", 10), anchor="e", style="Custom.TLabel")
        self.file_size_label.grid(row=0, column=1, padx=10, sticky="e")

        self.file_modified_label = ttk.Label(self.file_info_frame, text="Data de modificação: ", font=("Roboto", 10), anchor="e", style="Custom.TLabel")
        self.file_modified_label.grid(row=0, column=2, sticky="e")

    def create_tree_frame(self, bg_color):
        self.tree_frame = tk.Frame(self, bg=bg_color)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_frame.grid_rowconfigure(0, weight=1)

        self.tree = CustomTree(self.tree_frame)
        self.tree.grid(row=0, column=0, sticky="nsew")

        self.scrollbar_y = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)

    def create_menu_buttons(self, button_bg_color):
        menu_buttons = [
            ("Botão 1", self.on_button1_click),
            ("Botão 2", self.on_button2_click),
            ("Botão 3", self.on_button3_click),
            ("Salvar CSV", self.save_csv),
            ("Editar Dados", self.edit_data),
            ("Filtrar Dados", self.filter_data),
            ("Ordenar Dados", self.sort_data),
            ("Adicionar Dados", self.add_data),
            ("Excluir Dados", self.delete_data),
            ("Exportar CSV", self.export_csv)
        ]

        for text, command in menu_buttons:
            button = ttk.Button(self.menu_button_frame, text=text, command=command, style="Custom.TButton", cursor="hand2", padding=5)
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
            success = self.model.load_data(file_path)
            if success:
                self.update_loaded_file_info(file_path)
                messagebox.showinfo("Sucesso", "Arquivo CSV carregado com sucesso.")
                self.display_data_in_tree()
            else:
                messagebox.showerror("Erro", "Falha ao carregar arquivo CSV.")

    def update_loaded_file_info(self, file_path):
        self.model.update_loaded_file_info(file_path)
        self.update_file_info_labels()

    def update_file_info_labels(self):
        file_name = self.model.loaded_file_info.get('name', '')
        file_size = self.format_file_size(self.model.loaded_file_info.get('size', 0))
        modified_time = self.format_timestamp(self.model.loaded_file_info.get('modified', 0))

        self.file_name_label.config(text=f"Nome do arquivo: {file_name}")
        self.file_size_label.config(text=f"Tamanho do arquivo: {file_size}")
        self.file_modified_label.config(text=f"Data de modificação: {modified_time}")

    def format_timestamp(self, timestamp):
        import datetime
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def format_file_size(self, size_in_bytes):
        size_kb = size_in_bytes / 1024
        return f"{size_kb:.2f} KB"

    def on_window_resize(self, event):
        self.update_column_widths()

    def update_column_widths(self):
        total_width = self.tree.winfo_width()
        column_widths = (0.2, 0.2, 0.2, 0.2, 0.2)
        for col, width in zip(self.tree["columns"], column_widths):
            self.tree.column(col, width=int(total_width * width))

    def on_tree_resize(self, event):
        tree_height_pixels = 5 * self.tree.winfo_reqheight()
        self.tree.config(height=tree_height_pixels)

    def save_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivos CSV", "*.csv")])
        if file_path:
            success = self.model.save_data(file_path)
            if success:
                messagebox.showinfo("Sucesso", "CSV salvo com sucesso.")
            else:
                messagebox.showerror("Erro", "Falha ao salvar CSV.")

    def edit_data(self):
        # Implemente a edição de dados aqui
        pass

    def filter_data(self):
        # Implemente a filtragem de dados aqui
        pass

    def sort_data(self):
        # Implemente a ordenação de dados aqui
        pass

    def add_data(self):
        # Implemente a adição de dados aqui
        pass

    def delete_data(self):
        # Implemente a exclusão de dados aqui
        pass

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivos CSV", "*.csv")])
        if file_path:
            success = self.model.export_to_csv(file_path)
            if success:
                messagebox.showinfo("Sucesso", "CSV exportado com sucesso.")
            else:
                messagebox.showerror("Erro", "Falha ao exportar CSV.")

    def display_data_in_tree(self):
        self.tree.delete(*self.tree.get_children())
        if self.model.data is not None:
            for index, row in self.model.data.iterrows():
                material = row.get("Material", "")
                saldo = row.get("Soma de Saldo", "")
                ultimo_um_pedido = row.get("Último UM pedido", "")
                remessa_recente = row.get("Data de rem")
                # Adicione as colunas restantes conforme necessário

if __name__ == "__main__":
    model = Model()
    app = Application(model)
    app.mainloop()
