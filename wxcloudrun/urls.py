"""wxcloudrun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from wxcloudrun import views
#from django.conf.urls import url
from django.urls import path

# urlpatterns = (
#     # 计数器接口
#     url(r'^^api/count(/)?$', views.counter),
#     # 读取用户
#     url(r'^^api/getuser(/)?$', views.getuser),
#     # 获取主页
#     url(r'(/)?$', views.index)
# )

urlpatterns = [
    path('api/getuser', views.getuser),
    path('api/insertcountry', views.insertCountry),
    path('api/verify', views.verify),
    path('api/inserthistory', views.insertHistory),
    path('api/gethistory', views.getHistory),
    path('api/download', views.download),
    path('api/insertuser', views.insertUser),
    path('api/shibie',views.shibie),
    path('api/getiphone',views.getiphone),
    path('api/getxiaoqu',views.getXiaoqu),
    path('api/getalluser', views.getalluser),
    path('api/getallcontent',views.getAllContent),
    path('api/getcun', views.getCun),
]
