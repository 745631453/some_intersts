### 注册接口


#### request请求
POST/user/register/
##### params参数

    moblie str 电话
    password str 密码
    password2 str 确认密码

#### response响应

##### 失败响应1：
    {'code': 1000, 'msg': '注册信息参数不能为空'}

##### 失败响应2：
    {'code': 1000, 'msg': '手机号错误'}

##### 失败响应3：
    {'code': 1000, 'msg': '手机号已经注册'}

##### 失败响应4：
    {'code': 1000, 'msg': '两次密码错误'}

##### 成功响应：
    {'code': 200, 'msg': '请求成功'}