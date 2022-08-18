# Flask-VPS-Deployer

Is an auto setup tool for VPServers to handle the configuration of your Flask app.

It will:
- Auto update the server
- Update the servers IP address (If configured)
- Update the servers Hostname (If configured)
- Auto deploy a virtual environment
- Auto update pip
- Auto install from requirements.txt

It can also update all requirements in requirements.txt to the latest

### To use

Place the setup module folder in the root of your app (beside your requirements.txt file)

You can then use command flags for the project root

`python3 setup/ --project`

Outputs

```text
========================

Name: Flask-VPS-Deployer
Path: /Path/to/Project/Flask-VPS-Deployer
Contents: ['setup', 'readme.md', '.git']
Operating System: Darwin

========================
```

### The config.ini file

You will need to define some settings in the config.ini file, found inside the setup folder, it looks like this:

```text
;Supported platforms: apline, (ubuntu coming soon!)
;username = The user you want the Flask app to run as
;hostname = what the machine will be known as on the network
[DEPLOY]
platform: alpine
username: username
hostname: new_hostname

[GUNICORN]
run_file: run
;This is the file that runs your Flask app, you must leave out the .py
run_function: app
;This is the function to have gunicorn run, is usually app, but can be create_app() if you are using factory

[NETWORK]
ip_address: 192.168.1.10
netmask: 255.255.255.0
gateway: 192.168.1.1
```

If you do not want to change the settings on the network you can comment that section out like this:

```text
;[NETWORK]
;ip_address: 192.168.1.10
;netmask: 255.255.255.0
;gateway: 192.168.1.1
```

### Available options

`python3 setup --project`

This will show the path to your project and the name the deployer will use with supervisord

`python3 setup --deploy`

This will update the server and install and setup supervisord with gunicorn.

`python3 setup --install`

This will deploy a venv environment in your project folder and install requirements.txt

`python3 setup --update`

This will modify your requirements.txt to install all the latest updates or pip packages.