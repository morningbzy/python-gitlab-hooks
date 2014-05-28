gitlab hooks written in python

support for part of Asana


depend Python2.7

no licenes!

####how to run it

    gunicron -w 1 -b 127.0.0.1:8891 ./server.py

>
    说明： gitlab的hook分为web hook和system hook两种，这里只针对web hook。
    gitlab向配置的web hook的url发送http消息，为了实现hook的功能就必须要实现一个简单的服务，
    接收后格式化再重新处理，可以转发到其它服务或执行预设脚本


####FAQ

1. gitlab上的测试hook可以成功，正式适用却不行？

    测试是直接发送hook请求，正式环境下使用sidekiq消息服务发送请求，
    可能是sidekiq服务运行失败导致，查看sidekiq.log

2. 为什么一定要部署一个服务

    gitlab的web hook只能向配置好的url发送固定格式的请求，与要接受消息的服务不兼容，
    因此需要一个中间服务    
