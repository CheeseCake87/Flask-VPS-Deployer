import subprocess
import os
import sys
import logging

from . import Project

logging.getLogger().setLevel(logging.INFO)


class Install(Project):
    def __init__(self):
        super().__init__()
        self.processor()

    def processor(self):
        self.setup_venv()
        self.install_requirements()
        logging.info(f"=> Install process complete, please reboot the server")

    def setup_venv(self):
        if "venv" not in self.project_contents:
            logging.info(f"=> venv folder not found, deploying venv...")
            subprocess.call([sys.executable, '-m', 'venv', f'{self.project_path}/venv'])

    def install_requirements(self):
        if "requirements.txt" in self.project_contents:
            if not os.path.isfile(f"{self.project_path}/venv/bin/python3"):
                raise FileNotFoundError(
                    "No python module found in venv folder, try removing venv folder and reinstalling")
            logging.info("=> Updating pip if needed...")
            subprocess.call(
                [f'{self.project_path}/venv/bin/python3', '-m', 'pip', 'install', '--upgrade', 'pip'])
            logging.info(f"=> Installing gunicorn...")
            subprocess.call(
                [f'{self.project_path}/venv/bin/python3', '-m', 'pip', 'install', 'gunicorn'])
            logging.info(f"=> Installing from requirements.txt...")
            subprocess.call(
                [f'{self.project_path}/venv/bin/python3', '-m', 'pip', 'install', '-r', f'{self.project_path}/requirements.txt'])
            logging.info(f"=> requirements.txt Installed!")
            return
        raise FileNotFoundError("requirements.txt cannot be found")
