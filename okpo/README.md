```
cd okpo
docker build -t okpo/lab .
docker run -p 5000:5000 okpo/lab:latest
```


```
curl -X POST 127.0.0.1:5000\
    -d '{"v1":1, "v2":2}'\
     -H "Content-Type: application/json"
```

Install minicube and cubectl
https://kubernetes.io/docs/tasks/tools/install-minikube/
https://kubernetes.io/docs/tasks/tools/install-kubectl/


https://kubernetes.io/docs/setup/minikube/
To install images that are build locally use this tutorial
https://github.com/kubernetes/minikube/blob/0c616a6b42b28a1aab8397f5a9061f8ebbd9f3d9/README.md#reusing-the-docker-daemon

