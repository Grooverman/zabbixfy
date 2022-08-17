# Zabbixfy
### Receive data for Zabbix without any zabbix agent, just plain JSON over HTTP.

Installation instructions (Ubuntu):
```
git clone https://github.com/Grooverman/zabbixfy.git
cd zabbixfy
virtualenv .venv
source .venv/bin/activate
pip install flask flask_restful py-zabbix gunicorn
sudo ln -s $(pwd) /opt/zabbixfy
sudo cp zabbixfy.service /etc/systemd/system/zabbixfy.service
sudo systemctl daemon-reload
```

Test it:
```
curl -H 'Content-Type: application/json' -d '[["healthchecks", "health.check", "1"], ["321", "A", "B"]]' 127.0.0.1:5000
```
