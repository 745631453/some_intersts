import random
from datetime import datetime, timedelta
import time
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from Ind.models import MainLun, MainDao, MainMustBuy, MainShop, MainShow, MinModel \
    , MineModel, FoodType, Goods, OrderGoodsModel, CartModel, OrderModel


# 首页展示
def Home(request):
    # 将数据库的的参数传到页面去展示，同时注意只展示一个或指定的几个的时候要么在数据库中切片
    # 要么在页面中forloop.counter函数定义
    if request.method == 'GET':
        lun = MainLun.objects.all()
        dao = MainDao.objects.all()
        buy = MainMustBuy.objects.all()
        shop = MainShop.objects.all()
        shop1 = MainShop.objects.all()[0]
        shop2 = list(MainShop.objects.all()[1:3])
        shop3 = list(MainShop.objects.all()[3:7])
        shop4 = list(MainShop.objects.all()[7:11])
        show = MainShow.objects.all()
        ttp = {
            'lun': lun,
            'dao': dao,
            'buy': buy,
            'shop': shop,
            'show': show,
            'shop1': shop1,
            'shop2': shop2,
            'shop3': shop3,
            'shop4': shop4,

        }

        return render(request, 'home/home.html', ttp)


# 登录页面
def Login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        nam = request.POST.get('username')
        passwor = request.POST.get('password')
        if MinModel.objects.filter(usernam=nam).exists():
            name = MinModel.objects.get(usernam=nam)
            if name.password == passwor:
                # 设置cookie值
                ticket = ''
                for _ in range(15):
                    a = 'abcdefghijklmnopqrstuvwxyz'
                    ticket += random.choice(a)
                ti = int(time.time())
                ticket += str(ti)
                re = HttpResponseRedirect('/ind/home/')
                # 设置失效时间
                out_time = datetime.now() + timedelta(days=1)
                # 保存客户端
                re.set_cookie('ticket', ticket, expires=out_time)
                # 保存服务器
                MineModel.objects.create(m_id=name.id, m_ticket=ticket, m_time=out_time)

                return re

            else:
                return HttpResponse('密码错误')
        else:
            return HttpResponse('用户不存在')


# 登出页面
def Loginout(request):
    if request.method == 'GET':
        tic = request.COOKIES.get('ticket')
        # 删除数据库的值
        MineModel.objects.filter(m_ticket=tic).delete()
        re = HttpResponseRedirect('/ind/home/')
        # 删除浏览器的值
        re.delete_cookie('ticket')

        return re


