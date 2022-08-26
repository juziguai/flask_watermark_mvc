# wxcloudrun-flask
[![GitHub license](https://img.shields.io/github/license/WeixinCloud/wxcloudrun-express)](https://github.com/WeixinCloud/wxcloudrun-express)
![GitHub package.json dependency version (prod)](https://img.shields.io/badge/python-3.7.3-green)

微信云托管 python Flask 框架模版

## 快速开始
前往 [微信云托管快速开始页面](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/basic/guide.html)，选择相应语言的模板，根据引导完成部署。


## 目录结构说明

~~~
.
├── Dockerfile dockerfile       dockerfile
├── README.md README.md         README.md文件
├── container.config.json       模板部署「服务设置」初始化配置（二开请忽略）
├── requirements.txt            依赖包文件
├── config.py                   项目的总配置文件  里面包含数据库 web应用 日志等各种配置
├── run.py                      flask项目管理文件 与项目进行交互的命令行工具集的入口
└── wxcloudrun                  app目录
    ├── static                  静态资源
    ├── templates               html模板
    ├── __init__.py             python项目必带  模块化思想
    ├── dao.py                  数据库访问模块
    ├── model.py                数据库对应的模型
    ├── response.py             响应结构构造
    ├── templates               模版目录,包含主页index.html文件
    └── views.py                执行响应的代码所在模块  代码逻辑处理主要地点  项目大部分代码在此编写
~~~



## 服务 API 文档

### `GET /api/movie`

解析链接

#### 请求参数

user_url

#### 响应结果

- `movie_id`：视频id
- `movie_code`：响应码

##### 响应结果示例

```json
{
  "movie_id": "1660664469.mp4",
  "movie_code": "0"
}
```

#### 调用示例

```
curl https://<云托管服务域名>/api/movie
```


## 使用注意
如果不是通过微信云托管控制台部署模板代码，而是自行复制/下载模板代码后，手动新建一个服务并部署，需要在「服务设置」中补全以下环境变量，才可正常使用，否则会引发无法连接数据库，进而导致部署失败。
- MYSQL_ADDRESS
- MYSQL_PASSWORD
- MYSQL_USERNAME
以上三个变量的值请按实际情况填写。如果使用云托管内MySQL，可以在控制台MySQL页面获取相关信息。



## License

[MIT](./LICENSE)
