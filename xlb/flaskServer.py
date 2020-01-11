#!flask/bin/python
import os
import win32api
import win32process
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    # print('++++++ index')
    return "Hello, World!"


@app.route('/zyxx/api/v1.0/openCalculator1', methods=['GET'])
def open_calculator1():
    try:
        val = os.system("calc.exe")
        return "info1:{}".format(val)
    except Exception as ex:
        return "err1:{}".format(ex)


@app.route('/zyxx/api/v1.0/openCalculator2', methods=['GET'])
def open_calculator2():
    try:
        val = os.popen("calc.exe")
        return "info2:{}".format(val)
    except Exception as ex:
        return "err2:{}".format(ex)


@app.route('/zyxx/api/v1.0/openCalculator3', methods=['GET'])
def open_calculator3():
    try:
        val = os.startfile("calc.exe")
        return "info3:{}".format(val)
    except Exception as ex:
        return "err3:{}".format(ex)


@app.route('/zyxx/api/v1.0/openCalculator4', methods=['GET'])
def open_calculator4():
    try:
        val = win32api.ShellExecute(0, 'open', 'calc.exe', '', '', 1)
        return "info4:{}".format(val)
    except Exception as ex:
        return "err4:{}".format(ex)


@app.route('/zyxx/api/v1.0/openCalculator5', methods=['GET'])
def open_calculator5():
    try:
        val = win32process.CreateProcess(r'c:\windows\system32\calc.exe', '', None, None, 0, win32process.CREATE_NO_WINDOW, None, None, win32process.STARTUPINFO())
        return "info5:{}".format(val)
    except Exception as ex:
        return "err5:{}".format(ex)


if __name__ == '__main__':
    app.run(debug=True)