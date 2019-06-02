# Bluelog

*A blue blog.*

#### 流程

```
$ cd bluelog
$ pipenv install --dev
$ pipenv shell
$ flask forge
$ flask run
* Running on http://127.0.0.1:5000/
```

#### 测试账户密码:

* username: `admin`
* password: `ltf1234`


#### 下载镜像源

如果执行`pipenv install`命令安装依赖耗时太长，你可以考虑使用国内的PyPI镜像源，比如：
```
$ pipenv install --dev --pypi-mirror https://mirrors.aliyun.com/pypi/simple
```

