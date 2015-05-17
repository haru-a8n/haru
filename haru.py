"""
Haru Automation
Copyright (c) 2015 by Haru A8n (haru.a8n)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import comtypes
import comtypes.client
import ctypes
import string
import subprocess
import time

trace_on = True


class Logger(object):
    def __init__(self, trace):
        self.trace = trace

    def __call__(self, fn):
        if not self.trace:
            return fn

        from functools import wraps

        @wraps(fn)
        def wrapper(*args, **kwargs):
            code_path = '{0}.{1}'.format(args[0].__class__.__name__, fn.__name__)
            print('>{0}'.format(code_path))
            out = fn(*args, **kwargs)
            print('<{0}'.format(code_path))
            # Return the return value
            return out
        return wrapper


class CWindow(object):
    def __init__(self, trace=False, attr=None, parent=None, ae_init=False):
        """
        trace(True): Show log entry to most methods
        attr: attribute name used when called from __attr__
        parent: parent object
        ae_init(True): Initialization of Automation Element done at the subclass
        """
        assert not (attr is None)
        assert not (parent is None)

        self.parent = parent

        self.trace = trace
        super(CWindow, self).__init__()

        if ae_init:
            pass
        else:
            # This will try to match by name
            assert parent.element is not None, 'parent.element is None'
            ae = self.name_best_match(ae=parent.element, string_match=attr)

            if ae:
                self.element = ae
            else:
                # This is when creating object specifically called for a specific window
                windows = ['window', 'statusbar']
                if str(attr).lower() in windows and ae is None:
                    # This information gets used in __call__
                    self.element = self.parent.element
                else:
                    self.element = None

    def __getattr__(self, attr):
        # self.ShowTrace()
        if str(attr).lower() == 'combobox':
            obj = CComboBox(trace=self.trace, attr=attr, parent=self)
        elif str(attr).lower() == 'treeview':
            obj = CTreeView(trace=self.trace, attr=attr, parent=self)
        elif str(attr).lower() == 'listbox':
            obj = CListBox(trace=self.trace, attr=attr, parent=self)
        elif str(attr).lower() == 'listview':
            obj = CListView(trace=self.trace, attr=attr, parent=self)
        elif str(attr).lower() == 'edit':
            obj = CEdit(trace=self.trace, attr=attr, parent=self)
        elif str(attr).lower() == 'popupmenu':
            self.Click(self.element, button='right')
            obj = CPopupMenu(trace=self.trace, attr=attr, parent=self)
        else:
            obj = CWindow(trace=self.trace, attr=attr, parent=self)

        if obj.element:
            return obj
        else:
            raise AttributeError, attr

    # noinspection PyMethodMayBeStatic
    def best_match(self, str1, attr):
        """
        This will become a heuristic matching engine in the future
        """

        str1 = string.replace(str1, ' ', '')
        str1 = string.replace(str1, "'", "")
        str1 = str1.encode('ascii', 'ignore')
        if str(attr).lower() in str(str1).lower():
            return True
        else:
            return False

    def invoke(self):
        retry_interval = 0.5
        retry_max = 5
        loops = 0
        while True:
            try:
                if_invoke_pattern = self.element.GetCurrentPattern(comtypes.gen.UIAutomationClient.UIA_InvokePatternId)
                if_invoke = if_invoke_pattern.QueryInterface(comtypes.gen.UIAutomationClient.IUIAutomationInvokePattern)
                if_invoke.invoke()
                break
            except:
                print 'Retrying invoke...'
                time.sleep(retry_interval)
                loops += 1
                if loops > retry_max:
                    raise
    click = invoke

    @Logger(trace_on)
    def name_best_match(self, ae=None, string_match=''):
        assert ae, 'AE object None'

        cvw = Uia().uia.ControlViewWalker
        ae = cvw.GetFirstChildElement(ae)
        print('string_match:', string_match)
        while ae:
            print '-'*10
            print 'Name: ', ae.CurrentName
            print 'LocalizedControlType:', ae.CurrentLocalizedControlType
            print 'ClassName: ', ae.CurrentClassName
            if self.best_match(ae.CurrentClassName, string_match):
                break
            elif ae.CurrentName is not None and self.best_match(ae.CurrentName, string_match):
                break
            ae = cvw.GetNextSiblingElement(ae)

        # Don't need to assert of None, we need to check using other mechanism
        return ae


class CEdit(CWindow):
    """ Edit control """

    def __init__(self, attr=None, parent=None):
        super(CEdit, self).__init__(attr=attr, parent=parent)

        # This is when creating object specifically called for CEdit
        if str(attr).lower() == 'edit' and self.element is None:
            self.element = parent.element  # this is not the correct element, will be corrected in __call__

    def type(self, value):
        self.element.SetFocus()
        if bool(self.element.GetCurrentPropertyValue(
                comtypes.gen.UIAutomationClient.UIA_IsValuePatternAvailablePropertyId)):
            if_value_pattern = self.element.GetCurrentPattern(comtypes.gen.UIAutomationClient.UIA_ValuePatternId)
            val = if_value_pattern.QueryInterface(comtypes.gen.UIAutomationClient.IUIAutomationValuePattern)
            val.SetValue(value)
        else:
            assert "no type/sendkeys handler"
            # swf.SendKeys.SendWait( sValue )


class CMenuBar(CWindow):
    """ Menu Bar - legacy applications manipulate Menu/MenuItems.
    This specialized window will handle those cases.
    """

    def __init__(self, attr=None, parent=None):
        assert attr, 'attr is None'
        assert parent, 'parent is None'
        self.parent = parent
        super(CMenuBar, self).__init__(attr=attr, parent=parent)

    def __getattr__(self, attr):
        # self.parent.proc.WaitForInputIdle()
        self.parent.wait_for_input_idle()

        obj = CMenuItem(attr=attr, parent=self)
        if obj.element:
            obj.ae_main = self.parent.element
            return obj
        else:
            raise AttributeError(attr)


class CMenuItem(CWindow):
    """ Menu Item """

    def __init__(self, attr=None, parent=None):
        super(CMenuItem, self).__init__(attr=attr, parent=parent)
        # On platform win32 (vs WPF), Menubar's automation element parent is the main window.
        # Each submenu's parent is the main window
        if isinstance(parent, CMenuBar):
            cond = Uia().uia.CreatePropertyCondition(comtypes.gen.UIAutomationClient.UIA_NamePropertyId, attr)
            ae = self.parent.element.FindFirst(scope=comtypes.gen.UIAutomationClient.TreeScope_Children, condition=cond)
            self.click()

            # noinspection PyPep8Naming
            ExpandCollapseState_Expanded = 1  # enum ExpandCollapseState
            while ae.GetCurrentPropertyValue(
                    comtypes.gen.UIAutomationClient.UIA_ExpandCollapseExpandCollapseStatePropertyId) != \
                    ExpandCollapseState_Expanded:
                print('Waiting for {} to expand--@{}'.format(parent.element.CurrentName, time.asctime()))
                time.sleep(0.1)
        else:
            # First call will get the main menu, e.g. File
            cond = Uia().uia.CreateTrueCondition()
            ae = parent.ae_main.FindFirst(comtypes.gen.UIAutomationClient.TreeScope_Descendants,
                                          cond)
            # This will get the sub menu, e.g., File | Exit
            cvw = Uia().uia.ControlViewWalker
            ae = cvw.GetFirstChildElement(ae)
            while ae:
                if self.best_match(ae.CurrentName, attr):
                    break

                ae = cvw.GetNextSiblingElement(ae)
            self.menu_main = self.parent
        self.element = ae
        self.parent = parent
        self.ae_main = self.parent.ae_main

    def __getattr__(self, attr):
        obj = CMenuItem(attr=attr, parent=self)
        if obj.element:
            return obj
        else:
            raise AttributeError(attr)

    def is_checked(self):
        checked = False

        if bool(self.element.GetCurrentPropertyValue(
                comtypes.gen.UIAutomationClient.UIA_IsTogglePatternAvailablePropertyId)):
            # noinspection PyPep8Naming
            ToggleState_On = 1
            if self.element.GetCurrentPropertyValue(comtypes.gen.UIAutomationClient.UIA_ToggleToggleStatePropertyId) == \
                    ToggleState_On:
                checked = True
        print(dir(self.ae_main))
        self.ae_main.click()
        #This will close the menus, and just in case it is really deep menu we send 5 esc
        #swf.SendKeys.SendWait( 5*'{ESC}' )

        return checked


class MainWindow(CWindow):
    """Represents the main window"""
    def __init__(self, attr=None, parent=None):

        assert not (parent is None)
        self.parent = parent
        self.attr = attr
        self.uia = Uia()
        i_loop = 0
        while True:
            print('pid : {}'.format(parent.proc.pid))
            cond = self.uia.uia.CreatePropertyCondition(comtypes.gen.UIAutomationClient.UIA_ProcessIdPropertyId,
                                                        parent.proc.pid)
            print('getting ae')
            ae = self.uia.root().FindFirst(scope=comtypes.gen.UIAutomationClient.TreeScope_Children, condition=cond)

            if ae:
                print('we have ae')
                break
            else:
                print 'Main window not there yet, retrying... @%s'%time.asctime()
                time.sleep( 0.1 )
                i_loop += 1
                if i_loop >= 5:
                    print 'Giving up on trying to get main window...%s'%time.asctime()
                    break
        self.element = ae

        super(MainWindow, self).__init__(attr=attr, parent=parent, ae_init=True)

    def __getattr__(self, attr):
        if attr.lower() == 'menu':  # match main menu
            cond = self.uia.uia.CreatePropertyCondition(comtypes.gen.UIAutomationClient.UIA_ControlTypePropertyId,
                                                        comtypes.gen.UIAutomationClient.UIA_MenuBarControlTypeId)
            ae = self.element.FindFirst(scope=comtypes.gen.UIAutomationClient.TreeScope_Children, condition=cond)
            assert ae is not None
            if ae:
                obj = CMenuBar(attr=attr, parent=self)
                obj.element = ae
                obj.ae_main = self.element
        elif attr.lower() == 'edit':
            obj = CEdit(attr=attr, parent=self)
        else:
            print('Generic windows : {}'.format(attr))
            obj = super(MainWindow, self).__getattr__(attr)

        if obj.element:
            return obj
        else:
            raise AttributeError, attr

    @Logger(trace_on)
    def close(self):
        # http://weichong78.blogspot.com/2013/11/python-com-and-windows-uiautomation.html
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ee671195(v=vs.85).aspx
        pattern = self.element.GetCurrentPattern(comtypes.gen.UIAutomationClient.UIA_WindowPatternId)
        if_window_pattern = pattern.QueryInterface(comtypes.gen.UIAutomationClient.IUIAutomationWindowPattern)
        if_window_pattern.Close()

    def maximize(self):
        pattern = self.element.GetCurrentPattern(comtypes.gen.UIAutomationClient.UIA_WindowPatternId)
        if_window_pattern = pattern.QueryInterface(comtypes.gen.UIAutomationClient.IUIAutomationWindowPattern)
        # noinspection PyPep8Naming
        WindowVisualState_Maximized = 1
        if if_window_pattern.CurrentWindowVisualState != WindowVisualState_Maximized:
            if_window_pattern.SetWindowVisualState(WindowVisualState_Maximized)

    def wait_for(self, object_type=None, caption=None, timeout=-1, wait_interval=0.1):
        """
        ObjType: Type of object ['dialog']
        Caption: Caption of the object
        timeout: (seconds). -1 wait forever
        waitInterval: (seconds). Time delay between retrying to to check for the object.
        """
        time_start = time.time()
        if str(object_type).lower() == 'dialog':
            while 1:
                cond = self.uia.uia.CreatePropertyCondition(comtypes.gen.UIAutomationClient.UIA_NamePropertyId,
                                                            caption)
                ae = self.element.FindFirst(scope=comtypes.gen.UIAutomationClient.TreeScope_Children, condition=cond)
                if ae is None:
                    #print ">>> Waiting @%s"%time.asctime()
                    time.sleep(waitInterval)
                else:
                    break
                if timeout != -1:
                    if timeout < time.time() - time_start:
                        raise TimeOutError
        else:
            raise DebuggingForcedError

    # noinspection PyMethodMayBeStatic,PyPep8Naming
    def wait_for_input_idle(self):
        WaitForInputIdle = ctypes.windll.user32.WaitForInputIdle
        OpenProcess = ctypes.windll.kernel32.OpenProcess
        PROCESS_QUERY_INFORMATION = 1024
        hwnd_process = OpenProcess(PROCESS_QUERY_INFORMATION, 0, self.parent.proc.pid)
        ret = WaitForInputIdle(hwnd_process, -1)


class Robot(object):
    def __init__(self):
        super(Robot, self).__init__()
        self.proc = None

    @Logger(trace_on)
    def start(self, args):
        """
        Start an  application
        """
        self.proc = subprocess.Popen(args)

    def __getattr__(self, attr):
        obj = MainWindow(attr=attr, parent=self)
        if obj.element:
            return obj
        else:
            raise AttributeError(attr)


class Singleton(object):
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass


class Uia(Singleton):
    def __init__(self):
        print('Initializing UIA COM')
        comtypes.client.GetModule('UIAutomationCore.dll')
        # noinspection PyProtectedMember,PyUnresolvedReferences
        self.uia = comtypes.CoCreateInstance(comtypes.gen.UIAutomationClient.CUIAutomation._reg_clsid_,
                                             interface=comtypes.gen.UIAutomationClient.IUIAutomation,
                                             clsctx=comtypes.CLSCTX_INPROC_SERVER)

    def root(self):
        return self.uia.getRootElement()


if __name__ == '__main__':
    robot = Robot()
    robot.start(['notepad'])
    notepad = robot.Notepad
    notepad.edit.type("hello")
    notepad.close()
    notepad.wait_for(object_type='dialog', caption='Notepad')
    # notepad.Notepad.DontSave.invoke()
    notepad.Notepad.DontSave.click()