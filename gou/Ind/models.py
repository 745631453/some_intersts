from django.db import models


class Main(models.Model):
    img = models.CharField(max_length=200)  # 图片
    name = models.CharField(max_length=100)  # 名称
    trackid = models.CharField(max_length=16)  # 通用id

    class Meta:
        # 成为父类（抽象化）
        abstract = True


class MainLun(Main):
    # 轮播图
    class Meta:
        db_table = 'index_lun'


class MainDao(Main):
    # 导航
    class Meta:
        db_table = 'index_dao'


class MainMustBuy(Main):
    # 必购物
    class Meta:
        db_table = 'index_mustby'


class MainShop(Main):
    # 商店
    class Meta:
        db_table = 'axf_shop'


class MainShow(Main):
    # 主要展示商品
    categoryid = models.CharField(max_length=16)  # 分类名称
    brandname = models.CharField(max_length=100)  # 分类编号

    img1 = models.CharField(max_length=200)  # 图片
    childcid1 = models.CharField(max_length=16)
    productid1 = models.CharField(max_length=16)

    longname1 = models.CharField(max_length=100)  # 名称
    price1 = models.FloatField(default=0)  # 优惠价格
    marketprice1 = models.FloatField(default=1)  # 原始价格
    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=1)
    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=1)

    class Meta:
        db_table = 'axf_mainshow'


# 闪购（左侧导航栏）
class FoodType(models.Model):
    typeid = models.CharField(max_length=16)  # 分类id（导航栏中根据id显示对应对象）
    typename = models.CharField(max_length=100)  # 类型名称
    childtynames = models.CharField(max_length=200)  # 类型
    tyoesort = models.IntegerField(default=1)  # 排序

    class Meta:
        db_table = 'axf_foodtype'


class Goods(models.Model):
    # 商品展示
    productid = models.CharField(max_length=16)  # 商品编号
    productimg = models.CharField(max_length=200)  # 商品图
    productname = models.CharField(max_length=100)  # 商品名称
    productlongname = models.CharField(max_length=200)  # 商品规格名称
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)  # 商品细节规格
    price = models.FloatField(default=0)  # 折后价格
    marketprice = models.FloatField(default=1)  # 原价
    categoryid = models.CharField(max_length=16)  # 总的分类id
    childcid = models.CharField(max_length=16)  # 子分类id
    childcidname = models.CharField(max_length=100)  # 子名称
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)  # 分类排序（销量。好评度）
    productnum = models.IntegerField(default=1)  # 销量排序

    class Meta:
        db_table = 'axf_goods'


class MinModel(models.Model):
    # 用户
    usernam = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)
    sex = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='icons')  # 头像图片
    is_delete = models.BooleanField(default=False)  # 是否删除

    class Meta:
        db_table = 'axf_user'


class MineModel(models.Model):
    m = models.OneToOneField(MinModel)
    m_ticket = models.CharField(max_length=225)
    m_time = models.DateTimeField()

    class Meta:
        db_table = 'axf_user_tic'


class CartModel(models.Model):
    # 购物车
    user = models.ForeignKey(MinModel)  # 关联用户
    goods = models.ForeignKey(Goods)  # 管理商品
    c_num = models.IntegerField(default=1)  # 商品个数
    is_select = models.BooleanField(default=True)  # 是否勾选

    class Meta:
        db_table = 'axf_cart'


class OrderModel(models.Model):
    # 订单
    user = models.ForeignKey(MinModel)
    o_num = models.CharField(max_length=64)
    o_status = models.IntegerField(default=0)  # 状态
    o_create = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta:
        db_table = 'axf_order'


class OrderGoodsModel(models.Model):
    # 订单和商品的联系
    order = models.ForeignKey(OrderModel)  # 关联订单
    goods = models.ForeignKey(Goods)  # 关联商品
    goods_num = models.IntegerField(default=1)  # 商品个数

    class Meta:
        db_table = 'axf_order_goods'
