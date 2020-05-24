from api.models import Register


def state(self):
    if self.status == 0:
        return '初审未开始'
    elif self.status == 1:
        return '初审通过'
    elif self.status == 2:
        return '初审未通过'
    elif self.status == 3:
        return '面试通过'
    elif self.status == 4:
        return '面试未通过'
    elif self.status == 5:
        return '笔试通过'
    elif self.status == 6:
        return '笔试未通过'
    elif self.status == 7:
        return '录取通过'
    elif self.status == 8:
        return '录取未通过'
    else:
        return '状态错误'


# bool值状态改为字符串
def enable(self):
    if self.enable == True:
        return '用户已激活'
    else:
        return '用户未激活'


# datetime时间转为字符串时间
def changetime(self):
    str_time = self.create_time.strftime('%Y-%m-%d %H:%M:%S')
    return str_time


heard_list = ['学生姓名', '电子邮箱', '手机号码', '年级专业', '选择部门', '目前阶段', '激活状态', '创建时间']


def get_all_data():
    users = Register.objects.all()
    users_list = [heard_list]
    for user in users:
        user_list = [user.name, user.email, user.phone, user.major,
                     user.departer, state(user), enable(user), changetime(user)]
        users_list.append(user_list)
    return users_list


def get_data(sid):
    users = Register.objects.filter(sid=sid)
    users_list = [heard_list]
    for user in users:
        user_list = [user.name, user.email, user.phone, user.major,
                     user.departer, state(user), enable(user), changetime(user)]
        users_list.append(user_list)
    return users_list




