# from airtest.core.api import *
from airtest.core.android.android import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
# # auto_setup(__file__)
adb = ADB()
devicesList = adb.devices()
# print(devicesList)
poco = AndroidUiautomationPoco(devices=[devicesList[0][0]], use_airtest_input=True, screenshot_each_action=False)
# poco.device.wake()
# import os,sys
# sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
# print(111111,sys.path)
