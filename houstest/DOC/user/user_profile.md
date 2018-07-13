### 修改用户信息

#### request请求
POST/user/mprofile/

#### params参数
    avatar str 用户传入图片地址
    name str 用户名

#### 请求方式：PUT


##### 失败响应1
    {
    "code": 901,
    "msg": "参数不能为空"
    }
##### 失败响应2
    {'code': 1007, 'msg': '用户名已经注册'}
##### 失败响应3
    {'code': 900, 'msg': '数据库错误'}
##### 失败响应4
    {'code': 1006, 'msg': '图片不符合'}
##### 失败响应5