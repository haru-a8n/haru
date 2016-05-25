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
from lib.SendKeysCtypes import SendKeys
import lib.win32functions as win32functions
import lib.win32defines as win32defines
import lib.win32structures as win32structures
from lib.timings import Timings
import string
import subprocess
import time

trace_on = True


class TimeOutError(Exception):
    """ Timeout exception error"""
    pass


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
    def __init__(self, attr=None, parent=None, ae_init=False):
        """
        trace(True): Show log entry to most methods
        attr: attribute name used when called from __attr__
        parent: parent object
        ae_init(True): Initialization of Automation Element done at the subclass
        """
        assert attr
        assert parent

        self.parent = parent

        super(CWindow, self).__init__()

        if ae_init:
            pass
        else:
            print('need to init')
            # This will try to match by name
            assert parent.element is not None, 'parent.element is None'
            ae = self.name_best_match(ae=parent.element, string_match=attr)

            if ae:
                self.element = ae
            else:
                # This is when creating object specifically called for a specific window
                print('attr is.... {}'.format(attr))
                windows = ['window', 'statusbar']
                if str(attr).lower() in windows:
                    print('set parent')
                    # This information gets used in __call__
                    # print('statusbar here')
                    self.element = self.parent.element
                else:
                    print('else')
                    self.element = None

    def __getattr__(self, attr):
        # self.ShowTrace()
        if str(attr).lower() == 'combobox':
            obj = CComboBox(attr=attr, parent=self)
        elif str(attr).lower() == 'treeview':
            obj = CTreeView(attr=attr, parent=self)
        elif str(attr).lower() == 'listbox':
            obj = CListBox(attr=attr, parent=self)
        elif str(attr).lower() == 'listview':
            obj = CListView(attr=attr, parent=self)
        elif str(attr).lower() == 'edit':
            obj = CEdit(attr=attr, parent=self)
        elif str(attr).lower() == 'popupmenu':
            self.click(ae=self.element, button='right')
            obj = CPopupMenu(attr=attr, parent=self)
        else:
            print('Generic window')
            obj = CWindow(attr=attr, parent=self)

        if obj.element:
            return obj
        else:
            print(self.element.CurrentClassName)
            print(type(self))
            raise AttributeError(attr)

    def __call__(self, **kwargs):
        if len(kwargs) == 0:
            return self
        else:
            assert self.parent.element, 'Parent AE object None'
            ae = self.get_child_element(ae_parent=self.parent.element, **kwargs)

            assert ae, 'Automation element object None'
            self.element = ae
            return self

    # noinspection PyMethodMayBeStatic
    def __get_supported_properties(self, ae):
        assert ae, "Automation Element is None"

        prop_ids_all = sorted([x for x in dir(comtypes.gen.UIAutomationClient) if 'PropertyId' in x])
        prop_ids = [x for x in prop_ids_all if '_Is' not in x]
        prop_is = set(prop_ids_all).difference(prop_ids)
        properties = {}
        print('/' * 80)
        for prop_id in prop_ids_all:
            id_to_check = getattr(comtypes.gen.UIAutomationClient, prop_id)
            val = ae.GetCurrentPropertyValue(id_to_check)
            print('{:<50}:{}'.format(prop_id, val))
        print('/' * 80)

    def __rectangle(self, ae=None):
        if ae is None:
            _rect = self.element.CurrentBoundingRectangle
        else:
            _rect = ae.CurrentBoundingRectangle
        return win32structures.RECT(_rect.left, _rect.top, _rect.right, _rect.bottom)

    # noinspection PyMethodMayBeStatic,PyProtectedMember
    def _perform_click_input(self,
                             ae=None,
                             button="left",
                             coords=(None, None),
                             double=False,
                             button_down=True,
                             button_up=True,
                             absolute=False,
                             wheel_dist=0):
        """Perform a click action using SendInput

        All the *ClickInput() and *MouseInput() methods use this function.

        Thanks to a bug report from Tomas Walch (twalch) on sourceforge and code
        seen at http://msdn.microsoft.com/en-us/magazine/cc164126.aspx this
        function now always works the same way whether the mouse buttons are
        swapped or not.

        For example if you send a right click to Notepad.Edit - it will always
        bring up a popup menu rather than 'clicking' it.
        """

        # Handle if the mouse buttons are swapped
        if win32functions.GetSystemMetrics(win32defines.SM_SWAPBUTTON):
            if button.lower() == 'left':
                button = 'right'
            else:
                button = 'left'

        events = []
        if button.lower() == 'left':
            if button_down:
                events.append(win32defines.MOUSEEVENTF_LEFTDOWN)
            if button_up:
                events.append(win32defines.MOUSEEVENTF_LEFTUP)
        elif button.lower() == 'right':
            if button_down:
                events.append(win32defines.MOUSEEVENTF_RIGHTDOWN)
            if button_up:
                events.append(win32defines.MOUSEEVENTF_RIGHTUP)
        elif button.lower() == 'middle':
            if button_down:
                events.append(win32defines.MOUSEEVENTF_MIDDLEDOWN)
            if button_up:
                events.append(win32defines.MOUSEEVENTF_MIDDLEUP)
        elif button.lower() == 'x':
            if button_down:
                events.append(win32defines.MOUSEEVENTF_XDOWN)
            if button_up:
                events.append(win32defines.MOUSEEVENTF_XUP)

        if button.lower() == 'wheel':
            events.append(win32defines.MOUSEEVENTF_WHEEL)

        # if we were asked to double click (and we are doing a full click
        # not just up or down.
        if double and button_down and button_up:
            events *= 2

        if isinstance(coords, win32structures.RECT):
            coords = (coords.left, coords.top)

            #    # allow points objects to be passed as the coords
            #    if isinstance(coords, win32structures.POINT):
            #        coords = [coords.x, coords.y]
            #    else:
        coords = list(coords)

        # set the default coordinates
        if coords[0] is None:
            coords[0] = self.__rectangle(ae).width() / 2
        if coords[1] is None:
            coords[1] = self.__rectangle(ae).height() / 2

        if not absolute:
            coords[0] = coords[0] + self.__rectangle(ae).left
            coords[1] = coords[1] + self.__rectangle(ae).top

        # set the cursor position
        win32functions.SetCursorPos(coords[0], coords[1])
        time.sleep(Timings.after_setcursorpos_wait)

        inp_struct = win32structures.INPUT()
        inp_struct.type = win32defines.INPUT_MOUSE

        for event in events:
            inp_struct._.mi.dwFlags = event
            if button.lower() == 'wheel':
                inp_struct._.mi.mouseData = wheel_dist
            else:
                inp_struct._.mi.mouseData = 0

            win32functions.SendInput(
                1,
                ctypes.pointer(inp_struct),
                ctypes.sizeof(inp_struct))

            time.sleep(Timings.after_clickinput_wait)

    # noinspection PyMethodMayBeStatic
    def best_match(self, str1, attr):
        """
        This will become a heuristic matching engine in the future
        """

        str1 = str1.replace(' ', '')
        str1 = str1.replace("'", "")
        str1 = str1.encode('ascii', 'ignore')
        if str(attr).lower() in str(str1).lower():
            return True
        else:
            return False

    def dump_child_elements(self, ae=None, verbose=False):
        if ae is None:
            ae = self.element

        cvw = Uia().uia.ControlViewWalker
        ae_child = cvw.GetFirstChildElement(ae)
        while ae_child:
            print('-' * 67)
            print('Name: {}'.format(ae_child.CurrentName))
            print('ClassName: {}'.format(ae_child.CurrentClassName))
            print('LocalizedControlType: {}'.format(ae_child.CurrentLocalizedControlType))
            if verbose:
                self.__get_supported_properties(ae_child)
            ae_child = cvw.GetNextSiblingElement(ae_child)

    def get_child_element(self, ae_parent=None, search_scope='', **kwargs):
        """
        ae_parent: automation element the search will start from. If None, defaults to self.element
        seach_scope: Children or Descendants. Corresponds to AutomationElement TreeScope
        kwargs: Property to search
        """

        assert len(kwargs)
        print('Properties: %s' % kwargs)

        if ae_parent is None:
            ae_parent = self.element

        if (len(search_scope) == 0) or (search_scope.lower() == 'children'):
            scope = comtypes.gen.UIAutomationClient.TreeScope_Children
        else:
            scope = comtypes.gen.UIAutomationClient.TreeScope_Descendants

        uia = Uia().uia
        # match by ChildIndex
        if 'ChildIndex' in kwargs:
            cond = uia.CreateTrueCondition()
            ae_collection = ae_parent.FindAll(scope, cond)
            index = kwargs['ChildIndex']
            ae = ae_collection.GetElement(index)
            assert ae, 'Automation Element is None child index {}'.format(index)
        else:
            # Match by kwargs
            conditions = []
            for key in kwargs:
                prop = getattr(comtypes.gen.UIAutomationClient, 'UIA_{}PropertyId'.format(key))
                cond = uia.CreatePropertyCondition(prop, kwargs[key])
                conditions.append(cond)

            cond_len = len(conditions)
            if cond_len == 2:
                and_cond = uia.CreateAndCondition(conditions[0], conditions[1])
                ae = ae_parent.FindFirst(scope, and_cond)
            elif cond_len > 2:
                print('8' * 88)
                and_cond_array = uia.CreateAndConditionFromArray(conditions)
                ae = ae_parent.FindFirst(scope, and_cond_array)
            else:
                ae = ae_parent.FindFirst(scope, cond)

        return ae

    def invoke(self):
        """
        Cause the default action to be sent to the control. For example, send click to button.
        :return: None
        """
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
                print('Retrying invoke...')
                time.sleep(retry_interval)
                loops += 1
                if loops > retry_max:
                    raise

    click = invoke

    def click(self, **kwargs):
        kw_len = len(kwargs)
        if len(kwargs) == 0:
            self._perform_click_input(ae=self.element)
        elif kw_len == 1 and 'ae' in kwargs:
            self._perform_click_input(ae=kwargs['ae'])
        elif kw_len == 2 and 'ae' in kwargs and 'button' in kwargs:
            self._perform_click_input(ae=kwargs['ae'], button=kwargs['button'])
        else:
            raise NotImplementedError('No handler for argument yet')

    def name(self):
        return self.element.CurrentName

    @Logger(trace_on)
    def name_best_match(self, ae=None, string_match=''):
        assert ae, 'AE object None'

        cvw = Uia().uia.ControlViewWalker
        ae = cvw.GetFirstChildElement(ae)
        print('string_match:', string_match)
        while ae:
            print('-' * 10)
            print('Name: ', ae.CurrentName)
            print('LocalizedControlType:', ae.CurrentLocalizedControlType)
            print('ClassName: ', ae.CurrentClassName)
            if self.best_match(ae.CurrentClassName, string_match):
                break
            elif ae.CurrentName is not None and self.best_match(ae.CurrentName, string_match):
                break
            ae = cvw.GetNextSiblingElement(ae)

        # Don't need to assert if None, we need to check using other mechanism
        return ae

    def sendkeys(self, keys):
        SendKeys(keys)

    def wait_window_exists(self, ae_parent=None, timeout=10.0, wait_interval=0.2, search_scope='Children', **kwargs):
        """
        timeout(float): -1, wait forever, else wait for x secs
        kwargs:
            Special keys:
                NameBestMatch: Match using simple best match algorithm
        :returns: automation element
        """

        def __name_best_match():
            return self.NameBestMatch(aeObj=ae_parent, strMatch=kwargs['NameBestMatch'])

        def __regular_match():
            return self.get_child_element(ae_parent=ae_parent, search_scope=search_scope, **kwargs)

        if ae_parent is None:
            ae_parent = self.element

        if 'NameBestMatch' in kwargs:
            match_proc = __name_best_match
        else:
            match_proc = __regular_match

        time_start = time.time()
        while True:
            ae = match_proc()
            if ae:
                return ae
            else:
                print('Waiting for window to exists: {}'.format(kwargs))
                time.sleep(wait_interval)
                if timeout != -1:
                    if timeout < time.time() - time_start:
                        raise TimeOutError


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
            assert "Element does not support ValuePattern"


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
                print('Waiting for {}/{} to expand--@{}'.format(parent.element.CurrentName, attr, time.asctime()))
                self.click(ae=ae)
                time.sleep(0.1)

        else:
            print('menu item.... yes')
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

        state = self.element.GetCurrentPropertyValue(
            comtypes.gen.UIAutomationClient.UIA_LegacyIAccessibleStatePropertyId)

        # noinspection PyPep8Naming
        STATE_SYSTEM_CHECKED = 0x10
        print('state is {}'.format(state))
        if STATE_SYSTEM_CHECKED & state == STATE_SYSTEM_CHECKED:
            checked = True

        while True:
            el = Uia().uia.GetFocusedElement()
            if el.CurrentLocalizedControlType == 'menu item':
                self.sendkeys('{ESC}')
            else:
                break
        return checked


