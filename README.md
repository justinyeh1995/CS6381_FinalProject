# CS6381 FinalProject

## On Exposed Host Machines

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

## Ryu Application
```
cd services
ryu-manager controller.py --ofp-tcp-listen-port=6653
```
