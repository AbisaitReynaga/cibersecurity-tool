#!/bin/bash

CONFIG_FILE=/home/cibersecurity-tool/web_application/data/config.json
DATA_FILE=/home/cibersecurity-tool/web_application/data/scanning_data.json


NETWORK=$(cat $CONFIG_FILE | jq -r '.network')
NETMASK=$(cat $CONFIG_FILE | jq -r '.netmask')
sudo nmap -sn $NETWORK/$NETMASK | grep "Nmap scan report for" | awk '{print $5}' > /home/cibersecurity-tool/web_application/data/aliveHosts.txt
sudo nmap -sV -iL /home/cibersecurity-tool/web_application/data/aliveHosts.txt | awk '
/Nmap scan report for/ {
    if (host != "") {
        # Cierra el JSON del host anterior y agrega la MAC y OS si existen
        json_host = json_host "]"
        if (mac != "") {
            json_host = json_host ", \"MAC\": \"" mac "\""
        }
        if (os != "") {
            json_host = json_host ", \"OS\": \"" os "\""
        }
        print json_host "},"
    }
    host = $5
    json_host = "{ \"Host\": \"" host "\", \"Services\": ["
    first = 1
    mac = ""
    os = ""
}
/open/ {
    if (!first) {
        json_host = json_host ","
    }
    first = 0
    port = $1
    status = $2
    protocol = $3
    service = $4
    json_host = json_host "{ \"Port\": \"" port "\", \"Status\": \"" status "\", \"Protocol\": \"" protocol "\", \"Service\": \"" service "\"}"
}
/MAC Address:/ {
    mac = $3
    for (i=4; i<=NF; i++) {
        mac = mac " " $i
    }
}
/Service Info: OS:/ {
    os = substr($0, index($0, "OS:") + 4)
}
END {
    if (host != "") {
        # Cierra el JSON del último host y agrega la MAC y OS si existen
        json_host = json_host "]"
        if (mac != "") {
            json_host = json_host ", \"MAC\": \"" mac "\""
        }
        if (os != "") {
            json_host = json_host ", \"OS\": \"" os "\""
        }
        print json_host "}"
    }
}' >  /home/cibersecurity-tool/web_application/data/temp.json

echo "[" > $DATA_FILE
cat  /home/cibersecurity-tool/web_application/data/temp.json >> $DATA_FILE
echo "]" >> $DATA_FILE


