#-*-coding=utf8-*-
import time
from selenium import webdriver

driver = webdriver.Chrome('./chromedriver')
driver.get("https://mail.qq.com")
time.sleep(2)

# 切入frame标签中
time.sleep(2)
# 1.定位到frame标签
element = driver.find_element_by_id('login_frame')
# 2.切入
driver.switch_to.frame(element)

# 输入账号
time.sleep(2)
driver.find_element_by_id('u').send_keys('123456@qq.com')

# 输入密码
time.sleep(2)
driver.find_element_by_id('p').send_keys('cuowumima')

# 点击登录
time.sleep(2)
driver.find_element_by_id('login_button').click()

# 切出frame标签
time.sleep(4)
driver.switch_to.window(driver.window_handles[0])

# 检查是否切出成功
time.sleep(4)
content = driver.find_element_by_class_name('login_pictures_title').text
print(content)

driver.quit()