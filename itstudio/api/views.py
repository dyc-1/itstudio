from untils.configs import get_code, send_mail, content_yzm, comment_ip, code_ip
from untils.configs import ban, b_ip, comment_ip_dict, code_ip_dict, get_ip
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from untils.output import get_data, get_all_data
from untils.returndata import dict_to_json
from django.utils.http import urlquote
from django.shortcuts import render
from api.models import *
import requests
import openpyxl
import time
import re


# Create your views here.

@ban
def code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            em = re.findall(r"^[a-z0-9]+[@][a-z0-9]+\.com|cn$", email)
            exist_email = Register.objects.filter(email=email)
            if not (em and em[0] == email):
                return dict_to_json(state='emailError', messages='邮箱不正确')
            elif exist_email:
                return dict_to_json(state='emailError', messages='邮箱已存在')
            else:
                wait_time = code_ip(request)
                # wait_time = 0
                if wait_time != 0:
                    return dict_to_json(state='timeError', messages=f'请等待{wait_time}秒后再试')
                code = get_code(type='code')
                request.session['email'] = email
                request.session['code'] = code
                try:
                    content = f'    {content_yzm}您的验证码为{code}'
                    send_mail(email, content)
                    return dict_to_json(state='success', messages='访问提交成功')
                except Exception:
                    return dict_to_json(state='sendError', messages='邮箱发送错误')
        else:
            return dict_to_json(state='emailError', messages='未提交邮箱')
    else:
        return dict_to_json(state='postError', messages='未提交POST')


@ban
def register(request):
    if request.method == 'POST':
        if all(data in request.POST for data in ("name", "email", "phone", "major", "departer", "code")):
            em = re.findall(r"^[a-z0-9]+[@][a-z0-9]+\.com|cn$", request.POST.get('email'))
            ph = re.findall(r"^1\d{10}$", request.POST.get('phone'))
            ma = re.findall(r"^20\d{2}级+.*", request.POST.get('major'))
            exist_email = Register.objects.filter(email=request.POST.get('email'))
            if exist_email:
                return dict_to_json(state='emailError', messages='邮箱已存在')
            elif len(request.POST.get('name')) > 16:
                return dict_to_json(state='nameError', messages='姓名格式不正确')
            elif not (em and em[0] == request.POST.get('email')):
                return dict_to_json(state='emailError', messages='邮箱格式不正确')
            elif not (request.session['email'] and request.session['code']):
                return dict_to_json(state='codeError', messages='未发送验证码')
            elif not (ph and ph[0] == request.POST.get('phone')):
                return dict_to_json(state='phoneError', messages='手机号格式不正确')
            elif not (ma and ma[0] == request.POST.get('major')):
                return dict_to_json(state='majorError', messages='年级专业格式不正确')
            elif request.POST.get('departer') not in ['程序开发', 'APP开发', '游戏开发', '前端开发', 'UI设计']:
                return dict_to_json(state='departerError', messages='部门格式不正确')
            elif request.POST.get('code') != str(request.session['code']):
                return dict_to_json(state='codeError', messages='验证码不正确')
            elif request.POST.get('email') != request.session['email']:
                return dict_to_json(state='emailError', messages='邮箱被修改')
            else:
                sid = get_code(type='sid')
                user_data = {'email': request.POST['email'],
                             'name': request.POST['name'],
                             'phone': request.POST['phone'],
                             'major': request.POST['major'],
                             'departer': request.POST['departer']}
                if isinstance(user_data, (dict,)):
                    user_data.update({"enable": 1, "status": 0, "sid": sid})
                    Register.objects.create(**user_data)
                    return dict_to_json(state='success', messages='访问提交成功')
                else:
                    return dict_to_json(state='dataError', messages='提交的数据有误')
        else:
            return dict_to_json(state='postError', messages='提交参数不全')
    else:
        return dict_to_json(state='postError', messages='未提交POST')


@ban
def check(request):
    if request.method == 'GET':
        if request.GET.get('email'):
            email_exist = Register.objects.filter(email=request.GET.get('email')).first()
            if email_exist:
                status = email_exist.status
                enable = email_exist.enable
                if enable:
                    return dict_to_json(state='success', messages='访问提交成功', status=status)
                else:
                    return dict_to_json(state='stateError', messages='邮箱未激活', status='None')
            else:
                return dict_to_json(state='emailError', messages='邮箱不存在', status='None')
        else:
            return dict_to_json(state='emailError', messages='未提交邮箱', status='None')


def department(request):
    if request.method == 'GET':
        request.session['ip'] = get_ip(request)
        request.session['ban'] = request.GET.get('ban')
        js = []
        deps = Department.objects.all()
        for i in deps:
            js.append(
                {
                    'department': i.name,
                    'introduce': i.introduce,
                }
            )

        return dict_to_json(state='success', messages='访问提交成功', departments=js)


@ban
def member(request):
    if request.method == 'GET':
        grade = request.GET.get('grade')
        department = request.GET.get('department')
        members = Member.objects.filter(grade=grade, department=department)
        details = []
        for i in members:
            details.append({
                'name': i.name,
                'quote': i.quotes,
                'img': f'http://121.199.2.83/media/{i.img.name}',
            })

        return dict_to_json(grade=grade, department=department, num=len(details), detail=details)


@ban
def history(request):
    if request.method == 'GET':
        year = request.GET.get('year')

        history = History.objects.filter(year=year)
        details = []
        for i in history:
            details.append(
                {
                    'title': i.title,
                    'content': i.detail,
                }
            )

        return dict_to_json(year=year, num=len(history), detail=details)


