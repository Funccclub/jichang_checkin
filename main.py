import requests, json, os
os.environ['URL'] = 'https://1.cutecloud.net/user'
def send_pushplus_msg(content, token):
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": "签到通知",
        "content": content,
        "template": "html"
    }
    r = requests.post(url, data)
    return r.json()

def test_network_connectivity():
    url = "http://www.pushplus.plus/send"
    try:
        response = requests.get(url)
        print(f"Network test result: {response.status_code}")
    except Exception as e:
        print(f"Network test failed: {e}")

# 先测试网络连通性
test_network_connectivity()

session = requests.session()
# 机场的地址
url = os.environ.get('URL')
# 配置用户名（一般是邮箱）
email = os.environ.get('EMAIL')
# 配置用户名对应的密码 和上面的email对应上
passwd = os.environ.get('PASSWD')
# PushPlus的配置
token = os.environ.get('TOKEN')  # Token在PushPlus官网获取

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
    if token:
        response = send_pushplus_msg(content, token)
        if response['code'] != 200:
            print('发送消息失败: {}'.format(response['msg']))
        else:
            print('推送成功')
except Exception as e:
    print(e)
    content = '签到失败'
    print(content)
    if token:
        response = send_pushplus_msg(content, token)
        if response['code'] != 200:
            print('发送消息失败: {}'.format(response['msg']))
