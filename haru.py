import comtypes
import comtypes.client
import string
import subprocess

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

    # noinspection PyMethodMayBeStatic
    def best_match(self, str1, attr):
        """
        This will become a heuristic matching engine in the future
        """

        str1 = string.replace(str1, ' ', '')
        str1 = string.replace(str1, "'", "")
        if str(attr).lower() in str(str1).lower():
            return True
        else:
            return False

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
            ae = cvw.GetNextSiblingElement(ae)

        # Don't need to assert of None, we need to check using other mechanism
        return ae


class CEdit(CWindow):
    """ Edit control """

    def __init__(self, trace = False, attr = None, parent=None):
        self.trace = trace
        super( CEdit, self ).__init__(trace = trace, attr = attr, parent = parent)

        #This is when creating object specifically called for CEdit
        if str(attr).lower() == 'edit' and self.element == None:
            self.element = parent.element #this is not the correct element, will be corrected in __call__

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


class MainWindow(CWindow):
    """Represents the main window"""
    def __init__(self, attr=None, parent=None):

        assert not (parent is None)
        self.attr = attr
        self.uia = Uia()
        i_loop = 0
        while True:
            print(parent.proc.pid)
            cond = self.uia.uia.CreatePropertyCondition(comtypes.gen.UIAutomationClient.UIA_ProcessIdPropertyId,
                                                        parent.proc.pid)
            ae = self.uia.root().FindFirst(scope=comtypes.gen.UIAutomationClient.TreeScope_Children, condition=cond)

            if ae:
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
        if self.trace and hasattr(sys,'_getframe'):
            print '>>%s@%s@%s'%(self.__class__,sys._getframe(0).f_code.co_name,attr)

        #match main menu
        if attr.lower() == 'menu':
            cond = swa.PropertyCondition( swa.AutomationElement.ControlTypeProperty, swa.ControlType.MenuBar)
            menubarElement = self.element.FindFirst(swa.TreeScope.Children, cond)
            if menubarElement:
                obj = CMenuBar( trace=self.trace, attr = attr, parent = self )
                obj.__dict__['parent'] = self
                obj.__dict__['aeMain'] = self.element
                obj.__dict__['element'] = menubarElement
        elif attr.lower() == 'edit':
            obj = CEdit(trace=True, attr = attr, parent = self)
        else:
            obj = super( MainWindow, self).__getattr__(attr)

        if obj.element:
            return obj
        else:
            raise AttributeError, attr

    @Logger(trace_on)
    def close(self):
        # http://weichong78.blogspot.com/2013/11/python-com-and-windows-uiautomation.html
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ee671195(v=vs.85).aspx
        pattern = self.element.GetCurrentPattern(comtypes.gen.UIAutomationClient.UIA_WindowPatternId)
        interface_close = pattern.QueryInterface(comtypes.gen.UIAutomationClient.IUIAutomationWindowPattern)
        interface_close.Close()


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
            raise AttributeError, attr


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