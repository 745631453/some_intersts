from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from utlis.funcktions import db


class BaseModel(object):
    #
    creat_time = db.Column(db.DATETIME, default=datetime.now())
    update_time = db.Column(db.DATETIME, default=datetime.now(), onupdate=datetime.now())

    def add_update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# 创建用户
class User(BaseModel, db.Model):
    __tablename__ = 'ihome_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(11), unique=True)
    pwd_hash = db.Column(db.String(200))
    name = db.Column(db.String(30), unique=True)
    avatar = db.Column(db.String(100))  # 头像
    id_name = db.Column(db.String(30))  # 实名认证姓名
    id_card = db.Column(db.String(18), unique=True)  # 实名认证身份证号

    houses = db.relationship('House', backref='user')
    orders = db.relationship('Order', backref='user')

    # 读
    @property
    def password(self):
        return ''

    # 写
    @password.setter
    def password(self, pwd):
        self.pwd_hash = generate_password_hash(pwd)

    # 对比验证
    def check_pwd(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)

    #
    def to_basic_dict(self):
        return {
            'id': self.id,
            'avatar': self.avatar if self.avatar else '',
            'name': self.name,
            'phone': self.phone
        }


# 多对对
ihome_house_facility = db.Table(
    'ihome_house_facility',
    db.Column('house_id', db.Integer, db.ForeignKey('ihome_house.id'), primary_key=True),
    db.Column('facility_id', db.Integer, db.ForeignKey('ihome_facility.id'), primary_key=True)
)


class House(BaseModel, db.Model):
    __tablename__ = 'ihome_house'
    id = db.Column(db.Integer, primary_key=True)
    # 房屋主人用户编号
    user_id = db.Column(db.Integer, db.ForeignKey('ihome_user.id'), unique=False)
    # 归属地区域编号
    area_id = db.Column(db.Integer, db.ForeignKey('ihome_area.id'), unique=False)
    title = db.Column(db.String(64), nullable=False)  # 标题
    price = db.Column(db.Integer, default=0)  # 单价 单位分
    address = db.Column(db.String(512), default='')  # 地址
    room_count = db.Column(db.Integer, default=1)  # 房间数目
    acreage = db.Column(db.Integer, default=0)  # 房屋面积
    unit = db.Column(db.String(32), default='')  # 房屋单元
    capacity = db.Column(db.Integer, default=1)  # 房屋容纳的人数
    beds = db.Column(db.String(64), default='')  # 房屋床铺配置
    deposit = db.Column(db.Integer, default=0)  # 押金
    min_days = db.Column(db.Integer, default=1)  # 最少住几天
    msx_days = db.Column(db.Integer, default=0)
    order_count = db.Column(db.Integer, default=0)  # 预定完成的该房屋订单数
    index_image_url = db.Column(db.String(256), default='')  # 房屋主图片路径

    # 房屋设施
    facilities = db.relationship('Facility', secondary=ihome_house_facility)
    images = db.relationship('HouseImage')  # 房屋图片
    orders = db.relationship('Order', backref='house')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'image': self.index_image_url if self.index_image_url else '',
            'area': self.area.name,
            'price': self.price,
            'create_time': self.creat_time.strftime('%Y-%m-%d %H:%M:%S'),
            'room': self.room_count,
            'order_count': self.order_count,
            'address': self.address
        }

    def to_full_dict(self):
        return {
            'id': self.id,
            'user_avatar': self.user.avatar if self.user.avatar else '',
            'user_name': self.user.name,
            'title': self.title,
            'price': self.price,
            'address': self.address,
            'room_count': self.room_count,
            'acreage': self.acreage,
            'unit': self.unit,
            'capacity': self.capacity,
            'beds': self.beds,
            'deposit': self.deposit,
            'min_days': self.min_days,
            'max_days': self.msx_days,
            'order_count': self.order_count,
            'image': [image.url for image in self.images],
            'images': self.index_image_url if self.index_image_url else '',
            'facilities': [facility.to_dict() for facility in self.facilities]
        }


class HouseImage(BaseModel, db.Model):
    # 房屋图片
    __tablename__ = 'ihome_house_image'

    id = db.Column(db.Integer, primary_key=True)
    # 房屋编号
    house_id = db.Column(db.Integer, db.ForeignKey('ihome_house.id'), nullable=False)
    url = db.Column(db.String(256), nullable=False)  # 图片的路径


class Facility(BaseModel, db.Model):
    # 设施信息规格等
    __tablename__ = 'ihome_facility'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)  # 设施名
    css = db.Column(db.String(30), nullable=False)  # 设施展示的图片

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'css': self.css
        }

    def to_house_dict(self):
        return {'id': self.id}


class Area(BaseModel, db.Model):
    # 城区
    __tablename__ = 'ihome_area'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)  # 区域名
    houses = db.relationship('House', backref='area')  # 区域房屋

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Order(BaseModel, db.Model):
    __tablename__ = 'ihome_order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('ihome_user.id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('ihome_house.id'), nullable=False)
    begin_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    house_price = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(
        db.Enum(
            'WAIT_ACCEPT',  # 待接单
            'WAiT_PAYMENT',  # 待支付
            'PAID',  # 已支付
            'WAIT_COMMENT',  # 待评价
            'COMPLETE',  # 已完成
            'CANCELED',  # 已取消
            'REJECTED'  # 已拒单
        ),
        default='WAIT_ACCEPT', index=True)
    comment = db.Column(db.Text)

    def to_dict(self):
        return {
            'order_id': self.id,
            'house_title': self.house.title,
            'image': self.house.index_image_url if self.house.index_image_url else '',
            'create_date': self.creat_time.strftime('%y-%m-%d'),
            'begin_date': self.begin_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'amount': self.amount,
            'days': self.days,
            'status': self.status,
            'comment': self.comment
        }
