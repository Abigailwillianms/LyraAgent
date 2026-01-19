from airtest.core.api import *

connect_device("Windows:///?title_re=Never Gonna Give You Up - Rick Astley*")
image = snapshot("./images/images01.jpg")
print(image)