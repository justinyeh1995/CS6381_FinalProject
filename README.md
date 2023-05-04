# CS6381 FinalProject

## On Master Node 1 (Main)

1. Start Zookeeper Server

2. Start Detection Server

## On Exposed Host Machines
```sh=
sudo python3 -m pip install grpcio protobuf==4.21.12 scapy paramiko
```

if you have zookeeper on your host machines
```sh=
bin/zkCli.sh -timeout 3000 -server remoteIP:2181
```

2. Start up the Mitigation Client 
1. Start up the Detection Client and let it warm up for a few minutes


---

THIS SECTION IS DEPRECATED!!!
### Installation
```sh=
sudo apt-get install openvswitch-switch-dpdk
```

### Setup switches
```sh=
sudo ovs-vsctl add-br <bridge-name>
```
```sh=
sudo ip addr add <ens3-ip>/24 dev <bridge-name>
sudo ip link set <bridge-name> up
```

```sh=
sudo ovs-ofctl add-flow <bridge-name> "priority=0, actions=controller"
```

### Connect to ryu applications
```sh=
sudo ovs-vsctl set-controller <bridge-name> tcp:192.168.2.209:6653
```

---
## Services

### Start Detection Server
```sh=
python3 detection_server.py
```
### Ryu Application
```
cd services
ryu-manager controller.py --ofp-tcp-listen-port=6653
```

---
## Ransomware Test

### Start C2 server
```sh=
python3 server.py
```
### Run encryptor application on infected node

```
```
Ensure path to file target paths is correct.
python3 encryptor.py
```
```
