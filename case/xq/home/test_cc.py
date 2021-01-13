from app.base import *
from app.pages import app

@allure.feature('玩转业务主流程')
class Test_XQ(object):
    #所有用例执行前执行一次
    def setup_class(self):
        self.curdir_time = str(int(time.time()))
        self.phone = '13412340004'
        self.code = '123456'

    # 每个用例之前都会执行
    def setup_method(self, method):
        stop_app("com.planet.light2345")
        start_app("com.planet.light2345")
        sleep(10)
        pass
        # time.sleep(10)

    # 每个用例之后都会执行
    def teardown_method(self, method):
        pass

    # 所有用例执行后执行一次
    def teardown_method(self):
        pass
    @allure.story('登录流程')
    @allure.link('www.baidu.com')
    @allure.title('用例1')
    @air_report
    def test_1(self):
        app.launch.e_phone_login_button.click()
        app.launch.e_phone_input.set_text(self.phone)
        app.launch.e_get_code.click()
        app.launch.e_code_input.adb_set_text(self.code)
        sleep(3)
        app.launch.e_my_tab.click()
        app.launch.e_my_invite.click()
        assert_exists(app.my.e_invite_day_img.img, "图片存在")



if __name__ =="__main__":
    os.system('pytest -s -q test_cc.py --alluredir ./../log/temp')
    os.system('allure generate ./../log/temp -o ./../log/report --clean')