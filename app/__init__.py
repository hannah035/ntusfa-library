from flask import Flask
from upstash_redis import Redis

def create_app():
    app = Flask(__name__)
    
    # 配置 Upstash Redis
    app.redis = Redis(url="https://helpful-mako-37953.upstash.io", token="AZRBAAIncDEzNDZlNjU0YTViNDE0YmE4YmQ4YWJkZjE1MjU3ZmU2NnAxMzc5NTM")

    with app.app_context():
        # 導入路由
        from routes import init_app
        init_app(app)

    return app