# Reference: https://pypi.org/project/sxtwl/

Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ShX = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
numCn = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏",
     "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑","白露", "秋分", "寒露", "霜降", 
     "立冬", "小雪", "大雪"]
ymc = ["十一", "十二", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十" ]
rmc = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", 
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", 
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]
XiZ = ['摩羯', '水瓶', '双鱼', '白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手']
WeekCn = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]

import  sxtwl
from quart import Quart, request
import quart, quart_cors
import json, requests



# 从年月日时获得四柱八字，缺点：还计算经度对真太阳时带来的影响
def getBazi(year, month, day, hour, min=0, sec=0):
    date = sxtwl.fromSolar(year, month, day)
    yTG = date.getYearGZ()
    yPillar = Gan[yTG.tg] + Zhi[yTG.dz]
    mTG = date.getMonthGZ()
    mPillar = Gan[mTG.tg] + Zhi[mTG.dz]
    dTG  = date.getDayGZ()
    dPillar = Gan[dTG.tg] + Zhi[dTG.dz]
    sTG = date.getHourGZ(hour)
    sPillar = Gan[sTG.tg] + Zhi[sTG.dz]
    result_data = {
        'year_tg' : yTG.tg+1,
        'year_dz' : yTG.dz+1,
        'month_tg' : mTG.tg+1,
        'month_dz' : mTG.dz+1,
        'day_tg' : dTG.tg+1,
        'day_dz' : dTG.dz+1,
        'hour_tg' : sTG.tg+1,
        'hour_dz' : sTG.dz+1,
        'bazi' : yPillar + mPillar + dPillar + sPillar
        }
    return result_data


app = quart_cors.cors(Quart(__name__), allow_origin="https://chat.openai.com")
HOST_URL = "https://oc.ag1.pro"

@app.post('/bazi')
async def bazi():
    data = await request.get_json()
    year = data.get('year')
    month = data.get('month')
    day = data.get('day')
    hour = data.get('hour')
    min = data.get('min', 0)
    sec = data.get('sec', 0)

    bazi_result = getBazi(year, month, day, hour, min, sec)
    body = {
        'input': data,
        'result': bazi_result}
    
    print(body)

    return quart.Response(response=json.dumps(body), status=200)

@app.get("/test")
async def test():
    host = request.headers['Host']
    text = f"Hello from {host}!"
    return quart.Response(text, mimetype="text/plain")

@app.get("/players")
async def get_players():
    query = request.args.get("query")
    res = requests.get(
        f"{HOST_URL}/test")
    body = res.json()
    return quart.Response(response=json.dumps(body), status=200)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=443, 
            certfile='/home/ubuntu/certs/ag1.pro_cert.pem', 
            keyfile='/home/ubuntu/certs/ag1.pro_key.key',
            ca_certs='/home/ubuntu/certs/ag1.pro_cert_chain.pem'
            )