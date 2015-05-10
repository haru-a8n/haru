import comtypes
import comtypes.client
import subprocess


class Robot(object):
    def __init__(self):
        super(Robot, self).__init__()
        self.proc = None

    def start(self, args):
        """
        Start an  application
        """
        self.proc = subprocess.Popen(args)


class Uia(object):
    def __init__(self):
        self.uia = None

    def __enter__(self):
        comtypes.client.GetModule('UIAutomationCore.dll')
        # noinspection PyProtectedMember,PyUnresolvedReferences
        self.uia = comtypes.CoCreateInstance(comtypes.gen.UIAutomationClient.CUIAutomation._reg_clsid_,
                                             interface=comtypes.gen.UIAutomationClient.IUIAutomation,
                                             clsctx=comtypes.CLSCTX_INPROC_SERVER)
        return self

    def root(self):
        return self.uia.getRootElement()

    def __exit__(self, exc_type, exc_val, exc_tb):
        comtypes.CoUninitialize()


if __name__ == '__main__':
    # with Uia() as uia:
    #     print(uia.root().currentName)
    robot = Robot()
    robot.start(['notepad'])