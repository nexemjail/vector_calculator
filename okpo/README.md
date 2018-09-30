Install docker, minicube and kubectl via tutorial here:

https://kubernetes.io/docs/tasks/tools/install-minikube/


```
cd okpo
minicube start
eval $(minikube docker-env)
docker build . -t okpo-lab
kubectl apply -f deployment.yaml
kubectl apply -f hpa.yaml
kubectl expose deployment okpo-lab --type=LoadBalancer --name=okpo-lab --port=5000 --target-port=5000
```

See the port exposed via the command 
```kubectl get service```
To test scaling run 
```
MOLOTOV_PORT=(this-exposed-port) molotov test.py -p 1 -w 40 -d 500
```

To delete all the stuff run 
```
kubectl delete deployment okpo-lab
kubectl delete service okpo-lab
```

To stop minikube run
```
minikube stop
```

<!-- kubectl run okpo-lab --image=okpo-lab --port=5000 --image-pull-policy=Never  -->

<!-- --horizontal-pod-autoscaler-use-rest-clients=false -->
<!-- kubectl delete deployment okpo-lab -->

<!-- kubectl expose deployment okpo-lab --type=LoadBalancer -->


https://kubernetes.io/docs/tasks/administer-cluster/dns-horizontal-autoscaling/

Install minicube and cubectl
https://kubernetes.io/docs/tasks/tools/install-minikube/
https://kubernetes.io/docs/tasks/tools/install-kubectl/


https://kubernetes.io/docs/setup/minikube/
To install images that are build locally use this tutorial
https://github.com/kubernetes/minikube/blob/0c616a6b42b28a1aab8397f5a9061f8ebbd9f3d9/README.md#reusing-the-docker-daemon

