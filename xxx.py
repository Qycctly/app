import requests
from lxml import etree
import time
import random
import json
import os
import base64
# from PIL import Image

key="e12109a5c17b18292ed1a570bb75ac1a"
push='https://qmsg.zendee.cn/send/'+key


#需要更改的有USER，54行api后面替代ak和sk的部分，ak用apikey替换，sk用serectkey替换，还有fixdata里的内容，push
USER=['311809000211','12345xyz','杨斌','13937861913','河南省开封市杞县']#此处从左至右写你的账号，密码，监护人，监护人联系电话，户籍地，注意顺序不要错

URL_MAP = {
    'HOST': 'https://ehall.hpu.edu.cn/infoplus/form/XSMRJKSB/start',
    'START': 'https://ehall.hpu.edu.cn/infoplus/interface/start',
    'ALIVE': 'https://ehall.hpu.edu.cn/infoplus/alive',
    'CAPTCHA': 'https://uia.hpu.edu.cn/sso/apis/v2/open/captcha?date=',
    'LOGIN': 'https://uia.hpu.edu.cn/cas/login',
    'RENDER': 'https://ehall.hpu.edu.cn/infoplus/interface/render',
    'PROCESS': 'https://ehall.hpu.edu.cn/infoplus/interface/instance/[id]/progress',
    'NEXTSTEP': 'https://ehall.hpu.edu.cn/infoplus/interface/listNextStepsUsers',
    'DOACTION': 'https://ehall.hpu.edu.cn/infoplus/interface/doAction',
    'CHECK': 'https://ehall.hpu.edu.cn/taskcenter/api/me/processes/done?limit=1&start=0',
    'API': 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=[ak]&client_secret=[sk]',
    'REQUEST_URL': 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
}
headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
session=requests.session()
####请求登录页面
login_page=session.get(url=URL_MAP['HOST'],headers=headers)
print(login_page.status_code)
if login_page.status_code!=200:
    print('打卡失败，网络状态为'+str(login_page.status_code))
    msg='打卡失败，网络状态为'+str(login_page.status_code)
    MSG={
    "msg":msg
}
    requests.post(url=push,data=MSG)

# print(login_page.text)
# print(login_page.url)
tree=etree.HTML(login_page.text)
lt=tree.xpath('//input[@name="lt"]/@value')[0]
# print(lt)
#####验证码
for i in range(0,3):
    captcha = URL_MAP['CAPTCHA'] + str(int(round(time.time() * 1000)))
    req = session.get(captcha, headers=headers)
    # print(req.text)
    # img = ast.literal_eval(req.content.decode('utf-8'))['img']
    sss =req.json()['img']
    imagedata = base64.b64decode(sss)
    # with open('code.jpg','wb') as fp:
    #     fp.write(imagedata)
    # img=Image.open('code.jpg')
    # img.show()
    # time.sleep(15)

    # 二进制方式打开图片文件
    ####验证码识别
    # f = open('code.jpg', 'rb')
    # img = base64.b64encode(f.read())
    img = base64.b64encode(imagedata)
    # f.close()
    api = URL_MAP['API'].replace('[ak]', 'w0qYhkXXNftSera1vgoD0foE').replace('[sk]', '0XkODbGMO7C9G2Zo99nBV9Dx0Oa51zId')
    response = requests.get(api)
    # print(response.text)

    ## 验证码
    access_token = response.json()['access_token']
    request_url = URL_MAP['REQUEST_URL'] + "?access_token=" + access_token
    api_headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data={'image':img}, headers=api_headers)
    # print(response.text)
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    captcha = response.json()['words_result'][0]['words']
    # print(captcha)
    captcha = str(captcha.replace('=?', '')).split('+')
    # print(captcha)
    # captcha = sum(map(int, captcha))
    number=['0','1','2','3','4','5','6','7','8','9']
    if captcha[0] in number and captcha[1] in number:
        captcha=eval(captcha[0]+'+'+captcha[1])
        # print(captcha)
        a='验证码识别成功,为'+str(captcha)
        print(a)
        break

# time.sleep(20)
#登录
data={
        'username': USER[0],
        'password': USER[1],
        'captcha': captcha,
        'token': req.json()['token'],
        '_eventId': 'submit',
        'lt': lt,
        'source': 'cas',
        'execution': 'e1s1',
    }
# print(URL_MAP['HOST'])
page=session.post(URL_MAP['LOGIN'],data=data,headers=headers)
# print(page.url)
# print(page.text)
# 检测登录状态
url = session.get(URL_MAP['HOST'], headers=headers).url
# print(url)
if not url == URL_MAP['HOST']:
    print('登录失败,请重试或手动打卡！')
    b='登录失败,请重试或手动打卡!'
    msg=b
    MSG={
        "msg":msg
    }
    requests.post(url=push,data=MSG)

else:
    print('使用账号密码登录成功!')
    b='使用账号密码登录成功!'

#获取表单
csrf=etree.HTML(page.text)
csrf=csrf.xpath('//meta[@itemscope="csrfToken"]/@content')[0]
# print(csrf)
formdata={
    'idc':'XSMRJKSB',
    'release':'',
    'csrfToken':csrf,
    'formData':'{"_VAR_URL":"https://ehall.hpu.edu.cn/infoplus/form/XSMRJKSB/start","_VAR_URL_Attr":"{}"}'
}
form=session.post(URL_MAP['START'],data=formdata,headers=headers)
print(form.url)
url=form.json()['entities'][0]
# print(url)
 # 构造表单

