import os
import platform
import logging
import configparser


class Project:
    project_path: str = None
    project_contents: list = None
    project_name: str = None
    operating_system: str = None
    config = None

    def __init__(self):
        this_file_location = os.path.abspath(__file__).split("/")
        project_path_jump = this_file_location[:-3]
        self.config = configparser.ConfigParser()
        self.project_path = "/".join(project_path_jump)
        self.project_name = project_path_jump[-1]
        self.project_contents = os.listdir(self.project_path)
        self.operating_system = platform.system()
        self.operating_system_check()

    def read_config(self):
        if not os.path.isfile(f"{self.project_path}/setup/config.ini"):
            logging.critical("=> Unable to located the config.ini in setup folder, system will be unable to deploy")
        else:
            self.config.read(f"{self.project_path}/setup/config.ini")

    def operating_system_check(self):
        if self.operating_system == "Linux":
            return
        if self.operating_system == "Darwin":
            return
        logging.critical("=> Operating system not supported!")

    def details(self):
        print("========================")
        print("")
        self.read_config()
        print("Name:", self.project_name)
        print("Path:", self.project_path)
        print("Contents:", self.project_contents)
        print("Operating System:", self.operating_system)
        print("")
        print("========================")
