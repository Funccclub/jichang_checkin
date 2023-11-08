import os
import json
import requests
os.environ['URL'] = "https://1.cutecloud.net"
os.environ['EMAIL'] = "210648986@qq.com"
os.environ['PASSWD'] = "plmnko..."
os.environ['TOKEN'] = "b32da7f1b264429fb0c94e2c87329c32"

def send_pushplus_msg(content, token):
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": "签到结果",
        "content": content
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=body, headers=headers)
    return response.json()

def main():
    session = requests.Session()
    login_url = os.environ.get('URL') + "/auth/login"
    check_url = os.environ.get('URL') + "/user/checkin"
    email = os.environ.get('EMAIL')
    passwd = os.environ.get('PASSWD')
    token = os.environ.get('TOKEN')
    data = {
        "email": email,
        "passwd": passwd
    }
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        print('进行登录...')
        login_response = session.post(url=login_url, headers=header, data=data)
        print("Login response status code:", login_response.status_code)
        print("Login response body:", login_response.text)
        response = json.loads(login_response.text)
        print(response['msg'])
        # 进行签到
        result = json.loads(session.post(url=check_url, headers=header).text)
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

if __name__ == "__main__":
    main()
print("URL:", os.environ.get('URL'))
print("EMAIL:", os.environ.get('EMAIL'))
print("PASSWD:", os.environ.get('PASSWD'))
print("TOKEN:", os.environ.get('TOKEN'))
