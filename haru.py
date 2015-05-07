import comtypes
import comtypes.client


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
    with Uia() as uia:
        print(uia.root().currentName)
