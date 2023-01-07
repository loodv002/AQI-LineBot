# About code and module
- Update lambda function
  - main function: grab.py
  - dependency: config.py
  - module: json, requests*, psycopy2*

- Schedule lambda function
  - main function: schedule.py
  - dependency: utils.py, config.py, db.py, model.py
  - module: linebot*, datetime, sqlalchemy*, pyimgur*

- LineBot lambda function
  - main function: linebot.py
  - dependency: utils.py, config.py, db.py, model.py, reply.py
  - module: linebot*, datetime, sqlalchemy*, pyimgur*, re, matplotlib*

- Modules with * sign behind are not build-in modules.
- Modules above does not include their dependencies, such as numpy.
# About data
- Data are request from "https://data.epa.gov.tw/api/v2/aqx_p_432",
  you can also view them in "https://data.gov.tw/dataset/40448".
