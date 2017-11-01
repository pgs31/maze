import os

os.chdir(r"h:\maze")
users = "wuhyun1120 TorbenSell ChristopherDesira"

for user in users.split():
    if not os.path.exists(user):
        cmd = "git clone git://github.com/{}/maze {}".format(user, user)
    else:
        cmd = "cd {} && git pull".format(user)
    print(cmd)
    os.system(cmd)
