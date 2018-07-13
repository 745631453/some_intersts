from django.conf.urls import url
from Ind import views

urlpatterns = [
    # 首页
    url(r'^home/', views.Home,name='home'),
    # 登录登出注册
    url(r'^log/', views.Login),
    url(r'^logout', views.Loginout),
    url(r'^reg/', views.Register),
    # 购物车
    url(r'^car/', views.Car),
    # 我的
    url(r'^mine/', views.Mine),
    # 闪购
    url(r'^market/$', views.Market, name='ma'),
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.use_Market, name='market'),
    # 闪购添加删除
    url(r'^add/', views.addshop),
    url(r'^del/', views.delshop),
    # 改变勾选
    url(r'^changecheck/', views.changecheck),
    # 购物车下单
    url(r'^xiadan/', views.order),
    # 购物车下单创建详情
    url(r'^xiandancreate/(\d+)/', views.Ordercreate, name='Ordercreate'),
    # 支付完成
    url(r'^complay/(\d+)/', views.Complay, name='complay'),
    # 跳转代付款
    url(r'^orderwait/', views.OrderWait),
    # 跳转待收货
    url(r'^orderpayed/', views.OrderPayed),
    url(r'^delxiadan/(\d+)', views.Delorder, name='delorder')
]
