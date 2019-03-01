# -*- encoding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import  redis
import random,hashlib
import settings
from  django.shortcuts import  redirect

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib
import string


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def get_random_str(lens):
    return ''.join(random.sample('zyxwvutsrqponmlkjihgfecba1234567890', lens))

def replace_chart(oldstr=""):
    #oldstr="zwj@qudian.com"
    #if "@" in oldstr:
    #    oldstr=oldstr[0:oldstr.index("@")]
    return oldstr.lower().replace(" ","").replace("|","").replace("@qudian.com","")

def login_required(func):
    def chklogin(request, *args, **kwargs):
        login_result,chkresult,chkmess=mana_login().checkuserToken(request,1,"")
        if login_result:
            return func(request, *args, **kwargs)
        else:
            return  redirect('/login.html?action'+str(request.COOKIES))
    return chklogin


class mana_login():
    def __init__(self):
        self.r =  redis.StrictRedis(host="127.0.0.1", port=6379, db=8)
        self.r_Reader = redis.StrictRedis(host="127.0.0.1", port=6379, db=8)

    def get_value(self,key):
        value=self.r.get(key)
        if value is None:
            return ""
        return value

    # ------------------------------------------登录-------------------------------------------------
    # self.do.从key中生成一个token放到redis中
    def get_user_selflogin_token(self, keys):
        newstr = self.get_user_selflogin_tokeninfo()
        token = self.get_random_str(25)
        self.r.set(self.get_selflogin_key(token), newstr)
        return token

    # self.do.取token从redis中
    def get_user_selflogin_info(self, token, isdelete):
        userinfo = self.r_Reader.get(self.get_selflogin_key(token))
        # if isdelete!="1":
        # self.r.delete(token)
        return userinfo

    def get_userinfo(self,request):
        reporttoken = request.COOKIES.get('token', '')
        reportusername = request.COOKIES.get('username', '')
        if len(reporttoken) > 10 and len(reportusername) > 0:
            username = self.r.get(self.get_token_user(reporttoken, reportusername))
            redis_username = self.get_redis_username(username)
            dic_user=self.r.hgetall(redis_username)
            if dic_user.has_key("userpower"):
                dic_user["password"]="********"
                dic_user["username"]=reportusername
            return dic_user
        return {}

    def del_userToken(self, request,response):
        reporttoken = request.COOKIES.get('token', '')
        reportusername = request.COOKIES.get('username', '')
        response.delete_cookie.set_cookie('nickname', "")
        response.delete_cookie.set_cookie('token', "")
        response.delete_cookie.set_cookie('chs', "")
        self.r.delete(self.get_token_user(reporttoken, reportusername))


    def checkuserToken(self,request,chkpower, chkname="", parentname=""):
        reporttoken = request.COOKIES.get('token', '')
        reportusername = request.COOKIES.get('username', '')
        reportchs = request.COOKIES.get('chs', '')
        if len(reporttoken) > 10 and len(reportusername) > 0:
            # ip验证
            username = self.r.get(self.get_token_user(reporttoken, reportusername))
            if username is None or len(username) < 1:
                return False,-1,'没有登录用户'
            redis_username = self.get_redis_username(username)
            if username == reportusername and self.get_token_md5(reporttoken,request) in reportchs.split(',') and self.r.exists(redis_username):
                Fsdisable = self.r_Reader.hget(redis_username, 'isdisable')
                if Fsdisable is None or Fsdisable <> 'true':
                    if self.r_Reader.hexists(redis_username, 'userpower'):
                        userpower = int(self.r_Reader.hget(redis_username, 'userpower'))
                        usergroup = self.r_Reader.hget(redis_username, 'usergroup')
                    else:
                        return False,-2,"没有权限组"
                    if userpower > chkpower:
                        return True,9,"权限组大于要求"
                    elif userpower > 0:
                        if len(chkname) == 0:
                            return True, 8, "chkname<0"
                        else:
                            set_userPresmission = self.get_redis_user_Permissions(username)
                            if self.check_resultpresmission(set_userPresmission, chkname, usergroup):
                                return True, 7, ""
                            elif '.' in chkname:
                                # lindex=chkname.find('.')
                                pid = chkname[0:chkname.find('.')]
                                if self.check_resultpresmission(set_userPresmission, pid, usergroup):
                                    return True, 6, ""
                            elif len(parentname) > 2:
                                if self.check_resultpresmission(set_userPresmission, parentname, usergroup):
                                    return True, 5, ""
                            else:
                                return False, -4, ""
                    else:
                        return  False, -3, ""
        return False, 0, ""

    def check_resultpresmission(self, set_userPresmission, checkname, usergroup=''):
        if self.r_Reader.sismember(set_userPresmission, checkname):
            return True
        elif self.r_Reader.sismember(self.get_redis_user_Permissions("@everyone"), checkname):
            return True
        else:
            if usergroup is not None and len(usergroup) > 0:
                usergrouplist = usergroup.split(',')
                for user_cname in usergrouplist:
                    if self.r_Reader.sismember(self.get_redis_user_Permissions(user_cname), checkname):
                        return True
        return False



    def login_reg(self,username,newkey):
        if len(username)<3 or len(newkey)<5:
            return False,"激活键或用户名长度验证失败"
        redis_username=self.get_redis_username(username)
        #if self.r.hexists(redis_username,"userpower"):
        #    return False,"用户已激活，不能重复激活"
        randvalue=self.get_value(newkey)
        if  "|" in randvalue:
            randlist=randvalue.split('|')
            chkusername=randlist[0]
            chkpassword=randlist[1]
            if chkusername==username:
                if not self.r.hexists(redis_username, "userpower"): #新用户
                    self.r.hsetnx(redis_username,"userpower",1)
                    self.r.set("admin_userlist:all",username)
                    self.r.hsetnx(redis_username, "usergroup", "")#待调用接口
                    self.r.hsetnx(redis_username, "nickname", "")  # 待调用接口
                    self.r.hsetnx(redis_username, "mobile", "")  # 待调用接口
                    self.r.hsetnx(redis_username, "password", chkpassword)  # 待调用接口
                    self.r.hsetnx(redis_username, "reg_token", "")
                self.r.delete(newkey)
                return True,"OK"
            else:
                return False,"用户名联机验证失败"
        else:
            return False,"没找到可用的激活键，或激活键已过期"

    def login_mail(self, username):
        username = username.lower().replace("|", "").replace(",", "")
        redis_username = self.get_redis_username(username)
        #islogin = False
        if self.r.exists(redis_username):
            # 用户存在
            password = self.r.hget(redis_username, "password")
        else:
            password=self.get_random_str(20)
        randstr = self.get_random_str(25)
        newkey = self.get_register_key(randstr)
        isoldkey=False
        if self.r.hexists(redis_username, "reg_token"):  # 已经有了激活键
            oldkey = self.r.hget(redis_username, "reg_token")
            if len(oldkey) > 5:  # 激活键可用
                if self.r.exists(oldkey):
                    newkey = oldkey
                    self.r.expire(oldkey, 60000)
                    isoldkey = True
        if not isoldkey:
            self.r.hset(redis_username, "reg_token", newkey)
            self.r.set(newkey, "%s|%s" % (username, password), 60000)
        self.sendmail("%s@qudian.com" % (username,), "权限申请系统用户登录",'<h2>权限申请系统用户登录></h2><p>点此完成验证：<a href="http://water.qudian.com/login.html?action=reg&username=%s&newkey=%s">http://water.qudian.com/login.html?action=reg&username=%s&newkey=%s</a></p>' % (username, newkey, username, newkey))
        return False, "已经发邮件到%s@qudian.com，请点击邮件里的链接完成登录" % (username,)
        if islogin:
            return True, "OK"
        else:
            return False, "None"

    #login验证成功后的处理
    def login_ok(self,request,response,username):
        randstr = self.get_random_str(25)
        redis_username=self.get_redis_username(username)
        token = hashlib.md5(username + randstr).hexdigest()
        if not self.r.hexists(redis_username, "userpower"):
            self.r.hset(redis_username, 'userpower', 1)
        self.r.set(self.get_token_user(token, username), username)  # last
        response.set_cookie('username', username, 99999999)
        response.set_cookie('token', token, 99999999)
        self.set_token_md5(token, True, request, response)
        pass


    
    @staticmethod
    def get_clientip(request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            return request.META['HTTP_X_FORWARDED_FOR']
        else:
            return request.META['REMOTE_ADDR']


    def get_token_md5(self, token,request):
        ipstr = self.get_clientip(request)
        print(ipstr)
        tokenchs = 'ws_%s_51ak_%s' % (ipstr, token)
        tokenchs_md5 = hashlib.md5(tokenchs).hexdigest()
        reporttoken = request.COOKIES.get('chs', '')
        return tokenchs_md5


    def set_token_md5(self, token, isdouble,request,response):
        ipstr = self.get_clientip(request)
        print(ipstr)
        tokenchs = 'ws_%s_51ak_%s' % (ipstr, token)
        tokenchs_md5 = hashlib.md5(tokenchs).hexdigest()
        reporttoken = request.COOKIES.get('chs', '')
        if isdouble and len(reporttoken) > 10:
            if tokenchs_md5 not in reporttoken.split(','):
                newchs = "%s,%s" % (tokenchs_md5, reporttoken)
                response.set_cookie('chs', newchs, 99999999)
        elif isdouble:
            response.set_cookie('chs', tokenchs_md5, 99999999)
        return tokenchs_md5

    @staticmethod
    def get_random_str(lens):
        return ''.join(random.sample('zyxwvutsrqponmlkjihgfecba1234567890', lens))

    @staticmethod
    def get_token_user(token, username):
        return "token:%s#%s" % (username, token)

    @staticmethod
    def get_register_key(token):
        return "register_key:%s" % (token,)

    @staticmethod
    def get_selflogin_key(token):
        return "selflogin:%s" % (token,)

        # hash 用户信息
    @staticmethod
    def get_redis_username(username):
        return 'admin_user:' + username

    # set 用户拥有的报表及管理权限
    @staticmethod
    def get_redis_user_Permissions(username):
        return 'admin_user_permiss:' + username

    @staticmethod
    def get_redis_user_Permissions_p(username):
        return 'admin_user_permiss_p:' + username

    # set 用户拥有的link权限
    @staticmethod
    def get_redis_user_PermissionsLink(username):
        return 'admin_user_permissLink:' + username

    @staticmethod
    def get_redis_user_PermissionsLink_p( username):
        return 'admin_user_permissLink_p:' + username

    def update_set_change(self, groupname, setname, newsetliststr, userkey="groupname", action="add"):
        # self.get_redis_user_Permissions
        newsetlist = []
        newsetlist_tmp = newsetliststr.replace(";", ",").replace("，", ",").split(',')
        for setvalue in newsetlist_tmp:
            if len(setvalue) > 2:
                newsetlist.append(setvalue)
        if action == "add":
            oldsetlist = []
            if self.r.exists(setname):
                return False, [], []
        else:
            oldsetlist = self.r.smembers(setname)
        newset = list(set(newsetlist).difference(set(oldsetlist)))
        oldset = list(set(oldsetlist).difference(set(newsetlist)))
        for setvalue in newset:
            self.r.sadd(setname, setvalue)
            if userkey == "get_redis_user_Permissions":
                self.r.sadd(self.get_redis_user_Permissions(setvalue), groupname)
            else:
                redis_setvalue = self.get_redis_username(setvalue)
                oldgroupname = self.r.hget(redis_setvalue, userkey)
                # print(oldgroupname)
                if oldgroupname is not None and len(oldgroupname) > 1:
                    self.r.hset(redis_setvalue, userkey, oldgroupname + "," + groupname)
                else:
                    self.r.hset(redis_setvalue, userkey, groupname)
        for setvalue in oldset:
            self.r.srem(setname, setvalue)
            if userkey == "get_redis_user_Permissions":
                self.r.srem(self.get_redis_user_Permissions(setvalue), groupname)
            else:
                redis_setvalue = self.get_redis_username(setvalue)
                oldgroupname = self.r.hget(redis_setvalue, userkey)
                # (oldgroupname)
                if oldgroupname is not None:
                    # print('9'*10)
                    newgroupname = oldgroupname.replace("," + groupname, "").replace(groupname + ",", "").replace(
                        groupname, "")
                    # print(newgroupname)
                    self.r.hset(redis_setvalue, userkey, newgroupname)
        return True, oldset, newset
    @staticmethod
    def sendmail(email,title,content):
        from_addr = 'weichongfeng@qudian.com'
        password = 'Woshitiancai0323!@'
        smtp_server = 'smtp.exmail.qq.com'
        server = smtplib.SMTP(smtp_server, 25)
        server.starttls()
        server.set_debuglevel(1)
        server.login(from_addr, password)
        to_addr = email
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = _format_addr('Manager of Auth<%s>' % from_addr)
        msg['Subject'] = title
        msg['To'] = _format_addr('<%s>' % to_addr)
        res = server.sendmail(from_addr, [to_addr], msg.as_string())
        return res
