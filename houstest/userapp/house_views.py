from flask import Blueprint, render_template, session, jsonify, request
from sqlalchemy import or_

from userapp.models import User, House, Area, Facility, HouseImage, Order
from utlis import status_code
from utlis.settings import UPLOAD_DIR
import os

house = Blueprint('house', __name__)


# 房屋首页
@house.route('/myhouse/')
def my_house():
    return render_template('myhouse.html')


# 传递首页参数
@house.route('/auth_myhouse/')
def auth_myhouse():
    user = User.query.get(session['user_id'])
    if user.id_card:
        houses = House.query.filter(House.user_id == user.id).order_by(House.id.desc())
        house_list = []
        for ho in houses:
            house_list.append(ho.to_dict())
        return jsonify(house_list=house_list, code=200)
    else:
        return jsonify(status_code.MYHOUSE_USE_ID_NOT_EXSITS)


# 添加房屋
@house.route('/newhouse/', methods=['GET'])
def newhouse():
    return render_template('newhouse.html')


# 传递添加房屋参数
@house.route('/facility/', methods=['GET'])
def area_fcil():
    areas = Area.query.all()
    areas_list = [i.to_dict() for i in areas]

    faciltys = Facility.query.all()
    faciltys_list = [a.to_dict() for a in faciltys]

    return jsonify(areas_list=areas_list, faciltys_list=faciltys_list, code=200)


# 添加参数到数据库
@house.route('/getnewhouse/', methods=['POST'])
def get_newhouse():
    # to_dict转化为字典 前端传递$(this).serialize()是个列表
    get_new = request.form.to_dict()
    facility = request.form.getlist('facility')

    title = get_new.get('title')
    price = get_new.get('price')
    area_id = get_new.get('area_id')
    address = get_new.get('address')
    room_count = get_new.get('room_count')
    acreage = get_new.get('acreage')
    unit = get_new.get('unit')
    capacity = get_new.get('capacity')
    beds = get_new.get('beds')
    deposit = get_new.get('deposit')
    min_days = get_new.get('min_days')
    max_days = get_new.get('max_days')

    houses = House()
    houses.user_id = session['user_id']
    houses.title = title
    houses.price = price
    houses.area_id = area_id
    houses.address = address
    houses.room_count = room_count
    houses.acreage = acreage
    houses.capacity = capacity
    houses.beds = beds
    houses.deposit = deposit
    houses.min_days = min_days
    houses.msx_days = max_days
    houses.unit = unit

    if facility:
        fac = Facility.query.filter(Facility.id.in_(facility)).all()
        houses.facilities = fac

    try:
        houses.add_update()
        return jsonify(code=status_code.OK, hous_id=houses.id)
    except Exception as e:
        return e


# 添加房屋图片
@house.route('/newimage/', methods=['POST'])
def nweimag():
    images = request.files.get('house_image')
    house_id = request.form.get('house_id')
    # 保存绝对路径
    url = os.path.join(UPLOAD_DIR, images.filename)
    images.save(url)
    # 保存相对路径
    im_url = os.path.join(os.path.join('/static', 'upload'), images.filename)

    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = im_url
    try:
        house_image.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)
    # 首页展示图片 如果没有就添加进去因此只会获得一张
    hou = House.query.get(house_id)
    if not hou.index_image_url:
        hou.index_image_url = im_url
        try:
            hou.add_update()
        except:
            return jsonify(status_code.DATABASE_ERROR)
    return jsonify(code=status_code.OK, im_url=im_url)


# 房屋详情页面
@house.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


# 根据房屋id展示页面详情
@house.route('/detail/<int:id>/', methods=['GET'])
def house_datail(id):
    houses = House.query.get(id)
    faciltys = houses.facilities
    fac_list = [facility.to_dict() for facility in faciltys]
    booking = 1
    if 'user_id' in session and houses.user_id == session['user_id']:
        booking = 0
    return jsonify(house=houses.to_full_dict(),
                   fac=fac_list,
                   booking=booking, code=status_code.OK)


# 预定页面
@house.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')


# 首页
@house.route('/index/', methods=['GET'])
def ndex():
    return render_template('index.html')


# 传递图片个人信息等给首页
@house.route('/hindex/', methods=['GET'])
def house_index():
    user_name = ''
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user_name = user.name

    houses = House.query.order_by(House.id.desc()).all()[:5]
    hlisr = [h.to_dict() for h in houses]

    areas = Area.query.all()
    alist = [area.to_dict() for area in areas]

    return jsonify(code=status_code.OK,
                   hlisr=hlisr,
                   alist=alist,
                   user_name=user_name)


# 搜索
@house.route('/search/', methods=['GET'])
def serach():
    return render_template('search.html')


@house.route('/allsearch/', methods=['GET'])
def house_serach():
    search_dict = request.args
    area_id = search_dict.get('aid')
    start_data = search_dict.get('sd')
    end_date = search_dict.get('ed')
    sk_dict = search_dict.get('sk')
    # 查询区域
    houses = House.query.filter(House.area_id == area_id)
    # 时间处理
    orders1 = Order.query.filter(Order.begin_date >= start_data,
                                 Order.end_date <= end_date)

    orders2 = Order.query.filter(Order.begin_date <= end_date,
                                 Order.end_date >= end_date)

    orders3 = Order.query.filter(Order.begin_date <= start_data,
                                 Order.end_date >= start_data)

    orders4 = Order.query.filter(Order.begin_date <= start_data,
                                 Order.end_date >= end_date)

    orders_list1 = [o1.house_id for o1 in orders1]
    orders_list2 = [o2.house_id for o2 in orders2]
    orders_list3 = [o3.house_id for o3 in orders3]
    orders_list4 = [o4.house_id for o4 in orders4]

    orders_list = orders_list1 + orders_list2 + orders_list3 + orders_list4
    order_list = list(set(orders_list))

    if sk_dict:
        if sk_dict == 'booking':
            sk_dict = House.room_count.desc()
        elif sk_dict == 'price-inc':
            sk_dict = House.price.asc()
        elif sk_dict == 'price-des':
            sk_dict = House.price.desc()
        else:
            sk_dict = House.creat_time.desc()
    else:
        sk_dict = House.id.desc()

    houses = houses.order_by(sk_dict)

    hous = houses.filter(House.id.notin_(order_list))
    house_list = [hou.to_full_dict() for hou in hous]

    areas = Area.query.all()
    alist = [a.to_dict() for a in areas]
    aris = Area.query.get(area_id)
    ar = aris.to_dict()

    return jsonify(code=status_code.OK,
                   alist=alist,house_list=house_list,
                   ar=ar)
