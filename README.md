# CS6381 FinalProject

## On Exposed Host Machines
### Setup switches
```sh=
ovs-ofctl add-br <bridge-name>
```

```sh=
sudo ovs-ofctl add-flow <bridge-name> "priority=0, actions=controller"
```

```sh=
sudo ovs-vsctl add-port <bridge> <port>
```

```sh=
ovs-ofctl set-controller <bridge-name> "priority=0, actions=controller"
```

### connect to ryu applications
```sh=
sudo ovs-vsctl set-controller <bridge-name> tcp:129.114.25.220:6653
```

---

## Ryu Application
```
cd services
ryu-manager controller.py --ofp-tcp-listen-port=6653
```