@ban
def work(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        if not page:
            page = 1
        page = int(page)
        works = Work.objects.all()
        js = []
        if (len(works) - 6 * (page - 1)) > 6:

            for i in range(6):
                js.append(
                    {
                        'title': works[i + 6 * (page - 1)].title,
                        'img': f'http://121.199.2.83/media/{works[i + 6 * (page - 1)].img.name}',
                        'url': works[i + 6 * (page - 1)].url,
                    }
                )

        else:
            for i in range((len(works) - 6 * (page - 1))):
                js.append(
                    {
                        'title': works[i + 6 * (page - 1)].title,
                        'img': f'http://121.199.2.83/media/{works[i + 6 * (page - 1)].img.name}',
                        'url': works[i + 6 * (page - 1)].url,
                    }
                )
        return dict_to_json(page=page, works=js)


@ban
def comment(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        if not page:
            page = 1
        page = int(page)
        amount = request.GET.get('amount')
        if not amount:
            amount = '-1'
        comments = Comment.objects.all()

        if amount != '-1':
            comments = comments[:int(amount)]

        page_size = len(comments) // 10 + bool(len(comments) % 10)
        if amount == str(len(comments)):
            update = 0
        else:
            update = 1

        js = []
        if len(comments) - 10 * (page - 1) >= 10:

            for i in range(10):
                js.append(
                    {
                        'time': comments[len(comments) - 1 - i - 10 * (page - 1)].create_time.strftime('%Y-%m-%d '
                                                                                                       '%H:%M:%S'),

                        'content': comments[len(comments) - 1 - i - 10 * (page - 1)].content
                    }
                )
        else:
            for i in range(len(comments) - 10 * (page - 1)):
                js.append(
                    {
                        'time': comments[len(comments) - 1 - i - 10 * (page - 1)].create_time.strftime('%Y-%m-%d '
                                                                                                       '%H:%M:%S'),
                        'content': comments[len(comments) - 1 - i - 10 * (page - 1)].content
                    }
                )
        info = {
            'page': page,
            'amount': len(comments),
            'page_max': page_size,
            'update': update
        }
        return dict_to_json(info=info, comments=js)
    elif request.method == 'POST':
        content = request.POST.get('content')
        if content and content != '':
            wait_time = comment_ip(request)
            # wait_time = 0
            if wait_time == 0:
                comment_file = Comment(content=content)
                comment_file.save()
                return dict_to_json(state="success", messages="评论提交成功")
            else:
                return dict_to_json(state="error", messages=f"请等待{wait_time}秒后重试")
        else:
            return dict_to_json(state="error", messages="评论不能为空")


def data_init(request):
    main_url = 'http://www.itstudio.club/show/api/member/?'
    for year in range(2011, 2021):
        for id in range(8):
            response = requests.get(main_url + 'year=' + str(year) + '&id=' + str(id))
            text = eval(response.content)
            if text['num']:
                for i in text['list']:
                    img_url = 'http://www.itstudio.club/' + i['image']
                    response = requests.get(img_url)
                    sid1 = get_code(type='side')
                    with open('/home/learn/itstudio/media/{}_{}.jpg'.format(sid1, i['name']), 'wb+') as img:
                        img.write(response.content)
                    member_file = Member(name=i['name'], grade=year, department=i['department'],
                                         quotes=i['info'], img='{}_{}.jpg'.format(sid1, i['name']))
                    member_file.save()
                    print('ok')

    return HttpResponse('200')


@login_required
def exportToExcel(request):
    if request.method == 'GET':
        # 创建一个WorkBook
        wb = openpyxl.Workbook()
        # 创建一个Sheet
        sheet = wb.active
        # 获取数据库中的数据
        sid = request.GET.get('sid')
        if sid:
            users_list = get_data(sid)
        else:
            users_list = get_all_data()
        # 往Excel的Sheet填充内容
        i = j = 1  # i表示行,j表示列
        len_list = len(users_list)
        while i <= len_list:
            while j <= 8:
                sheet.cell(i, j, users_list[i - 1][j - 1])
                j += 1
            i += 1
            j = 1
        # 设置响应头
        response = HttpResponse(content_type='application/msexcel')
        # 设置下载文件编码，需要使用urlquote
        filename = urlquote('爱特报名表.xlsx')
        response['Content-Disposition'] = f"attachment;filename*=utf-8'zh_cn'{filename}"
        # 保存Excel到相应中
        wb.save(response)
        return response


@login_required
def get_ip_json(request):
    if request.method == 'GET':
        json = {}
        if request.GET.get('type') == 'comment':
            comment_ip_dicts = {}
            for ip in comment_ip_dict:
                timeArray = time.localtime(comment_ip_dict[str(ip)])
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                comment_ip_dicts[str(ip)] = otherStyleTime
            json.update({"评论提交IP池": comment_ip_dicts})
        elif request.GET.get('type') == 'code':
            code_ip_dicts = {}
            for ip in code_ip_dict:
                timeArray = time.localtime(code_ip_dict[str(ip)])
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                code_ip_dicts[str(ip)] = otherStyleTime
            json.update({"验证码获取IP池": code_ip_dicts})
        elif request.GET.get('type') == 'ban':
            ban_ip_list = b_ip
            json.update({"被封IP池": ban_ip_list})
        else:
            return dict_to_json(state="error", messages="IP池获取失败")
        return dict_to_json(state="success", messages="IP池获取成功", ip_dirc=json)


def test(request):
    """获取请求者的IP信息"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return HttpResponse(ip)
