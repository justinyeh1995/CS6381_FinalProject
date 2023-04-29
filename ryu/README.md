## Install Ryu
```sh=
git clone https://github.com/faucetsdn/ryu.git
cd ryu 
pip3 install .
```
## Run Controller
```sh=
ryu-manager controller.py
```

## Connect the host machines to a ryu controller running on another machine
```sh=
sudo ovs-vsctl set-controller <bridge-name> tcp:<ryu-controller-ip>:<ryu-controller-port>
```
### Say we are running the controller on masternode1, then
```sh=
sudo ovs-vsctl set-controller <bridge-name> tcp:129.114.25.220:6653
```

