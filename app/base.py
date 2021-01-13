#conding:utf-8
import os,sys,allure,re,types
from poco.proxy import UIObjectProxy
from poco.utils.query_util import build_query
from airtest.core.api import *
from airtest.report.report import simple_report
from config import log_path
from distutils.sysconfig import get_python_lib
from app import poco

pkdir = get_python_lib().lower()
rootpath = os.path.dirname(os.path.dirname(__file__)).replace('\\','/')
print('---',rootpath[2:])
class BasePage(UIObjectProxy):
    ttdict = {}
    def __init__(self, driver):
        self.temp = None
        # self._dict = None
        self.img = None
        self.step = None
        # self.f_methods = self.methods()
        self._dict = object.__getattribute__(self, '__dict__')
        super().__init__(driver)

    def three_click(self, focus=None, sleep_interval=None):
        focus = focus or self._focus or 'anchor'
        pos_in_percentage = self.get_position(focus)
        for i in range(0, 3):
            time.sleep(5)
            self.poco.pre_action('click', self, pos_in_percentage)
            ret = self.poco.click(pos_in_percentage)
            if sleep_interval:
                time.sleep(sleep_interval)
            else:
                self.poco.wait_stable()
            self.poco.post_action('click', self, pos_in_percentage)
        return ret

    def __call__(self, *args, **kwargs):
        if not self.temp:
            try:
                self.temp = args
            except:
                self.temp = kwargs
        key = list(self._dict.keys())[-1]
        if 'e_' in key:
            self.ttdict[key] = self.temp
            try:
                if kwargs:
                    self.temp = {}
                    self.temp['name'] = args[0]
                    self.temp['element'] = kwargs
                else:
                    self.temp = args
            except:
                self.temp = args
        return self

    def zt(self):
        pass

    def __getattribute__(self, attr, name):
        # 挡截 “e_” 和“_e_”的属性，“_e_”通常为BasePage的通用元素，加下横线用以区分
        if attr == '__dict__':
            return object.__getattribute__(self, '__dict__')
        if attr.startswith('e_') or attr.startswith('_e_'):
            if isinstance(self.ttdict[attr], dict):
                self._evaluated = False
                self.step = self.ttdict[attr]['name']
                self.query = build_query(None, **self.ttdict[attr]['element'])
                _proxy = self
            else:
                self.img = None
                self.step = self.ttdict[attr][0]
                if 'poco' in self.ttdict[attr][1]:
                    print(self.ttdict[attr][1] + '.query')
                    self._evaluated = False
                    self.query = eval(self.ttdict[attr][1] + '.query')
                    print(self.query)
                    # for i in self.f_methods:
                    #     print(f'_proxy.{i} = types.MethodType(self.{i},_proxy)')
                    #     exec(f'_proxy.{i} = types.MethodType(self.{i},_proxy)')
                    # for j in ['click', 'wait', 'set_text', 'exists']:
                    #     exec(f'_proxy.{j} = types.MethodType(self.{j}, _proxy)')
                    _proxy = self
                elif 'Template' in self.ttdict[attr][1]:
                    dir = os.path.dirname(__file__) + '\\' + name + '\images'
                    image_name = re.match('.*r"(.*).png',self.ttdict[attr][1])[1]
                    if os.path.exists(dir + '\\' + image_name + '.png'):
                        os.rename(dir + '\\' + image_name + '.png', dir + '\\' + self.step + '.png')
                    temp = self.ttdict[attr][1].replace(image_name, dir + '\\' + self.step)
                    self.img = eval(temp)
                    # self.step = self.ttdict[attr][0]
                    _proxy = self
                else:
                    self._evaluated = False
                    self.query = build_query(self.ttdict[attr][1])
                    _proxy = self
            return _proxy
        else:
            return object.__getattribute__(self, attr)

    # def methods(self):
    #     print(dir(self))
    #     return (list(filter(lambda m: m.startswith("f_") and callable(getattr(self, m)), dir(self))))

    def f_test1(self):
        print('this is test1')

    def adb_set_text(self, text):
        print(pkdir + f'\\airtest\core\\android\static\\adb\windows\\adb.exe shell input text {text}')
        os.system(pkdir + f'\\airtest\core\\android\static\\adb\windows\\adb.exe shell input text {text}')
        time.sleep(3)

    def click(self, times=1):
        if self.img:
            with allure.step(f'点击图片:{self.step}'):
                touch(self.img, times)
                self.img = None
        else:
            with allure.step(f'点击:{self.step}'):
                super().click()

    def wait(self, timeout = 3):
        if self.img:
            with allure.step(f'等待图片:{self.step}'):
                wait(self.img, timeout)
        else:
            with allure.step(f'等待元素:{self.step}'):
                super().wait(timeout)

    def exists(self):
        if self.img:
            with allure.step(f'判断图片存在:{self.step}'):
                exists(self.img)
        else:
            with allure.step(f'判断元素存在:{self.step}'):
                super().exists()

    def set_text(self, text):
        with allure.step(f'输入值:{text}'):
            super().set_text(text)

    def snapshot(self, filename=None, msg=""):
        with allure.step(f'截图'):
            snapshot(filename,msg)

    def keyevent(self, keyname, **kwargs):
        with allure.step(f'输入键盘按键码{keyname}'):
            keyevent(keyname, **kwargs)

    def swipe(self, *args):
        try:
            if isinstance(args[0],UIObjectProxy):
                # origin = self.get_position('anchor')
                super().swipe(args[0])
            else:
                try:
                    swipe(args[0],args[1])
                except:
                    if isinstance(args[0], Template):
                        swipe(self.img, args[0])
                    else:
                        pass
                    # origin = self.get_position('anchor')
        except:
            raise Exception("请传入有效的坐标或图片")

    def f_prings(self):
        print(1111111111111111)

def air_report(func):
    def _wrap(*args, **kwargs):
        curdir_time = str(int(time.time()))
        logdir = log_path + '\\' + curdir_time + '\\' + func.__name__
        os.makedirs(logdir)
        auto_setup(__file__, logdir=logdir, project_root=True)
        func(*args)
        logfile = logdir + f'\\{func.__name__}.html'
        simple_report(__file__, logpath=logdir, output=logfile)
        time.sleep(2)
        with open(logfile, 'r+', encoding='utf-8') as f:
            context = f.read()
            temp = context.replace(pkdir.replace('\\', '/') + '/airtest', 'http://172.17.12.8').replace(os.path.dirname(rootpath).replace('/','\\\\'), '')
        allure.attach(temp, 'report.html',attachment_type=allure.attachment_type.HTML)
    return _wrap