stepid=url.split('/')[-2]
# print(stepid)
formdata = {
    'stepId': stepid,
    'instanceId': '',
    'admin': 'false',
    'rand': random.random() * 999,
    'width': '1747',
    'lang': 'zh',
    'csrfToken': csrf
}
headers.update({'Referer': url})
req = session.post(URL_MAP['RENDER'], headers=headers, data=formdata)
c='已加载审批表!'
print(c)
form = req.json()['entities'][0]

 # 构造表单
instanceid = form['step']['instanceId']
formdata = {
    'stepId': stepid,
    'includingTop': 'true',
    'csrfToken': csrf,
    'lang': 'zh'
}
req = session.post(URL_MAP['PROCESS'].replace('[id]', instanceid), headers=headers, data=formdata)
d='审批表处理中...'
print(d)
timestamp = req.json()['entities'][0]['remarks'][0]['assignTime']
boundfields = ','.join(list(form['data'].keys()))
# print(timestamp)
# print(boundfields)
# 构造表单
postdata = form['data']
# print(postdata)
fixdata = {
    'fieldSQjhr':USER[2],                          #监护人
    'fieldSQjhrlxdh': USER[3],               #监护人联系电话
    'fieldSQhjd': USER[4],                       #户籍地
    'fieldTXxjzdlx': '1',                           #现居住地类型
    'fieldTXsfqgyq': '未去过重点疫区',                #是否去过重点疫区
    'fieldTXsfqgyq_Name': '未去过重点疫区',
    'fieldTXsfjc': '2',                             #是否接触
    'fieldTXcjtw': '35-36.5',                       #体温
    'fieldTXcjtw_Name': '35-36.5',
    'fieldTXsfyc': '2',                             #健康状态是否异常
    'fieldTXsfjcqk': '',
    'fieldTXsfjcqk_Name': '',
    'fieldTXzz': '',
    'fieldTXzz_Name': '',
    'fieldTXzz1': '',
    'fieldTXycjg': '',
    'fieldTXycjg_Name': '',
    'fieldTXycjgqt': '',
    'fieldTXzlcs': '',
    'fieldAN':'获取位置信息',
    'fieldDWAN': '河南省焦作市解放区人民路',
    'fieldGRDW': '113.23563548681861,35.215611703666454,17',
    'fieldGRDW_Name': '自动获取',
}
postdata.update(fixdata)
# print(postdata)
fixdata={
    "fieldTXsf": "410000",
    "fieldTXsf_Name": "河南省",
	"fieldTXcs": "410800",
	"fieldTXcs_Name": "焦作市",
	"fieldTXcs_Attr": "{\"_parent\":\"410000\"}",
	"fieldTXdq": "410811",
	"fieldTXdq_Name": "山阳区",
	"fieldTXdq_Attr": "{\"_parent\":\"410800\"}",
	"fieldTXjtwz": "河南理工大学",
    # "_VAR_ENTRY_NAME": "学生每日健康上报(_计算机科学与技术学院（软件职业技术学院）)",
	# "_VAR_ENTRY_TAGS": "健康状况上报,信管中心,移动端"
 }
postdata.update(fixdata)
print(postdata)
formdata = {
            'stepId': stepid,
            'actionId': 1,
            'formData': str(postdata),
            'timestamp': timestamp,
            'rand': random.random() * 999,
            'boundFields': boundfields,
            'csrfToken': csrf,
            'lang': 'zh'
        }
req = session.post(URL_MAP['NEXTSTEP'], headers=headers, data=formdata)
# print(req.text)
if req.json()['ecode'] == 'SUCCEED':
    print('健康打卡准备阶段, 成功!')
    e='健康打卡准备阶段, 成功!'
else:
    print('健康打卡准备阶段, 失败!')
    e='健康打卡准备阶段, 失败!'

# print(postdata)

formdata = {
        'actionId': 1,
        'formData': str(form['data']),
        'remark': '',
        'rand': random.random() * 999,
        'nextUsers': '{}',
        'stepId': stepid,
        'timestamp': timestamp,
        'boundFields': boundfields,
        'csrfToken': csrf,
        'lang': 'zh'
    }
req = session.post(URL_MAP['DOACTION'], headers=headers, data=formdata)
# print(req.text)
if req.json()['ecode'] == 'SUCCEED':
    print('健康打卡填报阶段, 成功!')
    f='健康打卡填报阶段, 成功!'
else:
    print('健康打卡填报阶段, 失败!')
    f='健康打卡填报阶段, 失败!'

#复查

req = session.get(URL_MAP['CHECK'], headers=headers)
# print(req.text)
last_time = req.json()['entities'][0]['update']
local_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(last_time))
update = round(time.time()) - last_time
if update > 5:
    print('上次打卡完成于%ss前,打卡可能未成功!', update)
    print('打卡复检状态异常!')
    g='打卡可能未成功!请去"https://ehall.hpu.edu.cn/taskcenter/workflow/done"查看',
else:
    print('打卡完成于%s', local_time)

    g='打卡成功，完成于'+local_time

s=g+'\n'+a+'\n'+b+'\n'+c+'\n'+d+'\n'+e+'\n'+f



msg=s
MSG={
    "msg":msg
}
requests.post(url=push,data=MSG)


