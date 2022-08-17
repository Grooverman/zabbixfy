# Zabbixfy
### Receive data for Zabbix without any zabbix agent, just plain JSON over HTTP.

#### Installation instructions (Ubuntu):
```
git clone https://github.com/Grooverman/zabbixfy.git
cd zabbixfy
virtualenv .venv
source .venv/bin/activate
pip install flask flask_restful py-zabbix gunicorn
sudo ln -s $(pwd) /opt/zabbixfy
sudo cp zabbixfy.service /etc/systemd/system/zabbixfy.service
sudo systemctl daemon-reload
sudo systemctl start zabbixfy
sudo systemctl enable zabbixfy
```

Test it:
```
curl -H 'Content-Type: application/json' -d '[["healthchecks", "health.check", "1"], ["321", "A", "B"]]' 127.0.0.1:5000
```

Add the following to your `/etc/nginx/conf.d/zabbix.conf` file, below the line that says `index   index.php;`:
```
        location /zabbixfy/ {
                proxy_pass http://127.0.0.1:5000/;
                proxy_redirect   off;
                proxy_set_header Host $http_host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
        }
```
Execute:
```
sudo systemctl reload nginx
```
Now the Zabbixfy API should be available at your Zabbix Frontend and you should be able to receive monitoring data from any HTTP client. 
