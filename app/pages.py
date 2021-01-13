from app.launch.launch import Launch
from app.my.my import MY
from app import poco

class app:
    launch = Launch(poco)
    my = MY(poco)