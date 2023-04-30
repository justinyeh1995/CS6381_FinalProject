# CS6381 FinalProject

## On Exposed Host Machines

### Installation
```sh=
sudo apt-get install openvswitch-switch-dpdk
```

### Setup switches
```sh=
ovs-vsctl add-br <bridge-name>
```

```sh=
sudo ovs-vsctl add-port <bridge> ens3
```

```sh=
sudo ovs-vsctl add-flow <bridge-name> "priority=0, actions=controller"
```

### Connect to ryu applications
```sh=
sudo ovs-vsctl set-controller <bridge-name> tcp:129.114.25.220:6653
```

---

## Ryu Application
```
cd services
ryu-manager controller.py --ofp-tcp-listen-port=6653
```
