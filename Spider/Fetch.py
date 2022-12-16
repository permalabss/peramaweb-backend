# coding gbk
# -*-utf-8-*-
# PaNews
import time

from selenium import webdriver
from selenium.webdriver import Chrome

# from Spider.Foresightnews import getpage

json_list =[]


from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/health', methods=["GET"])
def health():
    return "ok"

@app.route('/fetchurl', methods=["GET"])
def fetchHtml():
    params = request.args
    url = params.get('url')
    prefs = {"profile.managed_default_content_settings.images": 2,
             "profile.managed_default_content_settings.javascript": 1,
             'permissions.default.stylesheet': 2}
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    driver = Chrome(options=options)
    try:
        driver.get(url)
        # 页面所有源码
        time.sleep(10)
        js_height = "return document.body.clientHeight"
        height = driver.execute_script("return document.body.clientHeight")
        k = 1
        while True:
            if k * 500 < height:
                js_move = "window.scrollTo(0,{})".format(k * 500)
                print(js_move)
                driver.execute_script(js_move)
                time.sleep(0.05)
                height = driver.execute_script(js_height)
                k += 1
            else:
                break
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        result = driver.get_screenshot_as_base64()
        res = {"result": result}
        return jsonify(res)
    finally:
        driver.quit()
# # 获取网页源代码
#     r = requests.get('url')
#
# # 将网页源代码转换为BeautifulSoup对象
#     soup = BeautifulSoup(r.text, 'html.parser')
#
# # 获取渲染后的HTML页面
#     return soup.prettify()

# if __name__ == '__main__':
#     print(fetchHtml(sys.argv[1]))

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            threaded=True,
            debug=False,
            port=8868)