# 注册页面
def Register(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':
        # 获取页面值
        name = request.POST.get('username')
        e = request.POST.get('email')
        pa = request.POST.get('password')
        ic = request.FILES.get('icon')
        # 保存数据库中
        MinModel.objects.create(
            usernam=name,
            email=e,
            password=pa,
            icon=ic,
        )

        return HttpResponseRedirect('/ind/log/')


# 购物车页面
def Car(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            a = CartModel.objects.filter(user=user)

            return render(request, 'cart/cart.html', {'a': a})
        else:
            return HttpResponseRedirect('/ind/log/')


# 我的 页面
def Mine(request):
    if request.method == 'GET':
        # 传入浏览器字典——可以读写出待收货等状态
        date = {}
        # 通过中间键传入参数获取参数
        user = request.user
        # 判断是否有ticket值
        if user.id:
            # 和状态表关联
            o = user.ordermodel_set.all()
            a, b = 0, 0
            # 给状态赋值
            for i in o:
                if i.o_status == 0:
                    a += 1
                elif i.o_status == 1:
                    b += 1
            date = {
                'a': a,
                'b': b
            }

        return render(request, 'mine/mine.html', date)


# 默认传参至商品展示
def Market(request):
    return HttpResponseRedirect(reverse('axf:market', args=('104749', '0', '0')))


# 闪购商品展示
def use_Market(request, a, b, c):
    if request.method == 'GET':
        user = request.user
        date = {}
        # 获取类型
        foo = FoodType.objects.all()
        # 获取商品
        if b == '0':
            good = Goods.objects.filter(categoryid=a)
        else:
            good = Goods.objects.filter(childcid=b, categoryid=a)
        # 获取分类
        fenlei = []
        ff = FoodType.objects.filter(typeid=a).first()
        ff_list = ff.childtynames.split('#')
        for lis in ff_list:
            fenlei.append(lis.split(':'))
        # 定义排序原则
        if c == '0':
            pass
        elif c == '1':
            good = good.order_by('productnum')
        elif c == '2':
            good = good.order_by('price')
        elif c == '3':
            good = good.order_by('-price')
        date['user'] = user
        date['food'] = foo
        date['tpid'] = a
        date['cid'] = b
        date['good'] = good
        date['fenlei'] = fenlei

        return render(request, 'market/market.html', date)


# 静态页面添加
def addshop(requset):
    if requset.method == 'POST':
        user = requset.user
        date = {
            'msg': '成功',
            'code': 200
        }
        if user.id:
            goods_id = requset.POST.get('goods_id')
            add = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            if add:
                alln = CartModel.objects.filter(user=user,is_select=1)
                allnum = 0
                for i in alln:
                    a = float(i.goods.price)
                    b = i.c_num
                    allnum += a * b
                add.c_num += 1
                add.save()
                date['c_num'] = add.c_num
                date['allnum'] = allnum
            else:
                CartModel.objects.create(user=user, goods_id=goods_id, c_num=1)
                date['c_num'] = 1
        return JsonResponse(date)


# 静态页面减少数量
def delshop(requset):
    if requset.method == 'POST':
        user = requset.user
        date = {
            'msg': '成功',
            'code': 200
        }
        if user.id:
            goods_id = requset.POST.get('goods_id')
            dele = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            if dele:
                if dele.c_num > 0:
                    if dele.c_num == 1:
                        dele.delete()
                        date['c_num'] = 0
                    else:
                        dele.c_num -= 1
                        dele.save()
                        date['c_num'] = dele.c_num
        return JsonResponse(date)


# 购物车中勾选按钮
def changecheck(request):
    if request.method == 'POST':
        date = {}
        user = request.user
        if user.id:
            gid = request.POST.get('goods_id')
            de = CartModel.objects.filter(goods_id=gid).first()
            if de.is_select:
                de.is_select = False
            else:
                de.is_select = True
            de.save()
            date = {'changecheck': de.is_select}
        return JsonResponse(date)


# 创建订单
def order(request):
    if request.method == 'GET':
        user = request.user
        cart = CartModel.objects.filter(is_select=True)
        if cart:
            orderid = OrderModel.objects.create(user=user, o_status=0)
            for i in cart:
                OrderGoodsModel.objects.create(goods=i.goods,
                                               order=orderid,
                                               goods_num=i.c_num,
                                               )
                i.delete()
            return HttpResponseRedirect(reverse('axf:Ordercreate', args=(orderid.id,)))
        else:
            return HttpResponseRedirect(reverse('axf:ma'))


# 付款页面
def Ordercreate(request, id):
    if request.method == 'GET':
        orders = OrderGoodsModel.objects.filter(order_id=id)
        order1 = orders.first().order_id
        date = {
            'orders': orders,
            'order': order1,
        }

        return render(request, 'order/order_info.html', date)


# 将付款状态调制待收货
def Complay(request, orderid):
    if request.method == 'GET':
        OrderModel.objects.filter(pk=orderid).update(o_status=1)
        return HttpResponseRedirect(reverse('axf:home'))


# 代付款页面
def OrderWait(request):
    if request.method == 'GET':
        wait = OrderModel.objects.filter(o_status=0)
        date = {
            'wait': wait
        }

        return render(request, 'order/order_list_wait_pay.html', date)


# 待收货页面
def OrderPayed(request):
    if request.method == 'GET':
        payed = OrderModel.objects.filter(o_status=1)
        date = {
            'wait': payed
        }

        return render(request, 'order/order_list_payed.html', date)


def Delorder(request, o_id):
    if request.method == 'GET':
        OrderGoodsModel.objects.filter(order=o_id).delete()
        OrderModel.objects.filter(pk=o_id).delete()

        return HttpResponseRedirect('/ind/orderwait/')
