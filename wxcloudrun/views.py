import hashlib
import json
import re
import sys

import jsonpath
import requests
from flask import render_template, request, jsonify

from run import app
from wxcloudrun import tools

# 创建工具变量
User_Agent = tools.User_Agent
login_errcode = tools.login_errcode
login_errmsg = tools.login_errmsg


@app.route ( '/' )
def index():
    """
    :return: 返回index页面
    """
    return render_template ( 'index.html' )


@app.route ( '/movie', methods=['POST'] )
def movie():
    user_url = request.data
    user_url = request.json['user_url']
    # user_url = request.args.get ( 'user_url' )  # 返回一个list
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
    # print ( '服务器返回：', respones.status_code )

    # 2、respones模块处理
    # 2.1 获取响应头中重定向地址
    Http_respones_location = respones.headers['location']
    # print(video_id)

    # 2.2 正则表达式进行提取关键字段
    # re.findall 函数
    video_id = re.findall ( r'video/(\d+)', Http_respones_location )[0]
    # print ( '截取到初步video：', video_id )
    URL_Https = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids='
    URL_end = '&reflow_source=reflow_page'
    URL_sum = URL_Https + video_id + URL_end
    print ( '第一步URL为：' + URL_sum )

    # 2.3 发送最终URL
    # print ( '开始发送请求' )
    response = requests.get ( url=URL_sum, headers=headers )
    if response.status_code == 200:
        print ( '响应成功！' )
    else:
        print ( '响应失败！' )
        sys.exit ()

    # 2.4 jsonpath提取关键链接
    dict_data = json.loads ( response.content )
    max_URL = jsonpath.jsonpath ( dict_data, '$...play_addr.url_list.[0]' )[0]
    # print ( '有水印URL为：', max_URL )
    video_title = jsonpath.jsonpath ( dict_data, '$..share_title' )[0]
    print ( "视频标题为：", video_title )
    video_id = jsonpath.jsonpath ( dict_data, '$..play_addr.uri' )[0]
    print ( "视频ID为：", video_id )
    video_ratio = jsonpath.jsonpath ( dict_data, '$..video.ratio' )[0]
    print ( "视频清晰度为：", video_ratio )
    nickname = jsonpath.jsonpath ( dict_data, '$..author.nickname' )[0]
    print ( "视频作者为：", nickname )
    url_list_png = jsonpath.jsonpath ( dict_data, '$..avatar_larger.url_list[0]' )[0]
    print ( "作者头像为：", url_list_png )
    url_list_cover = jsonpath.jsonpath ( dict_data, '$..cover.url_list[0]' )[0]
    print ( "视频封面为：", url_list_cover )
    # 2.5 替换关键字段值
    ret = re.sub ( r'playwm', "play", max_URL )
    print ( '无水印URL为：', ret )

    # 2.4 发送请求
    # print ( '开始下载视频' )
    # 发送请求，获取响应内容
    respones = requests.get ( url=ret, headers=headers, allow_redirects=False )
    respones_text = respones.text

    # 提取字段
    pattern = r"https://.*?80000"
    Match = re.search ( pattern=pattern, string=respones_text )
    Download_link = Match.group ()
    print ( "最终下载链接为：", Download_link )

    data = {
        "Download_link": Download_link,  # 最终下载链接
        "code": "0",
        "video_title": video_title,  # 视频标题
        "video_id": video_id,  # 视频ID为
        "video_ratio": video_ratio,  # 视频清晰度
        "ret": ret,  # 无水印链接
        "nickname": nickname,  # 视频作者
        "url_list_png": url_list_png,  # 作者头像
        "url_list_cover": url_list_cover,  # 视频封面
    }
    video = {
        "movie": ret,
        "aa": 0,
        "video_title": video_title,
        "nickname": nickname,
        "url_list_png": url_list_png,
        "url_list_cover": url_list_cover
    }

    # jsonify帮助转为json数据，并设置响应头 Content-Type 为 application/json
    return jsonify ( data )
    # return render_template ( 'video.html', video=video )

    # 3、持久化保存，保存成文件 or 写入数据库
    # respones_max_JSON = response.json()
    # print(respones_max_JSON)
    # # print('开始保存响应的JSON文件')
    # print('JSON文件保存成功！文件地址为', '文件名称为：')


@app.route ( '/api/test', methods=['GET'] )
def test():  # put application's code here
    # return 'Hello World!'
    movies = 'static/movie/test.mp4'
    return render_template ( 'index.html', movie=movies )


@app.route ( '/api/wx/login', methods=['POST'] )
def login():
    # print ( "进入登录方法" )

    request_host = request.host
    js_code = request.json['js_code']
    # print ( '获取到的请求IP为：：' + request_host )
    # print ( '获取到的js_code为：' + js_code )
    # 持久化
    ###########

    # 返回json数据的方法
    openid = hashlib.md5 ()
    openid.update ( str ( js_code ).encode ( 'utf-8' ) )
    openid_md5 = str ( openid.hexdigest () )
    print ( '加密后的openid为：' + str ( openid_md5 ) )

    # if 判断 数持久化成功 返回成功。
    errcode = login_errcode['ok']
    errmsg = login_errmsg['ok']
    data = {
        "openId": openid_md5,
        "errcode": errcode,
        "errmsg": errmsg
    }

    # jsonify帮助转为json数据，并设置响应头 Content-Type 为 application/json
    return jsonify ( data )
