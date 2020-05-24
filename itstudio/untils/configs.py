from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
import random
import time


# 随机code/sid生成函数
from django.http import HttpResponse


def get_code(type):
    all_char = '0123456789qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJIKOLPHRZIT'
    if type == 'code':
        code = ''
        for i in range(6):
            num = random.randint(0, 9)
            code += all_char[num]
        return code
    else:
        sid = str(time.time())[:10]
        for i in range(14):
            num = random.randint(0, 64)
            sid += all_char[num]
        return sid


# 发送邮件的函数
def send_mail(email, content):
    # 发件人邮箱账号
    my_sender = '1559492576@qq.com'
    # 发件人邮箱密码
    my_pass = "egrmsvwjxlbfbadd"
    # 收件人邮箱账号
    my_user = email
    # 括号里包括邮件主要内容、编码方式
    msg = MIMEText(content, 'plain', 'utf-8')
    # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['From'] = formataddr(["【爱特工作室】", my_sender])
    # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['To'] = formataddr(["亲爱的海大新生", my_user])
    # 邮件的主题，也可以说是标题
    msg['Subject'] = "【爱特工作室验证码】"
    # 发件人邮箱中的SMTP服务器，端口是465
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    # 括号中对应的是发件人邮箱账号、邮箱密码
    server.login(my_sender, my_pass)
    # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.sendmail(my_sender, [my_user, ], msg.as_string())
    server.quit()


content_yzm = '''
亲爱的用户：
    您好！
    欢迎您加入我们爱特工作室！
    一定保存好验证码，打死也不要告诉别人哦！
'''

content_jh = '''
亲爱的用户：
    您好！
    欢迎您加入我们爱特工作室！
    请点击激活链接前往激活页面激活用户！
'''

comment_ip_dict = {}
code_ip_dict = {}
#
ac_ip = ['111.15.74.105', '192.168.1.3', "223.80.203.45", "117.136.92.4", "111.32.65.210"]
b_ip = []


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip


def code_ip(request):
    ip = get_ip(request)
    now_time = time.time()
    if ip in code_ip_dict:
        end_time = code_ip_dict[str(ip)]
        if now_time - end_time >= 30:
            code_ip_dict[str(ip)] = now_time
            return 0
        else:
            wait_time = now_time - end_time
            return 30 - int(wait_time)
    else:
        code_ip_dict[str(ip)] = now_time
        return 0


def comment_ip(request):
    ip = get_ip(request)
    now_time = time.time()
    if ip in comment_ip_dict:
        end_time = comment_ip_dict[str(ip)]
        if now_time - end_time >= 30:
            comment_ip_dict[str(ip)] = now_time
            return 0
        else:
            wait_time = now_time - end_time
            return 30 - int(wait_time)
    else:
        comment_ip_dict[str(ip)] = now_time
        return 0


def ban(func):
    def wrapper(request, *args, **kwargs):
        ip = get_ip(request)
        if ip in b_ip:
            return HttpResponse('来自学弟的亲切问候：你的ip被ban了')
        else:
            if (request.session.get('ip') and request.session.get('ban')) or (ip in ac_ip):
                setattr(request, 'ip', ip)
                setattr(request, 'ban', 1)
                result = func(request, *args, **kwargs)
                return result
            else:
                b_ip.append(ip)
                return HttpResponse('来自学弟的亲切问候：你的ip被ban了')
    return wrapper
