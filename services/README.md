generate the python code from .proto
```sh=
python3 -m grpc_tools.protoc -I protos --python_out=. --pyi_out=. --grpc_python_out=. protos/detection.proto
```
