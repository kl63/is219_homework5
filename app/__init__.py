import pkgutil
import importlib
from app.commands import CommandHandler
from app.commands import Command
from app.plugins.menu import MenuCommand
import multiprocessing
from dotenv import load_dotenv
import os



class App:
    def __init__(self):
        load_dotenv()
        self.settings = {}  # Initialize settings as an empty dictionary
        # Load all environment variables into settings
        for key, value in os.environ.items():
            self.settings[key] = value
        # Default to 'PRODUCTION' if 'ENVIRONMENT' not set
        self.settings.setdefault('ENVIRONMENT', 'TESTING')   
        self.command_handler = CommandHandler()
    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings[env_var]

    def load_plugins(self):
        plugins_package = 'app.plugins'
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_package.replace('.', '/')]):
            if is_pkg:
                plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)
                    try:
                        if issubclass(item, (Command)):
                            self.command_handler.register_command(plugin_name, item())
                    except TypeError:
                        continue

        self.command_handler.register_command("menu", MenuCommand(self.command_handler))

    def start(self):
        self.load_plugins()
        print("Type 'exit' to exit.")
        while True:
            self.command_handler.execute_command(input(">>> ").strip())

def start_app():
    app = App()
    app.start()

if __name__ == "__main__":
    multiprocessing.Process(target=start_app).start()