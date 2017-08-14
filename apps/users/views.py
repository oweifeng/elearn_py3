from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q  # Q可以帮助实现并集
from django.views.generic.base import View

from .models import UserProfile
from .forms import LoginForm


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
                login(request, user)
                return render(request, "index.html")
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误!"})
        else:
            return render(request, "login.html", {"login_form":login_form})  # 如果login_form出错, 则返回login_from对象, 在前端进一步处理


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html", {})
