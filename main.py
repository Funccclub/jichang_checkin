import os
import json
import requests

def send_wechat_msg(content, corpid, corpsecret, agentid):
    # 获取access_token
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(corpid, corpsecret)
    response = requests.get(url).json()
    access_token = response.get('access_token')

    # 发送消息
    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(access_token)
    data = {
        "touser" : "@all",
        "msgtype" : "text",
        "agentid" : agentid,
        "text" : {
            "content" : content
        },
        "safe" : 0
    }
    response = requests.post(url, data=json.dumps(data)).json()
    return response

def main():
    session = requests.Session()
    login_url = os.environ.get('URL') + "/auth/login"
    check_url = os.environ.get('URL') + "/user/checkin"
    email = os.environ.get('EMAIL')
    passwd = os.environ.get('PASSWD')
    corpid = os.environ.get('CORPID')
    corpsecret = os.environ.get('CORPSECRET')
    agentid = os.environ.get('AGENTID')
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
        if corpid and corpsecret and agentid:
            response = send_wechat_msg(content, corpid, corpsecret, agentid)
            if response['errcode'] != 0:
                print('发送消息失败: {}'.format(response['errmsg']))
            else:
                print('推送成功')
    except Exception as e:
        print(e)
        content = '签到失败'
        print(content)
        if corpid and corpsecret and agentid:
            response = send_wechat_msg(content, corpid, corpsecret, agentid)
            if response['errcode'] != 0:
                print('发送消息失败: {}'.format(response['errmsg']))

if __name__ == "__main__":
    main()
print("URL:", os.environ.get('URL'))
print("EMAIL:", os.environ.get('EMAIL'))
print("PASSWD:", os.environ.get('PASSWD'))
print("CORPID:", os.environ.get('CORPID'))
print("CORPSECRET:", os.environ.get('CORPSECRET'))
print("AGENTID:", os.environ.get('AGENTID'))
