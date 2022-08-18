from dataclasses import dataclass


@dataclass
class Resources:
    alpine_setup_sh = """
setup-hostname ::hostname::
setup-keymap gb gb
apk update &&
apk upgrade &&
apk add htop &&
apk add musl-dev &&
apk add g++ &&
apk add supervisor
rc-update add supervisord boot
    """

    alpine_network_interface = """
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
        address ::ip_address::
        netmask ::netmask::
        gateway ::gateway::
"""

    supervisor_config = """
[program:flask]
directory=::project_path::
command=::project_path::/venv/bin/gunicorn -b 0.0.0.0:5000 -w 3 run:gunicorn
user=::user::
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stdout_logfile=::project_path::/error.log
stderr_logfile=::project_path::/general.log
    """
