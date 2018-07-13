from flask import Blueprint, request, render_template, jsonify, session
from utlis import status_code
from userapp.models import Order, House
from datetime import datetime

order = Blueprint('order', __name__)


# 获取预定参数
@order.route('/', methods=['POST'])
def getor():
    order_dict = request.form

    houser_id = order_dict.get('house_id')
    start_time = datetime.strptime(order_dict.get('start_time'), '%Y-%m-%d')
    end_time = datetime.strptime(order_dict.get('end_time'), '%Y-%m-%d')
    house = House.query.get(houser_id)
    if not all([houser_id, start_time, end_time]):
        return jsonify(status_code.PARAMS_ERROR)
    if start_time > end_time:
        return jsonify(status_code.ORDER_START_TIME_GT_END_TIME)

    if not house.msx_days > (end_time - start_time).days < house.min_days:
        if house.msx_days == 0:
            pass
        else:
            return jsonify(status_code.ORDER_START_TIME_GT_END_TIME)

    order = Order()
    order.user_id = session['user_id']
    order.house_id = houser_id
    order.begin_date = start_time
    order.end_date = end_time
    order.house_price = house.price
    order.days = (end_time - start_time).days
    order.amount = order.days * order.house_price
    try:
        order.add_update()
        return jsonify(code=status_code.OK)
    except:
        return jsonify(status_code.DATABASE_ERROR)


@order.route('/order/', methods=['GET'])
def orders():
    return render_template('orders.html')


@order.route('/allorders/', methods=['GET'])
def allorders():
    order = Order()
    order_g = order.query.filter(Order.user_id == session['user_id'])
    order_get = [orde.to_dict() for orde in order_g]

    return jsonify(code=status_code.OK, order_get=order_get)


@order.route('/lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')


@order.route('/fd/', methods=['GET'])
def lorders_fd():
    # 查房东id
    housers = House.query.filter(House.user_id == session['user_id'])
    housers_ids = [house.id for house in housers]
    # 根据房屋id找订单
    orders = Order.query.filter(Order.house_id.in_(housers_ids))
    olist = [orde.to_dict() for orde in orders]
    # 方法二：

    return jsonify(code=status_code.OK, olist=olist)


@order.route('/order/<int:id>/', methods=['PATCH'])
def order_status(id):
    status = request.form.get('status')
    orde = Order.query.get(id)
    orde.status = status

    if status == 'REJECTED':
        comment = request.form.get('comment')
        orde.comment = comment
    try:
        orde.add_update()
        return jsonify(code=status_code.OK)
    except:
        return jsonify(status_code.DATABASE_ERROR)
