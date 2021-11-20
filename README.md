# 阿里云 云解析DNS动态更新

通过调用云解析DNS提供的接口，动态更新A记录到当前本地公网ip地址

## 注意事项

1.域名已经使用阿里云 云解析DNS <br/>
2.程序一旦执行完成将会立即更新所设置域名的A记录，测试程序请使用测试用域名 <br/>
3.程序我个人代码部分完全开源,可以作为商业用途。~~没人会用于商业用途的吧~~ 所调用的第三方包请参照相关许可 <br/>

## 配置文件
***

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
打开settings.json文件，并编辑内容
```json
   {
    "regionId": "cn-hangzhou",
    "accessKeyId": "",
    "accessSecret": "",
    "domain_name": "",
    "secondary_domain": "",
    "sleep_time": 10
    }
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
accessKeyId和accessSecret为阿里云生成，具体生成方法请自行研究或拨打95187询问阿里云客服<br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
domain_name为主域名，secondary_domain为子域名<br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
sleep_time 为解析记录刷新时间，为避免接口滥用，请不要设置过低数值<br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
networkTestAddr 用于测试网络是否连通 随便找个稳定的网站用于测试就行了<br>

## 运行
***

`docker run -v <your settings.json path>:/app/settings.json ghcr.io/arugal/aliyunddns/app:latest`


