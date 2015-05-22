import unittest
import sys
sys.path.append('..')
import haru

# skip = True
skip = False

class HaruTest(unittest.TestCase):
    @unittest.skipIf(skip, "bypass")
    def test_cwindow_invoke(self):
        app = haru.App()
        app.start(['notepad'])
        notepad = app.Notepad
        notepad.edit.type("hello")
        notepad.close()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.invoke()

    @unittest.skipIf(skip, "bypass")
    def test_cwindow_click(self):
        app = haru.App()
        app.start(['notepad'])
        notepad = app.Notepad
        notepad.edit.type("hello")
        notepad.close()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

    @unittest.skipIf(skip, "bypass")
    def test_file_exit(self):
        """Test File | Exit"""

        app = haru.App()
        app.start('notepad.exe')
        notepad = app.Notepad
        notepad.edit.type("hello world")
        notepad.Menu.File.Exit.click()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

    @unittest.skipIf(skip, "bypass")
    def test_cwindow_maximize(self):
        app = haru.App()
        app.start(['notepad'])
        notepad = app.Notepad
        notepad.edit.type("hello")
        notepad.maximize()
        notepad.close()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

    @unittest.skipIf(skip, "bypass")
    def test_is_menu_checked(self):
        """Menu checked"""
        app = haru.App()
        app.start(['notepad.exe'])
        notepad = app.Notepad
        notepad.edit.type("hello")

        # Either check it or not
        notepad.Menu.View.StatusBar.click()
        if notepad.Menu.View.StatusBar.is_checked():
            print "Item checked"
        else:
            print "not checked"
        # Either check it or not
        notepad.Menu.View.StatusBar.click()
        if notepad.Menu.View.StatusBar.is_checked():
            print "Item checked"
        else:
            print "not checked"
        notepad.Menu.File.Exit.click()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

    @unittest.skipIf(skip, "bypass")
    def test_status_bar(self):
        """Test Status Bar"""
        app = haru.App()
        app.start(['notepad.exe'])
        notepad = app.Notepad
        notepad.edit.type("hello")
        is_checked = notepad.Menu.View.StatusBar.is_checked()
        print('{} checked : {}'.format('*'*10, is_checked))
        if not is_checked:
            notepad.Menu.View.StatusBar.click()

        sb = notepad.StatusBar(ClassName='msctls_statusbar32')
        obj = sb.Window(ChildIndex=1)
        print obj.name()
        notepad.Menu.File.Exit.click()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

    @unittest.skipIf(skip, "bypass")
    def test_status_bar_2_params(self):
        """__call__ with 2 params"""
        app = haru.App()
        app.start(['notepad.exe'])
        notepad = app.Notepad
        notepad.edit.type("hello")
        is_checked = notepad.Menu.View.StatusBar.is_checked()
        print('{} checked : {}'.format('*'*10, is_checked))
        if not is_checked:
            notepad.Menu.View.StatusBar.click()

        sb = notepad.StatusBar(ClassName='msctls_statusbar32', FrameworkId='Win32')
        obj = sb.Window(ChildIndex=1)
        print obj.name()
        notepad.Menu.File.Exit.click()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

    @unittest.skipIf(skip, "bypass")
    def test_status_bar_3_params(self):
        """__call__ with 3 params"""
        app = haru.App()
        app.start(['notepad.exe'])
        notepad = app.Notepad
        notepad.edit.type("hello")
        is_checked = notepad.Menu.View.StatusBar.is_checked()
        print('{} checked : {}'.format('*'*10, is_checked))
        if not is_checked:
            notepad.Menu.View.StatusBar.click()

        sb = notepad.StatusBar(ClassName='msctls_statusbar32', FrameworkId='Win32', LocalizedControlType="status bar")
        obj = sb.Window(ChildIndex=1)
        print obj.name()
        notepad.Menu.File.Exit.click()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

    @unittest.skipIf(skip, "bypass")
    def test_wait_for(self):
        """Test WaitWindowExists"""
        app = haru.App()
        app.start(['notepad.exe'])
        notepad = app.Notepad
        notepad.edit.type("hello")
        is_checked = notepad.Menu.View.StatusBar.is_checked()
        print('{} checked : {}'.format('*'*10, is_checked))
        if not is_checked:
            notepad.Menu.View.StatusBar.click()

        sb = notepad.StatusBar(ClassName='msctls_statusbar32', FrameworkId='Win32', LocalizedControlType="status bar")
        obj = sb.Window(ChildIndex=1)
        notepad.Menu.File.Exit.click()
        print('Test here')
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

if __name__ == '__main__':
    unittest.main()
