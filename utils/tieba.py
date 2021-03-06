# -*- coding: utf-8 -*-
'''''#百度错误代码:
err_code:40  请输入验证码完成发帖
'''
import re
import json
from urllib import request, parse
from http import cookiejar


def sign():
    sign_url = 'http://tieba.baidu.com/sign/add'
    print('正在尝试签到')
    tbs = get_tbs()
    print('获取喜欢的贴吧ing...')
    like_tieba = 'http://tieba.baidu.com/f/like/mylike'
    req = request.Request(like_tieba)
    resp = request.urlopen(req).read()
    re_like_tieba = '<a href="\/f\?kw=.*?" title=".*">(.*?)<\/a>'
    find_like_tieba = re.findall(re_like_tieba, resp)
    print('我喜欢的贴吧:')

    for mylike_tieba in find_like_tieba:
        print(mylike_tieba)

        # 构造签到数据头:
        sign_request = {'ie': 'utf-8', 'kw': mylike_tieba, 'tbs': tbs}
        sign_request = request.Request(sign_url, headers=sign_request)
        sign_resp = sign_request.data
        sign_resp = json.load(sign_resp)
        print(sign_resp)
        if sign_resp['error'] == '':
            user_sign_rank = int(sign_resp['data']['uinfo']['user_sign_rank'])  # 第几个签到
            cont_sign_num = int(sign_resp['data']['uinfo']['cont_sign_num'])  # 连续签到
            cout_total_sing_num = int(sign_resp['data']['uinfo']['cout_total_sing_num'])  # 累计签到
            print("签到成功,第%d个签到,连续签到%d天,累计签到%d天" % (user_sign_rank, cont_sign_num, cout_total_sing_num))
        else:  # 签到失败处理
            if not sign_resp['error'] == u'亲，你之前已经签过了':
                find_like_tieba.append(mylike_tieba)
                print('wtf')


def get_tbs():
    tbs_url = 'http://tieba.baidu.com/dc/common/tbs'
    req = request.Request(tbs_url)
    tbs_resp = request.urlopen(req).read()
    print(tbs_resp)
    tbs = re.search('"tbs":"(?P<tbs>.*?)"', tbs_resp).group('tbs')
    print('tbs:', tbs)
    return tbs


def checkAllCookiesExist(cookieNameList, cookieJar):
    cookiesDict = {}
    for eachCookieName in cookieNameList:
        cookiesDict[eachCookieName] = False

    allCookieFound = True
    for cookie in cookieJar:
        if (cookie.name in cookiesDict):
            cookiesDict[cookie.name] = True

    for eachCookie in cookiesDict.keys():
        if (not cookiesDict[eachCookie]):
            allCookieFound = False
            break

    return allCookieFound


def baidu(username, password):  # 尝试登录百度
    login_path = 'https://passport.baidu.com/v2/api/?login'
    try:
        cj = cookiejar.CookieJar()
        opener = request.build_opener(request.HTTPCookieProcessor(cj))
        headers = [('User-agent',
                    'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31')]
        getapiUrl = "https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true"
        req = request.Request(getapiUrl, headers=headers)
        getapiRespHtml = opener.open(req).read()
        foundTokenVal = re.search("bdPass\.api\.params\.login_token='(?P<tokenVal>\w+)'", getapiRespHtml)
        if (foundTokenVal):
            tokenVal = foundTokenVal.group("tokenVal")
            print("tokenVal=", tokenVal)
        else:
            print('foundTokenVal is null')
            return

        post_dic = {
            'staticpage': 'http://www.baidu.com/cache/user/html/v3Jump.html',
            'charset': 'UTF-8',
            'token': tokenVal,
            'tpl': 'mn',
            'apiver': 'v3',
            # 'tt':,
            # 'codestring':,
            'isPhone': 'false',
            'safeflg': 0,
            'u': 'http://www.baidu.com/',
            'quick_user': 0,
            # 'usernamelogin':1,
            'splogin': 'rate',
            'username': username,
            'password': password,
            # 'verifycode':'',
            'mem_pass': 'on',
            # 'ppui_logintime':14791
            'callback': 'parent.bd__pcbs__c5crjq',
        }
        postdata = parse.urlencode(post_dic)
        req = request.Request(login_path, postdata)
        resp = request.urlopen(req).read()

        # data=urllib2.urlopen(test_url).read()
        cookiesToCheck = ['BDUSS', 'PTOKEN', 'STOKEN', 'SAVEUSERID']
        loginBaiduOK = checkAllCookiesExist(cookiesToCheck, cj)
        if (loginBaiduOK):
            print("+++ Emulate login baidu is OK, ^_^")
            print('ok')
        else:
            print("--- Failed to emulate login baidu !")
            print('failed')
        sign()
        print('尝试结束，看疗效...')
    except Exception as e:
        print(str(e))


# 我喜欢的贴吧
# http://tieba.baidu.com/f/like/mylike?
# re:<a href="\/f\?kw=.*?" title=".*">.*?<\/a>
user = 'youremail'
password = 'yourpassword'
baidu(user, password)
