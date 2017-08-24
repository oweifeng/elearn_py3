from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q  # Q可以帮助实现并集
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 会用username或者email对传入的username进行匹配
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)   # 实例化LoginForm类的对象, 需传入request.POST参数
        if login_form.is_valid():   # 检查login_form是否出错, 没出错的才验证用户名和密码
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户未激活,请先邮箱激活."})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误!"})
        else:
            return render(request, "login.html", {"login_form":login_form})  # 如果login_form出错, 则返回login_from对象, 在前端进一步处理


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(username=user_name):
                return render(request, "register.html", {'register_form': register_form, "msg": "用户已存在."})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False  # 待通过邮箱验证之后才把该值置真
            user_profile.save()

            send_register_email(user_name, "register")
            return render(request, "login.html", {"msg": "已注册成功, 请登录."})
        else:
            return render(request, "register.html", {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                user = UserProfile.objects.get(email=record.email)
                user.is_active = True
                user.save()
            return render(request, "login.html", {"msg": "已激活成功, 请登录."})
        else:
            return render(request, "active_fail.html")


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})
    def post(self, request):
        forget_form = ForgetForm(request)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
