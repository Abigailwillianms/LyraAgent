from airtest.core.api import *
from airtest.core.win.win import *

connect_device(f"Windows:///?title_re=原神*")

key_press('W')

sleep(2)

key_release('W')

end = input("end")