import requests, json, os

def send_wechat_msg(content, corpid, corpsecret, agentid):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(corpid, corpsecret)
    r = requests.get(url)
    access_token = r.json()['access_token']
    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(access_token)
    headers = {'content-type': 'application/json'}
    data = {
        "touser": "@all",  # 发送给所有人
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": content
        },
        "safe": 0
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    return r.json()

session = requests.session()
# 机场的地址
url = os.environ.get('URL')
# 配置用户名（一般是邮箱）
email = os.environ.get('EMAIL')
# 配置用户名对应的密码 和上面的email对应上
passwd = os.environ.get('PASSWD')
# 企业微信的配置
corpid = os.environ.get('CORPID')  # CorpID是企业号的标识
corpsecret = os.environ.get('CORPSECRET')  # CorpSecret可在企业微信管理端-我的企业-企业信息查看
agentid = os.environ.get('AGENTID')  # AgentId可在企业微信管理端-应用与小程序-应用查看

login_url = '{}/auth/login'.format(url)
check_url = '{}/user/checkin'.format(url)

header = {
        'origin': url,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
data = {
        'email': email,
        'passwd': passwd
}

try:
    print('进行登录...')
    response = json.loads(session.post(url=login_url,headers=header,data=data).text)
    print(response['msg'])
    # 进行签到
    result = json.loads(session.post(url=check_url,headers=header).text)
    print(result['msg'])
    content = result['msg']
    # 进行推送
    if corpid and corpsecret and agentid:
        send_wechat_msg(content, corpid, corpsecret, agentid)
        print('推送成功')
except Exception as e:
    content = '签到失败: ' + str(e)
    print(content)
    if corpid and corpsecret and agentid:
        send_wechat_msg(content, corpid, corpsecret, agentid)
