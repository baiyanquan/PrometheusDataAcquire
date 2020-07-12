FROM python:3


WORKDIR /root/PrometheusDataAcquire

RUN git clone https://gitee.com/baiyanquan/PrometheusDataAcquire.git /root/PrometheusDataAcquire \
    && pip install --upgrade pip \
    && pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && pip install flask_cors -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && mkdir /root/data\
    && cd /root/data\
    && git config --global user.name "baiyanquan"\
    && git config --global user.password "hyq19980329"\
    && git config user.email '405579949@qq.com'\
    && git init\
    && git remote add origin https://gitee.com/baiyanquan/SockShopPerformanceData-ChaosbladeExperimentOnKubernetes.git\
    && git pull origin master

CMD ["python", "/root/PrometheusDataAcquire/PerformanceDataPicker.py"]