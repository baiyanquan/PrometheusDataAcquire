FROM python:3


WORKDIR /root/PrometheusDataAcquire

RUN git clone https://github.com/baiyanquan/PrometheusDataAcquire.git /root/PrometheusDataAcquire \
    && pip install --upgrade pip \
    && pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && pip install flask_cors -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && mkdir /root/data\
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime\
    && echo 'Asia/Shanghai' >/etc/timezone

CMD ["python", "/root/PrometheusDataAcquire/SockPerformanceDataPicker.py"]