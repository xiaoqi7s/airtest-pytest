from app.base import BasePage

class MY(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # ele元素事例

        #img图片事例
        self.e_invite_day_img = self("邀请页面日赚图片",'Template(r"tpl1576805695978.png", record_pos=(-0.246, -0.551), resolution=(720, 1280))')

        self._end = self()

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        return self

    def __getattribute__(self, attr):
        return super().__getattribute__(attr, __class__.__name__)

    def f_test3(self):
        print(333333333333)