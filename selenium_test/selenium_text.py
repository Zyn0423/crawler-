#-*-coding=utf8-*-
from selenium import webdriver
import traceback
# try:
#     webrequest=webdriver.Chrome(r'')
#     # webrequest=webdriver.PhantomJS(r'')
#     url = 'http://www.itcast.cn'
#     webrequest.get(url)
# except Exception:
#     详细异常打印
#     traceback.format_exc



# # 1\实例化一个driver对象
# driver = webdriver.Chrome('')
# # 模拟浏览器访问url
# driver.get('https://www.douban.com/')
# ret1 = driver.find_element_by_id("anony-nav")
# print(ret1)
# # 输出为：<selenium.webdriver.remote.webelement.WebElement (session="ea6f94544ac3a56585b2638d352e97f3", element="0.5335773935305805-1")>
# ret2 = driver.find_elements_by_id("anony-nav")
# print(ret2)
# # 输出为：[<selenium.webdriver.remote.webelement.WebElement (session="ea6f94544ac3a56585b2638d352e97f3", element="0.5335773935305805-1")>]
# ret3 = driver.find_elements_by_xpath("//*[@id='anony-nav']/h1/a")
# print(len(ret3))
# # 输出为：1
# ret4 = driver.find_elements_by_tag_name("h1")
# print(len(ret4))
# # 输出为：1
# ret5 = driver.find_elements_by_link_text("下载豆瓣 App")
# print(len(ret5))
# # 输出为：1
# ret6 = driver.find_elements_by_partial_link_text("豆瓣")
# print(len(ret6))
# # 输出为：24
#
# # driver.close() # 关闭当前的这个(一个)标签页
# driver.quit() # 完全退出模拟控制的浏览器！


# webrequest = webdriver.Chrome(r'./chromedriver')
# url = 'https://www.baidu.com'
# webrequest.get(url)

# 2\获取COOKIES方法
# dict_cookies={ i['name']:i['value'] for i in webrequest.get_cookies()}  获取多个cookies
# dict_cookie=webrequest.get_cookie('name')      获取指定一个


# 3\等待方法
    # 强制等待
# time.sleep(1)
#     隐式等待  最长等30
# webrequest.implicitly_wait(30)

#       显示等待  需要导入三个包
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
#
# driver=webdriver.Chrome('')
# driver.get(url)
# driver.implicitly_wait(30)
# emt=(By.LINK_TEXT,'查找内容')
# try:
#     WebDriverWait(driver,30,0.5).until(EC.presence_of_element_located(emt))
#     driver.find_element_by_link_text('查找内容').get_attribute('href')
# except:
#     pass
#
# finally:
#     driver.quit()

# 截图
# webrequest.save_screenshot('taobao.png')

# 4\selenium执行js代码
# js = 'window.scrollTo(0,document.body.scrollHeight)' # js语句     滑动最底部
# driver.execute_script(js) # 执行js的方法


# 5\switch方法切换的操作
# 5.1. 获取当前所有的窗口
# current_windows = driver.window_handles

# 5.2. 根据窗口索引进行切换
# driver.switch_to.window(current_windows[1])
# 5.3.
# iframe是html中常用的一种技术，即一个页面中嵌套了另一个网页，
# selenium默认是访问不了frame中的内容的，对应的解决思路是driver.switch_to.frame()
# login_frame = driver.find_element_by_id('login_frame') # 定位frame元素
# driver.switch_to.frame(login_frame) # 转向到该frame中
# driver.switch_to.alert() # 跟frame一样的处理方式！


# 6. 页面前进和后退
# driver.forward()     # 前进
# driver.back()        # 后退


# 关闭浏览器 、关闭标签页
# webrequest.quit()\close


# 7、无头浏览器适用场景服务器部署
# options=webdriver.ChromeOptions()
# options.set_headless()
# driver=webdriver.Chrome('./chromedriver',chrome_options=options)
# driver.get("https://www.baidu.com")
# driver.save_screenshot('baidu.png')
# driver.quit()
