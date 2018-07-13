OK = 200
SUCCESS = {'code': 200, 'msg': '请求成功'}
DATABASE_ERROR = {'code': 900, 'msg': '数据库错误'}
PARAMS_ERROR = {'code': 901, 'msg': '参数不能为空'}

# 用户模块
USER_REGISTER_PARAMS_ERROR = {'code': 1000, 'msg': '注册信息参数不能为空'}
USER_REGISTER_MOBILE_ERROR = {'code': 1001, 'msg': '手机号错误'}
USER_REGISTER_MOBILE_IS_EXSITS = {'code': 1002, 'msg': '手机号已经注册'}
USER_REGISTER_PASSWORD_IS_ERROR = {'code': 1003, 'msg': '两次密码错误'}

USER_LOGIN_PASSWORD_IS_ERROR = {'code': 1006, 'msg': '密码错误'}
USER_LOGIN_IS_NOT_EXSIST = {'code': 1005, 'msg': '用户不存在'}

USER_PROFILE_IMG_ERRO = {'code': 1006, 'msg': '图片不符合'}

USER_UPDATE_USERNAME_IS_EXSITS = {'code': 1007, 'msg': '用户名已经注册'}

USER_AUTH_IDCARE_IS_ERROR = {'code': 1008, 'msg': '用户身份证有误'}

# 房屋
MYHOUSE_USE_ID_NOT_EXSITS = {'code': 2000, 'msg': '用户没有实名认证'}
# 订单
ORDER_START_TIME_GT_END_TIME = {'code': 3000, 'msg': '订单时间有误'}
