import os
import unittest
import sys

path = os.path.realpath(__file__)
p = os.path.split(path)
while p[1] != 'test':
    p = os.path.split(p[0])
sys.path.append(p[0])
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
            print("Item checked")
        else:
            print("not checked")
        # Either check it or not
        notepad.Menu.View.StatusBar.click()
        if notepad.Menu.View.StatusBar.is_checked():
            print("Item checked")
        else:
            print("not checked")
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
        print('{} checked : {}'.format('*' * 10, is_checked))
        if not is_checked:
            notepad.Menu.View.StatusBar.click()

        sb = notepad.StatusBar(ClassName='msctls_statusbar32')
        obj = sb.Window(ChildIndex=1)
        print(obj.name())
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
        print('{} checked : {}'.format('*' * 10, is_checked))
        if not is_checked:
            notepad.Menu.View.StatusBar.click()

        sb = notepad.StatusBar(ClassName='msctls_statusbar32', FrameworkId='Win32')
        obj = sb.Window(ChildIndex=1)
        print(obj.name())
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
        print('{} checked : {}'.format('*' * 10, is_checked))
        if not is_checked:
            notepad.Menu.View.StatusBar.click()

        sb = notepad.StatusBar(ClassName='msctls_statusbar32', FrameworkId='Win32', LocalizedControlType="status bar")
        obj = sb.Window(ChildIndex=1)
        print(obj.name())
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
        print('{} checked : {}'.format('*' * 10, is_checked))
        if not is_checked:
            notepad.Menu.View.StatusBar.click()

        sb = notepad.StatusBar(ClassName='msctls_statusbar32', FrameworkId='Win32', LocalizedControlType="status bar")
        obj = sb.Window(ChildIndex=1)
        notepad.Menu.File.Exit.click()
        print('Test here')
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

    @unittest.skipIf(skip, "bypass")
    def test_dump_elements(self):
        """Test dump elements"""
        app = haru.App()
        app.start(['notepad.exe'])
        notepad = app.Notepad
        notepad.dump_child_elements(verbose=True)
        notepad.Menu.File.Exit.click()

    @unittest.skipIf(skip, "bypass")
    def test_tree_view(self):
        """Test Treeview object
        Note that this requires test\testapp\treeview.sln be built using Visual Studio
        """
        app = haru.App()
        loc = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testapp/treeview/bin/Debug/treeview.exe')
        print(loc)
        app.start([loc])
        tv_test = app.treeview
        tv = tv_test.Treeview(LocalizedControlType='tree')
        tv.traverse('Root~A~AA~AAA')
        tv_test.close()

    @unittest.skipIf(skip, "bypass")
    def test_popup_menu(self):
        """Test handling of popup menu"""
        app = haru.App()
        app.start('notepad.exe')
        notepad = app.Notepad
        edit = notepad.edit
        edit.type('hello world')
        edit.sendkeys('^a')
        edit.sendkeys('^c')
        edit.sendkeys('{END}{ENTER}')
        edit.sendkeys('^v{ENTER}^v{ENTER}^v{ENTER}')
        edit.PopupMenu(path='Paste')
        notepad.Menu.File.Exit.click()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

if __name__ == '__main__':
    unittest.main(failfast=True)
