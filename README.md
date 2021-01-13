# 写在前面

1，需要有一点python基础，因为使用了pytest和airtest,所以这两者需要有一点了解。

# 工程简介

1，框架采用python语言编写，结合pytest+airtest+allure组成，编辑工具采用pycharm。

2，支持用例编写，单文件存放多条用例，因pytest特性，文件及用例需要以test_开头或结尾。

3，结合airtest中工具特性，用例支持原生控件，元素，h5元素及图像识别检查。

4，用例执行，单条，批量执行，特定标签分类执行。

5，利用allure及airtest原始报告组成html报告。


# 安装说明
1，python --推荐使用3.6.5版本，安装略。

2，jdk1.8+ --下载地址：https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html 注意配置java_home及path。

3，airtest --支持windows和mac版本。下载地址：http://airtest.netease.com/changelog.html 解压之后在相应目录可以直接启动。

4，allure --下载地址：https://github.com/allure-framework/allure2/releases 需要讲bin目录添加到path中。

5，另python的依赖库见工程中的requestments.txt，安装命令：pip install -r requestments.txt。


# 工程目录结构介绍

    |                                           # 根目录
    ├─app                                       # 元素及方法层
    │  │  base.py                               #页面逻辑支撑方法文件。非常重要，但不需要关注
    │  │  pages.py                              #*重要*整体整合页面，新增页面目录之后，需要在该目录下增加对应页面信息
    │  ├─launch                                 # 单个页面目录
    │  │  │  launch.py                          # *重要*  元素存放位置，该页面对应元素放在该文件下，该页面相关的方法存在位置。
    │  │  └─images                              # 页面对应包含的相关图片
    │  │          手机登录按钮图片.png
    └─case                                      #用例层
        └─xq                                    #用例对应模块
            ├─home                              #可细分模块，可有可无
            │      test_cc.py                   #*重要*具体用例文件，需要以test_开头或结尾
            │
            └─log
                ├─1576836879
                    ├─test_1
                        xxx.html                #用例1对应的airtest的html报告   暂时不用关注
                ├─report
                    index.html                  #*重要*allure生成的报告文件目录主文件，需要在pycharm中打开，本地打开无法访问
                ├─temp                          #日志产生需要的临时文件 暂时不用关注

   项目整体说明：
   
   1，新建页面元素，在app目录下复制页面目录launch，然后修改名称为对应名称xxx和xxx.py,图片目录名称就叫images就好。主要page页面中目录需要和文件名相同。即launch和launch.py
    
   2，在pages.py中增加from app.launch.launch import Launch 及 launch = Launch(poco)
    
   3, 使用时，首先在新建的xxx.py文件中填入对应页面的元素。写到对应对应.py文件中类的__init__方法的self.end前面即可。因为ui识别工具采用的是pocoui,所以元素信息
    
   需要符合它的特性，支持以下4种写法，具体元素怎么获取，可以参考airtest的使用教程。http://airtest.netease.com/ 推荐前2着写法，因为比较简洁。追求的方便的朋友也可以采用方式3
  
   的写法，另外图片目前只支持第4种的写法。
  
   #   1) self.e_agree_checkbox = self("同意勾选框", "com.planet.light2345:id/checkBox")
        
   #   2) self.e_home_tab = self("首页", text="首页")
        
   #   3) self.e_my_invite = self("邀请好友按钮", 'poco("我的").child("android.widget.ListView")[1].child("android.view.View")[0]')
        
   #   4) self.e_phone_login_img = self("手机登录按钮图片", 'Template(r"tpl1576656754763.png", record_pos=(-0.001, 0.765), resolution=(720, 1280))')
        
   注：元素编写时，前面为元素变量名，需要以e_开头，后面尽量用简短的单词说明元素含义，如是按钮的可以带上button,tab的可以带上tab，图片可以带上img等，值为self("元素描述"，"元素信息")。
      
   4，元素填写完毕之后，就可以开始写用例了。在对应test_xx.py文件中书写。
    
# 用例示例说明：

    from app.base import *
    from app.pages import app                                       #base和pages是基础支持，需要引入

    @allure.feature('玩转业务主流程')                                  #allure为了让报告好看，所以需要加一些中文描述。class前面的allure.feature为用例组的描述信息。
    class Test_XQ(object):                                           #测试类，需要以Test_开头
        #所有用例执行前执行一次
        def setup_class(self):
            self.curdir_time = str(int(time.time()))
            self.phone = '13412340004'
            self.code = '123456'

        # 每个用例之前都会执行
        def setup_method(self, method):
            # stop_app("com.planet.light2345")                        #这4个方法左侧已有说明，以具体使用场景可能会用到。目前setup_method，每个用例应该都需要有一段公共逻辑需要执行
            # start_app("com.planet.light2345")
            # sleep(10)
            pass
            # time.sleep(10)

        # 每个用例之后都会执行
        def teardown_method(self, method):
            pass

        # 所有用例执行后执行一次
        def teardown_method(self):
            pass

        @allure.story('登录')                                         #allure.story给用例名称增加描述
        @air_report                                                   @air_report 必须要写，生成报告的工具
        def test_1(self):                                             #真正的用例部分，需要以test_开头
            app.launch.e_phone_login_button.click()                   #用例正文，常用的方法，click，set_text等。
            app.launch.e_phone_input.set_text(self.phone)
            app.launch.e_get_code.click()
            app.launch.e_code_input.adb_set_text(self.code)
            sleep(3)

        @allure.story('检验')                                         #用例2同上。
        @air_report
        def test_2(self):
            app.launch.e_my_tab.click()
            app.launch.e_my_invite.click()
            assert_exists(app.my.e_invite_day_img.img, "图片存在")



    if __name__ =="__main__":
        os.system('pytest -s -q test_cc.py --alluredir ./../log/temp')    #用例执行相关，因为pytest主要还是靠命令行执行。命令见左侧两行，这里只是为了方便调试。注意带文件名为执行指定文件，不带为全部。
        os.system('allure generate ./../log/temp -o ./../log/report')     #命令行生成allure报告
        
# 其他说明

   pycharm对pytest的运行设置, file->settings->Tools->python intergrated tools->testing中选择pytest。可以支持运行单条case