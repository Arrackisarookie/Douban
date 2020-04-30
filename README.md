# Douban

### 配置
Python 3.6+
#### 依赖
`requirements.txt` 可使用以下命令安装依赖
```
$ pip install -r requirements.txt
```

#### 安全
`instance/secure.py`, _需自行创建并配置以下变量_

- SECRET_KEY
- SQLALCHEMY_DATABASE_URI
- SQLALCHEMY_TRACK_MODIFICATIONS

#### 环境(可选)
`.env`, _需自行创建并配置以下变量_

- FLASK_ENV

#### 应用
`app/config.py`, _已创建，可自行调整_
- MOVIES_PER_PAGE

### 使用
1. 克隆项目
2. 安装依赖，配置文件
3. 连接数据库
4. 在服务器后台输入以下命令初始化数据表
```
flask initdb
```
5. 在服务器后台输入以下命令从豆瓣自动爬取数据并存入数据库
```
flask crawl
```
6. 启动网站服务
