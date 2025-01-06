from common.action import *
from random import randint


# 点击POST（发送）按钮
def send_post(driver):
    click_element(driver,
                  r'/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div['
                  r'2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/button[2]',  timeout=60)


def click_post_menu(driver):
    click_element(driver,
                  r'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/section/div/div/div['
                  r'1]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div/div[6]/div/div', timeout=100)
    time.sleep(randint(1, 2))


def get_twitter_first_post_url(driver, menu_option="home"):
    driver.get("https://twitter.com/")
    # 点击profile
    click_element(driver, r'//*[@id="targetElement"]/div[1]/div[2]/nav/a[9]', timeout=100)
    time.sleep(4.3)
    # 获取当前twitter用户名
    user_id = str(driver.current_url).split("/")[-1]
    print(user_id)
    time.sleep(randint(3, 5))
    if menu_option == "replies":
        # 点击replies
        click_element(driver,
                      r'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/nav/div/div['
                      r'2]/div/div[2]/a/div/div', timeout=100)
    elif menu_option == "home":
        # 点击home
        click_element(driver, r'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/nav/div/div['
                              r'2]/div/div[1]/a', timeout=100)
    time.sleep(randint(3, 5))
    #
    click_element(driver, r'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div['
                          r'3]/div/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div[2]/div/span['
                          r'1]', timeout=50)
    time.sleep(4)
    post_url = driver.current_url
    return post_url