class CPopupMenu(CWindow):
    """
    PopupMenu handler. Can be called as a callable or as attribute

    Usage:
    app.PopupMenu(path='Menu1~Menu2')
    Navigate to menu Menu1->Menu2 via a context menu
    Optional parameters:
        separator(string): string used to split the path, default is '~'
    """

    def __init__(self, attr=None, parent=None):
        """
        Optional parameters:
            attr(string): setup automatically in __attr__ and various places
            parent(Object): Parent object of this class instance, setup in __attr__ and various places
        """
        self.parent = parent

        super(CPopupMenu, self).__init__(attr=attr, parent=parent, ae_init=True)

        ae_root = Uia().root()
        assert ae_root

        ae_menu = self.wait_window_exists(ae_parent=ae_root, LocalizedControlType='menu', wait_interval=0.5)
        assert ae_menu, 'Automation Element None'

        self.element = ae_menu

    def __call__(self, **kwargs):
        sep = 'separator'
        if sep in kwargs:
            separator = kwargs[sep]
            kwargs.pop(sep)
        else:
            separator = '~'

        assert 'path' in kwargs
        ae = self.element
        assert ae

        items = kwargs['path'].split(separator)
        print('Items : {}'.format(items))
        for item in items:
            print('Menu: ', item)

            count = 0
            while True:
                try:
                    cond = Uia().uia.CreatePropertyCondition(comtypes.gen.UIAutomationClient.UIA_NamePropertyId,
                                                             item)
                    # .Descendants, required for menu as the element parent/child relationship is messed up in win32
                    ae_new = ae.FindFirst(scope=comtypes.gen.UIAutomationClient.TreeScope_Descendants, condition=cond)
                    if ae_new is None:
                        self.wait_window_exists(ae_parent=ae, search_scope='Descendants', Name=item)
                    else:
                        ae = ae_new
                        break
                except TimeOutError:
                    count += 1
                    print('Menu cannot be detected, retrying %s' % count)
                    swf.SendKeys.SendWait('{ESC}')
                    ae.SetFocus()
                    swf.SendKeys.SendWait('{RIGHT}')
                    if count > 5:
                        msg = 'Menu element not detected %s... retrying' % item
                        raise DebuggingForcedError(msg)
            assert ae
            if items.index(item) < len(items) - 1:
                print('Focusing ', item)
                ae.SetFocus()
                swf.SendKeys.SendWait('{RIGHT}')

        self.click(ae=ae)
        return self


