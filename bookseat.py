# /bin/python
# -*- coding:utf-8 -*-
import time
import sys
import requests
from bs4 import BeautifulSoup


__author__ = 'xy'

# 主类
class FUCK():
    def __init__(self, username, password, seatNO):
    
    #    以四个参数初始化，用户名，密码，要预约的座位号，接受预约结果提醒邮件的邮箱
    
        self.username = username
        self.password = password
        self.seatNO = seatNO
        self.base_url = 'http://202.112.150.5:82/'
        self.login_url = 'http://202.112.150.5:82/'
        self.order_url = self._get_order_url()

        self.login_content = ''
        self.middle_content = ''
        self.final_content = ''

        self.s = requests.session()  # 创建可传递cookies的会话

        # post data for login
        self.data1 = {
            'subCmd': 'Login',
            'txt_LoginID': self.username,  # S+学号
            'txt_Password': self.password,  # 密码
            'selSchool': 60,  # 60表示北京交通大学
        }

        # post data for order a seat
        self.data2 = {
            'subCmd': 'query',
        }

        # 自定义http头，然而我在程序里并没有使用
        self.headers = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        self.login()
        self.run()
        

        # 怀疑程序出错时，取消下行注释，可打印一些参数
        # self._debug()

    def _get_date_str(self):
        s = time.localtime(time.time())
        ########333
        date_str = str(s.tm_year) + '%2f' + str(s.tm_mon) + '%2f' + str(s.tm_mday + 1)
        date_str = date_str.replace('%2f1%2f32', '%2f2%2f1') \
            .replace('%2f2%2f29', '%2f3%2f1') \
            .replace('%2f3%2f32', '%2f4%2f1') \
            .replace('%2f4%2f31', '%2f5%2f1') \
            .replace('%2f5%2f32', '%2f6%2f1') \
            .replace('%2f6%2f31', '%2f7%2f1') \
            .replace('%2f7%2f32', '%2f8%2f1') \
            .replace('%2f8%2f32', '%2f9%2f1') \
            .replace('%2f9%2f31', '%2f10%2f1') \
            .replace('%2f10%2f32', '%2f11%2f1') \
            .replace('%2f11%2f31', '%2f12%2f1') \
            .replace('%2f12%2f32', '%2f1%2f1')
        return date_str

    def _get_order_url(self):
        return "http://202.112.150.5:82/BookSeat/BookSeatMessage.aspx?seatNo=101002" + self.seatNO + "&seatShortNo=02" + self.seatNO + "&roomNo=101002&date=" + self._get_date_str()

    def _get_static_post_attr(self, page_content, data_dict):
       
        # 拿到<input type='hidden'>的post参数，并添加到post_data中
        
        soup = BeautifulSoup(page_content, "html.parser")
        for each in soup.find_all('input'):
            if 'value' in each.attrs and 'name' in each.attrs:
                data_dict[each['name']] = each['value']  # 添加到login的post_data中
                # self.data2[each['name']] = each['value']  # 添加到order的post_data中
        return data_dict

    
    def login(self):
        homepage_content = self.s.get(self.base_url).content
        self.data1 = self._get_static_post_attr(homepage_content, self.data1)
        r = self.s.post(self.login_url, self.data1)
        self.login_content = r.content

    def run(self):

        # 这个get的意思是：原先的cookie没有预约权限，
        # 访问这个get之后，会使cookie拥有预约权限，从而执行下一个post
        self.middle_content = self.s.get('http://202.112.150.5:82/BookSeat/BookSeatListForm.aspx').content

        # 经测试，这个post只需要一个subCmd的参数就可以正常返回，因此不必根据get内容更新post参数
        # self.data2 = self._get_static_post_attr(middle_content, self.data2)

        # 这个post请求完成了预约功能！
        r = self.s.post(self.order_url, self.data2)

        self.final_content = r.content

  
   

   

   

if __name__ == '__main__':
    
        FUCK(S12274091,S12274091,178)
