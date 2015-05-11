import comtypes
import comtypes.client
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
                #This is when creating object specifically called for a specific window
                windows = ['window','statusbar']
                if str(attr).lower() in windows and ae == None:
                    #This information gets used in __call__
                    self.element = self.parent.element
                else:
                    self.element = None

    @Logger(trace_on)
    def name_best_match(self, ae=None, string_match=''):
        assert ae, 'AE object None'

        ae = swa.TreeWalker.ControlViewWalker.GetFirstChild( ae )
        while ae:
            print '-'*10
            print 'Name: ',ae.Current.Name
            print 'LocalizedControlType:',ae.Current.LocalizedControlType
            print 'ClassName: ',ae.Current.ClassName
            if self.BestMatch(ae.Current.Name, string_match ):
                break
            ae = swa.TreeWalker.ControlViewWalker.GetNextSibling( ae )

        #Don't need to assert of None, we need to check using other mechanism
        return ae


class MainWindow(CWindow):
    """Represents the main window"""
    def __init__(self, trace=False, attr = None, parent= None):

        self.trace = trace
        self.attr = attr
        self.proc = parent.proc
        self.aeRoot = iprcs.uiauto().RootElement()


        iLoop = 0
        while True:
            prop = swa.AutomationElement.ProcessIdProperty
            cond = swa.PropertyCondition( prop, self.proc.Id )
            ae = self.aeRoot.FindFirst(swa.TreeScope.Children, cond)

            if ae:
                break
            else:
                print 'Main window not there yet, retrying... @%s'%time.asctime()
                time.sleep( 0.1 )
                iLoop += 1
                if iLoop >= 5:
                    print 'Giving up on trying to get main window...%s'%time.asctime()
                    break
        self.element = ae

        super( MainWindow, self ).__init__(trace = trace, attr = attr, parent=parent, aeInit=True)


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
        obj = MainWindow(trace=True, attr=attr, parent=self)
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
    # with Uia() as uia:
    #     print(uia.root().currentName)
    # robot = Robot()
    # robot.start(['notepad'])
    # notepad = robot.Notepad
    a = Uia()
    print(a.root().currentName)
    b = Uia()
    if a is b:
        print('ok')