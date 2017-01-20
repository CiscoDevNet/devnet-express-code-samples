import platform
import pip
import subprocess


def os_system():

    platform_name = platform.system()
    if platform_name == "Windows":
        return "Windows"
    elif platform_name == "Linux":
        return "Linux"
    else:
        return "MacOS"


def check_py():

    if os_system() == "Windows":
        try:
            py_ver = subprocess.check_output(
                "py -3 -V").decode('UTF-8').splitlines()[0]
            print("Script has detected " + py_ver +
                  " version present on the machine.")
        except:
            print("Script could not detect Python 3 on the machine.\n"
                  "Go to https://www.python.org/downloads/ page and download latest Python 3 version.")
    else:
        try:
            py_ver = subprocess.check_output(["python3", "-V"]).decode('UTF-8').splitlines()[0]
            print("Script detected " + py_ver +
                  " version present on the machine.")
        except:
            print("Script could not detect Python 3 on the machine.\n"
                  "Go to https://www.python.org/downloads/ page and download latest Python 3 version.")


def check_modules():

    necessary_modules = ["requests", "ncclient", "netaddr", "pyang"]
    installed_packages_list = sorted(["%s" % (i.key)
                                      for i in pip.get_installed_distributions()])

    for module in necessary_modules:
        if module in installed_packages_list:
            print("You have \"" + module +
                  "\" module installed on your local machine!")
        else:
            print("\n\nLooks like you are missing an important module!\n")
            print('Open your terminal screen and type pip install ' + module)


def main():

    check_py()
    check_modules()

if __name__ == "__main__":
    main()
