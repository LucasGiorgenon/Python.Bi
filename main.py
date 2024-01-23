from gui import Application
from logic import Model

if __name__ == "__main__":
    model = Model()
    app = Application(model)
    app.mainloop()
