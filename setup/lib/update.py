import subprocess
import os
import logging

from . import Project

logging.getLogger().setLevel(logging.INFO)


class Update(Project):
    project_path = None
    project_contents = None
    search_path1 = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    search_path2 = os.getcwd()

    def __init__(self):
        super().__init__()
        self.write_currently_installed()
        self.do_update()

    def write_currently_installed(self):
        current_freeze = subprocess.check_output([f'{self.project_path}/venv/bin/python3', '-m', 'pip', 'freeze'])
        decode = current_freeze.decode("utf-8")
        with open(f"{self.project_path}/requirements.txt", mode="w") as current_req:
            current_req.write(decode.replace("==", ">="))
        logging.info("=> Current packages added to requirements.txt")

    def do_update(self):
        if "requirements.txt" in self.project_contents:
            if not os.path.isfile(f"{self.project_path}/venv/bin/python3"):
                raise FileNotFoundError(
                    "No python module found in venv folder, try removing venv folder and reinstalling")
            logging.info("=> Updating pip if needed...")
            subprocess.call(
                [f'{self.project_path}/venv/bin/python3', '-m', 'pip', 'install', '--upgrade', 'pip'])
            logging.info(f"=> Updating from requirements.txt...")
            subprocess.call(
                [f'{self.project_path}/venv/bin/python3', '-m', 'pip', 'install', '-r',
                 f'{self.project_path}/requirements.txt'])
            logging.info(f"=> requirements.txt Installed!")
            return
        raise FileNotFoundError("requirements.txt cannot be found")
