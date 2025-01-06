import time

from common.action import *

metamask_url = "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#unlock"
password_el = r'//*[@id="password"]'
button_el = r'//*[@id="app-content"]/div/div[2]/div/div/button'
switchChain_el = r'//*[@id="app-content"]/div/div[2]/div/div[1]/button'
test_button_el = r'/html/body/div[3]/div[3]/div/section/div[4]/label'


# metamask登录

def metamask_login(driver, password: str):
    driver.get(metamask_url)
    click_element(driver, password_el, timeout=10)
    try:
        input_text = get_element(driver, password_el)
        delay_input(input_text, password, 0)
        click_element(driver, button_el)
    except AttributeError:
        pass


# 切换网络
def switch_chain(driver, chain_name: str):
    driver.get(metamask_url)
    time.sleep(4)
    # 切换网络按钮
    click_element(driver, switchChain_el, timeout=6)
    # 查询当前有多少条链
    net_els = driver.find_elements(By.CSS_SELECTOR,
                                   r'body > div.mm-modal > div:nth-child(3) > div > section > '
                                   r'div.mm-box.multichain-network-list-menu > div > div')
    chains = len(net_els)
    # print(chains)
    # 获取网络的点击位置
    buttons_name = {}
    time.sleep(3)
    # 获取网络名称
    for index in range(chains):
        index += 1
        button_element = "body > div.mm-modal > div:nth-child(3) > div > section > " \
                         "div.mm-box.multichain-network-list-menu > div > div:nth-child({}) > div".format(str(index))
        name_element = "body > div.mm-modal > div:nth-child(3) > div > section > " \
                       "div.mm-box.multichain-network-list-menu > div > div:nth-child({}) > div > " \
                       "div.mm-box.multichain-network-list-item__network-name.mm-box--display-flex.mm-box--align" \
                       "-items-center > p".format(str(index))
        try:
            name = driver.find_element(By.CSS_SELECTOR, name_element)
            # print("ID {}: {}".format(index - 1, name.text))
            button = driver.find_element(By.CSS_SELECTOR, button_element)
            buttons_name[name.text] = button
        except NoSuchElementException:
            pass

    if chain_name in buttons_name:
        buttons_name[chain_name].click()
        print(chain_name)
    else:
        print("Switch Chain Failed")


def get_wallet_address(driver):
    driver.get(metamask_url)
    click_element(driver, r'//*[@id="app-content"]/div/div[2]/div/div[3]/div/div/button')
    click_element(driver, r'//*[@id="app-content"]/div/div[2]/div/div[3]/div[2]/button[1]')
    address = get_element(driver, r'/html/body/div[3]/div[3]/div/section/div/div/div[2]/div[2]/div/div/button/span['
                                  r'1]/div').text
    return address


# 获取当前网络的代余额
def get_current_chain_token(driver, token_xpath):
    driver.get(metamask_url)
    click_element(driver, r'//*[@id="app-content"]/div/div[3]/div/div/div/div[2]/div/ul/li[1]/button', timeout=30)
    try:
        balance = driver.find_element(By.XPATH, token_xpath).text
        return balance
    except NoSuchElementException:
        print("获取元素文本失败")


def okx_wallet_switch(driver, status):
    try:
        driver.get("chrome://extensions/")
        time.sleep(0.8)
        host = get_element(driver, r'/html/body/extensions-manager')
        life = driver.execute_script('return document.querySelector("body > '
                                     'extensions-manager").shadowRoot.querySelector('
                                     '"#items-list").shadowRoot.querySelector('
                                     '"#mcohilncbfahbmgdjkbpemcciiolgcge").shadowRoot.querySelector('
                                     '"#enableToggle").getAttribute("aria-pressed")', host)
        # print(life)
        if status == "on":
            if life == "false":
                driver.execute_script('''document.querySelector("body > extensions-manager").shadowRoot.querySelector(
                "extensions-item-list").shadowRoot.querySelector("#mcohilncbfahbmgdjkbpemcciiolgcge").shadowRoot.querySelector(
                "#enableToggle").click()''', host)
        elif status == "off":
            if life == "true":
                driver.execute_script('''document.querySelector("body > extensions-manager").shadowRoot.querySelector(
                  "extensions-item-list").shadowRoot.querySelector("#mcohilncbfahbmgdjkbpemcciiolgcge").shadowRoot.querySelector(
                  "#enableToggle").click()''', host)
        time.sleep(1)
    except NoSuchElementException:
        print("{} failed".format(status))
