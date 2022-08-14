import time
from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from wxcloudrun import tools
import re,requests,sys,json,jsonpath

# 创建工具变量
User_Agent = tools.User_Agent

@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


@app.route ( '/movie' )
def movie():
    # print ( request.args )
    user_url = request.args.get ( 'user_url' )  # 返回一个list
    print ( '接收到的原始链接为：', user_url )
    # 判断获取的值是否为空，不为流程继续
    if not user_url:
        return '录入链接为空，请检查！'
        sys.exit ()

    # 1、requests模块之封装请求头信息
    # 1.1 封装headers信息，UA伪装
    headers = {
        'User-Agent': User_Agent['IOS']
    }
    # 1.2 封装URL信息
    # 1.3
    URL = re.findall ( r'https://v.douyin.com/(\w+)', user_url )[0]
    min_url = 'https://v.douyin.com/' + URL
    print ( '解析后链接：', min_url )
    # 1.4 发送URL请求
    # allow_redirects：是否允许重定向；False,禁止重定向
    respones = requests.get ( url=min_url, headers=headers, allow_redirects=False )
    # print('获取的重定向：',respones.is_redirect)
    # print('请求的URL为：', respones.url)
    print ( '服务器返回：', respones.status_code )

    # 2、respones模块处理
    # 2.1 获取响应头中重定向地址
    Http_respones_location = respones.headers['location']
    # print(video_id)

    # 2.2 正则表达式进行提取关键字段
    # re.findall 函数
    video_id = re.findall ( r'video/(\d+)', Http_respones_location )[0]
    print ( '截取到初步video：', video_id )
    URL_Https = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids='
    URL_end = '&reflow_source=reflow_page'
    URL_sum = URL_Https + video_id + URL_end
    print ( '第一步URL为：' + URL_sum )

    # 2.3 发送最终URL
    print ( '开始发送请求' )
    response = requests.get ( url=URL_sum, headers=headers )
    if response.status_code == 200:
        print ( '发送成功！' )
    else:
        print ( '发送失败！' )
        sys.exit ()

    # 2.4 jsonpath提取关键链接
    dict_data = json.loads ( response.content )

    max_URL = jsonpath.jsonpath ( dict_data, '$...play_addr.url_list.[0]' )[0]
    print ( '有水印URL为：', max_URL )
    # 2.5 替换关键字段值
    ret = re.sub ( r'playwm', "play", max_URL )
    print ( '无水印URL为：', ret )

    # 2.4 发送请求
    print ( '开始下载视频' )
    # 发送请求，获取响应内容
    response = requests.get ( url=ret, headers=headers )
    # 将响应内容存储存为变量
    vodeo = response.content
    if  vodeo:
        print('下载成功！')
    else:
        print("下载失败！")
    # 3、持久化保存，可保存本地 OR 数据库
    # 设置保存文件路径及变量名
    # # 设置时间戳
    timec = int ( time.time () )
    fileName = 'static/movie/' + str ( timec ) + '.mp4'

    # 进行IO操作，进行W类型，保存文件位置及保存文件的编码格式
    with open ( fileName, 'wb' ) as fp:
        fp.write ( vodeo )

    # 打印文件信息
    print ( '视频保存成功！路径为', fileName )
    return render_template ( 'index.html', movie=fileName )

    # 3、持久化保存，保存成文件 or 写入数据库
    # respones_max_JSON = response.json()
    # print(respones_max_JSON)
    # # print('开始保存响应的JSON文件')
    # print('JSON文件保存成功！文件地址为', '文件名称为：')


@app.route ( '/test' )
def test():  # put application's code here
    # return 'Hello World!'
    movies = 'static/movie/test.mp4'
    return render_template ( 'index.html', movie=movies )