class CTreeView(CWindow):
    """ TreeView control """

    # noinspection PyClassHasNoInit
    class ExpandCollapseState:
        ExpandCollapseState_Collapsed, ExpandCollapseState_Expanded, ExpandCollapseState_PartiallyExpanded, \
        ExpandCollapseState_LeafNode = range(4)

    def __init__(self, attr=None, parent=None):
        self.parent = parent
        self.current_node = None  # Current Treeview node
        super(CTreeView, self).__init__(attr=attr, parent=parent)

        # This is when creating object specifically called for CTreeview
        if str(attr).lower() == 'treeview' and self.element is None:
            self.element = parent.element  # this is not the correct element, will be corrected in __call__

    def __getattr__(self, attr):
        if str(attr).lower() == 'popupmenu':

            count = 0
            while True:
                try:
                    self.Click(self.current_node, button='right')
                    aeRoot = iprcs.uiauto().RootElement()
                    assert aeRoot

                    self.wait_window_exists(aeRoot, LocalizedControlType='menu', timeout=10.0, wait_interval=0.5)
                    break
                except TimeOutError:
                    # Why is menu is not there? not completed loading yet?
                    if count > 5:
                        raise DebuggingForcedError('Menu element not detected')

                    count += 1
                    print('Menu cannot be detected, retrying %s' % count)
                    swf.SendKeys.SendWait('{ESC}')
                    time.sleep(1.0)  # Wait long enough for the view to load
                    #                    if bool(self.curnode.GetCurrentPropertyValue( swa.AutomationElement.IsOffscreenProperty)) == True:
                    #                        print 'Item not visible, scrolling into view'
                    #                        pat = self.curnode.GetCurrentPattern( swa.ScrollItemPattern.Pattern)
                    #                        pat.ScrollIntoView()

            obj = CPopupMenu(trace=True, attr=attr, parent=self)
            return obj
        else:  # AtributeError handled by base class
            obj = super(CTreeView, self).__getattr__(attr)

    def click(self, **kwargs):
        if 'ae' in kwargs:
            self._perform_click_input(ae=kwargs['ae'], coords=(-5, 0))
        else:
            return super(CTreeView, self).click(**kwargs)

    def traverse(self, path, separator=None):
        if separator is None:
            separator = '~'
        items = path.split(separator)
        count_traverse = 0
        while True:
            ae = self.element
            for item in items:
                print('Node: {}'.format(item))
                pattern_match = False
                cond = Uia().uia.CreatePropertyCondition(comtypes.gen.UIAutomationClient.UIA_NamePropertyId,
                                                         item)
                ae = ae.FindFirst(scope=comtypes.gen.UIAutomationClient.TreeScope_Children, condition=cond)
                assert ae
                state = ae.GetCurrentPropertyValue(
                    comtypes.gen.UIAutomationClient.UIA_ExpandCollapseExpandCollapseStatePropertyId)

                print('state: {}'.format(state))
                if state == self.ExpandCollapseState.ExpandCollapseState_Expanded:
                    pat = ae.GetCurrentPattern(swa.SelectionItemPattern.Pattern)
                    pat.Select()
                else:
                    print('item: {}'.format(item))
                    self.click(ae=ae)
                    while True:
                        state = ae.GetCurrentPropertyValue(
                            comtypes.gen.UIAutomationClient.UIA_ExpandCollapseExpandCollapseStatePropertyId)
                        print('current state : {}'.format(state))
                        if state in (self.ExpandCollapseState.ExpandCollapseState_Expanded,
                                     self.ExpandCollapseState.ExpandCollapseState_LeafNode):
                            break
                        print('Waiting for %s to expand' % item)
                        time.sleep(0.1)
                    if bool(ae.GetCurrentPropertyValue(
                            comtypes.gen.UIAutomationClient.UIA_IsScrollItemPatternAvailablePropertyId)):
                        if_pattern = ae.GetCurrentPattern(
                            comtypes.gen.UIAutomationClient.UIA_ScrollItemPatternId)
                        pat = if_pattern.QueryInterface(
                            comtypes.gen.UIAutomationClient.IUIAutomationScrollItemPattern)
                        pat.ScrollIntoView()

                if ae.GetCurrentPropertyValue(comtypes.gen.UIAutomationClient.UIA_NamePropertyId) == item:
                    pattern_match = True
                else:
                    # raise DebuggingForcedError('Tree traverse bad item')
                    break

            if pattern_match:
                break
            else:
                count_traverse += 1
                if count_traverse > 3:
                    raise DebuggingForcedError('Tree traverse bad item')

        self.current_node = ae


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
                print('Main window not there yet, retrying... @%s' % time.asctime())
                time.sleep(0.1)
                i_loop += 1
                if i_loop >= 5:
                    print('Giving up on trying to get main window...%s' % time.asctime())
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
            print('Generic window : {}'.format(attr))
            obj = super(MainWindow, self).__getattr__(attr)

        if obj.element:
            return obj
        else:
            raise(AttributeError, attr)

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
            ae = self.wait_window_exists(timeout=timeout, wait_interval=wait_interval, Name=caption)
        else:
            raise DebuggingForcedError

    # noinspection PyMethodMayBeStatic,PyPep8Naming
    def wait_for_input_idle(self):
        WaitForInputIdle = ctypes.windll.user32.WaitForInputIdle
        OpenProcess = ctypes.windll.kernel32.OpenProcess
        PROCESS_QUERY_INFORMATION = 1024
        hwnd_process = OpenProcess(PROCESS_QUERY_INFORMATION, 0, self.parent.proc.pid)
        ret = WaitForInputIdle(hwnd_process, -1)


class App(object):
    def __init__(self):
        super(App, self).__init__()
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
    # app = App()
    # app.start(['notepad'])
    # notepad = app.Notepad
    # notepad.edit.type("hello")
    # notepad.close()
    # notepad.wait_for(object_type='dialog', caption='Notepad')
    # notepad.Notepad.DontSave.click()

    print(comtypes.gen.UIAutomationClient.UIA_IsValuePatternAvailablePropertyId)
    print(dir(comtypes.gen.UIAutomationClient))
