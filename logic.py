import pandas as pd
import os

class Model:
    def __init__(self):
        self.loaded_file_info = {}
        self.data = None

    def load_data(self, file_path):
        try:
            self.data = pd.read_csv(file_path)
            return True
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return False

    def update_loaded_file_info(self, file_path):
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_modified = os.path.getmtime(file_path)

        self.loaded_file_info["name"] = file_name
        self.loaded_file_info["size"] = file_size
        self.loaded_file_info["modified"] = file_modified

    def save_data(self, file_path):
        try:
            self.data.to_csv(file_path, index=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False

    def edit_data(self, row_index, column_name, new_value):
        try:
            self.data.at[row_index, column_name] = new_value
            return True
        except Exception as e:
            print(f"Erro ao editar dados: {e}")
            return False

    def add_data(self, new_data):
        try:
            self.data = pd.concat([self.data, new_data], ignore_index=True)
            return True
        except Exception as e:
            print(f"Erro ao adicionar dados: {e}")
            return False

    def delete_data(self, row_index):
        try:
            self.data = self.data.drop(index=row_index).reset_index(drop=True)
            return True
        except Exception as e:
            print(f"Erro ao excluir dados: {e}")
            return False

    def export_to_csv(self, file_path):
        try:
            self.data.to_csv(file_path, index=False)
            return True
        except Exception as e:
            print(f"Erro ao exportar dados: {e}")
            return False
