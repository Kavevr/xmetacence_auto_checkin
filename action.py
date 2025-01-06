import random
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# 随机序列号
def range_serial_number(s, e):
    nums = []
    for i in range(s, e):
        nums.append(i)
    random_elements = random.sample(nums, len(nums))
    return random_elements


# 等待弹窗出现
def wait_new_window(driver, timeout=2):
    try:
        WebDriverWait(driver, timeout, 1).until(EC.new_window_is_opened((driver.window_handles,)))
        print(driver.window_handles)
    except TimeoutException:
        pass


# 延时输入
def delay_input(element: webdriver, text: str, delay_time: float = 0.2):
    for t in text:
        element.send_keys(t)
        time.sleep(delay_time)


def switch_to_window(driver, num):
    try:
        driver.switch_to.window(driver.window_handles[num - 1])
    except IndexError:
        print("Error: Maximum number of windows {}".format(len(driver.window_handles)))


# 点击
def click_element(driver, xpath, timeout=10):
    try:
        WebDriverWait(driver, timeout, 1).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        driver.find_element(By.XPATH, xpath).click()
    except ElementClickInterceptedException:
        print("当前元素不能被点击")
    except TimeoutException:
        print("等待超时")


# 获取元素
def get_element(driver, xpath, timeout=20):
    try:
        WebDriverWait(driver, timeout, 1).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        return element
    except NoSuchElementException:
        print("get_element: Not Found Such Element")
    except TimeoutException:
        pass


# 获取元素文本
def get_element_text(driver, xpath, timeout=4):
    try:
        WebDriverWait(driver, timeout, 1).until(EC.visibility_of_element_located((By.XPATH, xpath)))

        element_text = driver.find_element(By.XPATH, xpath).text
        return element_text
    except TimeoutException:
        return "没有找到元素文本"


# def input_form_send(driver, xpath, value):
#     get_element(driver, xpath).send_keys(value)

def get_driver_status(number):
    open_url = "http://127.0.0.1:50325/api/v1/browser/start?open_tabs=1&serial_number=" + str(number)
    while True:
        resp = requests.get(open_url).json()
        if resp["code"] == 0:
            print("当前浏览器ID: {}".format(number))
            return resp
            break
        else:
            print("启动失败: {}".format(number))
            print(resp)
            time.sleep(5)
            continue


def driver_init(number):
    resp = get_driver_status(number)
    chrome_driver = resp["data"]["webdriver"]
    service = Service(executable_path=chrome_driver)
    chrome_options = Options()

    chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # try:
    #     driver.maximize_window()
    # except WebDriverException:
    #     print("{} 请手动全屏".format(number))
    #     pass
    return driver
