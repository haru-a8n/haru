import comtypes

from comtypes import *
from comtypes.client import *

comtypes.client.GetModule('UIAutomationCore.dll')
from comtypes.gen.UIAutomationClient import *

uia = CoCreateInstance(CUIAutomation._reg_clsid_,
                       interface=IUIAutomation,
                       clsctx=CLSCTX_INPROC_SERVER)

desktop_element = uia.getRootElement()
print(desktop_element.currentName)
CoUninitialize()