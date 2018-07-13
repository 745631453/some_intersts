### 登录接口

#### request请求
POST/user/login/

#### params参数

    mobile 用户名
    password 登录密码

#### response响应

##### 失败响应1
    {
    "code": 1001,
    "msg": "手机号错误"
    }
    
##### 失败响应2
    {
    "code": 1005,
    "msg": "用户不存在"
    }

##### 失败响应3
    {
    "code": 1006,
    "msg": "密码错误"
    }

##### 失败响应4
    {
    "code": 901,
    "msg": "参数不能为空"
    }
    
##### 成功响应
    {'code': 200, 'msg': '请求成功'}