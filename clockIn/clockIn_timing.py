import json
import os
import time

import schedule

import req_model


def main(js: json):
    last_msg = None
    for i in range(3):
        time.sleep(i * 5)
        try:
            if js["username"] != "" and js["password"] != "":
                msg = req_model.upload(js["username"], js["password"])
                if msg == "":
                    req_model.push_msg("[BUPT Covid] Failed to clock in at {}: unknown error".format(time.strftime("%H:%M")), js)
                elif json.loads(msg)["m"] == "今天已经填报了":
                    title = "BUPT Covid: SUCCEED"
                    msg = "{} already clocked in today.".format(js['username'])
                    print(msg)
                    req_model.push_msg(title, js, msg)
                    return
                elif json.loads(msg)["m"] == "操作成功":
                    title = "BUPT Covid: SUCCEED"
                    msg = "Succeed to clock in for {} at {}.".format(js['username'], time.strftime("%H:%M"))
                    print(msg)
                    req_model.push_msg(title, js, msg)
                    return
                else:
                    print(time.strftime("%H:%M") + " " + json.loads(msg)["m"])
                    req_model.push_msg(time.strftime("%H:%M") + " " + json.loads(msg)["m"], js)
        except Exception as e:
            last_msg = e
    title = "BUPT Covid: FAILED"
    msg = "Failed to clock in for {}, caused by: {}.".format(js["username"], last_msg)
    req_model.push_msg(title, js, msg)
            


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
        data = json.load(f)
    for item in data:
        # do it now
        main(data[item])
        schedule.every().day.at(data[item]["time"]).do(main, data[item])
    while 1:
        time.sleep(1)
        schedule.run_pending()
