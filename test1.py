# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 15:23:16 2020

@author: 59654
"""
# from flask import Flask
# # 实例化，可视为固定格式
# app = Flask(__name__)

# # route()方法用于设定路由；类似spring路由配置
# @app.route('/helloworld')
# def hello_world():
#     return 'Hello, World!！！！'

# if __name__ == '__main__':
#     # app.run(host, port, debug, options)
#     # 默认值：host="127.0.0.1", port=5000, debug=False
#     app.run(host="0.0.0.0", port=5000)
    
    
# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# app.run()

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()