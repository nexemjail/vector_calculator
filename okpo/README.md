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
