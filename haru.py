def get_uia_root():
    import comtypes
    import comtypes.client

    comtypes.client.GetModule('UIAutomationCore.dll')

    # noinspection PyProtectedMember,PyUnresolvedReferences
    uia = comtypes.CoCreateInstance(comtypes.gen.UIAutomationClient.CUIAutomation._reg_clsid_,
                                    interface=comtypes.gen.UIAutomationClient.IUIAutomation,
                                    clsctx=comtypes.CLSCTX_INPROC_SERVER)

    desktop_element = uia.getRootElement()
    print(desktop_element.currentName)
    comtypes.CoUninitialize()

if __name__ == '__main__':
    get_uia_root()