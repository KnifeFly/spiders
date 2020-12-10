import time
import requests
import hashlib

# js源码: c.appKey || ("waptest" === d.subDomain ? "4272" : "12574478")
# 如果是 waptest appkey则是4272 否则则是 12574478
APP_KEY="12574478"


def main():
    # 需要 时间戳 和 sign两个参数
    url = "https://h5api.m.taobao.com/h5/mtop.wdk.vertical.forms.itempagedetail.login/1.0/?jsv=2.5.1&appKey=12574478&t={}&sign={}&type=originaljson&dataType=json&timeout=5000"
    # 13位时间戳
    timestr = int(round(time.time() * 1000))
    # header头
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "accept": "application/json"
    }

    # 查询的产品信息
    post_data = """{"showSeries":true,"showSeriesTitle":false,"extParam":"false_20191219","bizChannel":"SG_HM_H5","source":"other","appName":"HEMA_H5","itemId":"591194199143","shopIds":"170165277,170165277","localShopIds":"170165277","poi":""}"""

    # 组装参数 得到sign
    arg = f"undefined&{timestr}&{APP_KEY}&{post_data}"
    sign = hashlib.md5(arg.encode()).hexdigest()

    # 第一次请求得到 _m_h5_tk 和 _m_h5_tk_enc 两个cookie
    resp = requests.post(url.format(timestr, sign), data={"data": post_data}, headers=headers)
    print(f"第一次请求: {resp.text}\n")

    # 需要从cookie的_m_h5_tk中得到token
    token=''
    for name, value in resp.cookies.items():
        if name == "_m_h5_tk":
            token = value.split("_")[0]


    # 再次得到时间戳
    timestr = int(round(time.time() * 1000))
    # 此次arg的第一个参数需要 token
    arg = f"{token}&{timestr}&{APP_KEY}&{post_data}"
    sign = hashlib.md5(arg.encode()).hexdigest()

    print(f"token: {token}\nsign: {sign}\n")

    # 再次请求得到数据返回
    resp = requests.post(url.format(timestr, sign), data={"data": post_data}, headers=headers, cookies=requests.utils.dict_from_cookiejar(resp.cookies))
    print(f"第二次请求: {resp.text}\n")

    
if __name__ == '__main__':
    main()