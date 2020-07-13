docker stop prometheus_data_acquire
docker rm prometheus_data_acquire
docker rmi prometheus_data_acquire:hyq

cd /home/serveradmin/hyq/dockerfile
docker build -f ./PrometheusDataAcquire -t prometheus_data_acquire:hyq .
docker run --name prometheus_data_acquire -v /home/serveradmin/hyq/data/PerformanceDataAcquire:/root/data --net host -d prometheus_data_acquire:hyq