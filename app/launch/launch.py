from app.base import BasePage

class Launch(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # ele元素事例
        self.e_agree_checkbox = self("同意勾选框", "com.planet.light:id/checkBox")
        self.e_get_code = self("获取短信验证码", "com.planet.light:id/btnBinding")
        self.e_agree_button = self("同意按钮", "com.planet.light:id/tv_confirm")
        self.e_my_invite = self("邀请好友按钮", 'poco("我的").child("android.widget.ListView")[1].child("android.view.View")[0]')
        self.e_phone_login_button = self("手机登录按钮", "com.planet.light:id/itemIconView")
        self.e_phone_input = self("手机号输入框", "com.planet.light:id/etPhone")
        self.e_code_input = self("验证码输入框", "com.planet.light:id/VerifyCodeEt")
        self.e_login_button = self("登录按钮", "com.planet.light:id/btnBinding")
        self.e_getcode_button = self("获取验证码按钮", "com.planet.light:id/btnPhoneSendBindCode")
        self.e_home_tab = self("首页", text="首页")
        self.e_my_tab = self("我的", 'poco("android:id/content").offspring("com.planet.light:id/bottom_tab_layout").child("android.view.View")[5].child("com.planet.light2345:id/icon")')

        #img图片事例
        self.e_phone_login_img = self("手机登录按钮图片", 'Template(r"tpl1576656754763.png", record_pos=(-0.001, 0.765), resolution=(720, 1280))')

        self._end = self()

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        return self

    def __getattribute__(self, attr):
        return super().__getattribute__(attr, __class__.__name__)

    def f_test3(self):
        print(333333333333)