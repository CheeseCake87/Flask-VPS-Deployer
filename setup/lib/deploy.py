import subprocess
import os
import logging

from . import Project
from .resources import Resources

logging.getLogger().setLevel(logging.INFO)


class Deploy(Project):
    def __init__(self):
        super().__init__()
        self.processor()

    def processor(self):
        if self.config['DEPLOY']['platform'] == "alpine" and self.operating_system == "Linux":
            self.setup_alpine()
        logging.critical("=> Unable to deploy, platform + OS do not meet requirements.")

    def setup_alpine(self):
        logging.info(f"=> Setting up alpine environment...")
        with open(f"{self.project_path}/setup/alpine_setup.sh", mode="w") as alpine_setup:
            alpine_setup.write(Resources.alpine_setup_sh)

        subprocess.call(['ash', f'{self.project_path}/setup/alpine_setup.sh'])

        if self.config.has_option("DEPLOY", "hostname"):
            subprocess.call(['setup-hostname', f"{self.config['DEPLOY']['hostname']}"])

        if not os.path.exists("/etc/supervisor.d/"):
            os.mkdir("/etc/supervisor.d")

        if self.config.has_section("GUNICORN") and self.config.has_section("DEPLOY"):
            write_supervisor = True
            if not self.config.has_option("GUNICORN", "run_file") and write_supervisor:
                write_supervisor = False
            if not self.config.has_option("NETWORK", "run_function") and write_supervisor:
                write_supervisor = False
            if write_supervisor:
                with open(f"/etc/supervisor.d/{self.project_name}.ini", mode="w") as supervisor_config:
                    supervisor_config.write(
                        Resources.supervisor_config.replace(
                            "::project_path::", self.project_path
                        ).replace(
                            "::user::", self.config['DEPLOY']['username']
                        )
                    )
            else:
                logging.info("=> GUNICORN Section is disabled or contains an error, supervisor update skipped.")

        if self.config.has_section("NETWORK"):
            write_network = True
            if not self.config.has_option("NETWORK", "ip_address") and write_network:
                write_network = False
            if not self.config.has_option("NETWORK", "netmask") and write_network:
                write_network = False
            if not self.config.has_option("NETWORK", "gateway") and write_network:
                write_network = False
            if write_network:
                with open(f"/etc/network/interfaces", mode="w") as network_interfaces:
                    network_interfaces.write(
                        Resources.alpine_network_interface.replace(
                            "::ip_address::", self.config['DEPLOY']['ip_address']
                        ).replace(
                            "::netmask::", self.config['DEPLOY']['netmask']
                        ).replace(
                            "::gateway::", self.config['DEPLOY']['gateway']
                        )
                    )
            else:
                logging.info("=> NETWORK Section is disabled or contains an error, network update skipped.")

        logging.info("=> Deployment complete, now do setup.py --install.")
