import comtypes

from comtypes import *
# noinspection PyUnresolvedReferences
from comtypes.client import *

comtypes.client.GetModule('UIAutomationCore.dll')
# noinspection PyUnresolvedReferences
from comtypes.gen.UIAutomationClient import *

# noinspection PyProtectedMember,PyUnresolvedReferences
uia = CoCreateInstance(CUIAutomation._reg_clsid_,
                       interface=IUIAutomation,
                       clsctx=CLSCTX_INPROC_SERVER)

desktop_element = uia.getRootElement()
print(desktop_element.currentName)
CoUninitialize()