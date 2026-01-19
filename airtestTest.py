from airtest.core.api import *

connect_device("Windows:///?title_re=红玫瑰 - 陈奕迅*")
image = snapshot("../../Documents/我的POPO/QwenAgent/QwenAgent/images/images01.jpg")
print(image)