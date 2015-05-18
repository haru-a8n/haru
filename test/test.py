import unittest
import sys
sys.path.append('..')
import haru

skip = True
# skip = False

class HaruTest(unittest.TestCase):
    @unittest.skipIf(skip, "bypass")
    def test_cwindow_invoke(self):
        robot = haru.Robot()
        robot.start(['notepad'])
        notepad = robot.Notepad
        notepad.edit.type("hello")
        notepad.close()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.invoke()

    @unittest.skipIf(skip, "bypass")
    def test_cwindow_click(self):
        robot = haru.Robot()
        robot.start(['notepad'])
        notepad = robot.Notepad
        notepad.edit.type("hello")
        notepad.close()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

    @unittest.skipIf(skip, "bypass")
    def testFileExit(self):
        """Test File | Exit"""

        robot = haru.Robot()
        robot.start('notepad.exe')
        notepad = robot.Notepad
        notepad.edit.type("hello world")
        notepad.Menu.File.Exit.click()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

    @unittest.skipIf(skip, "bypass")
    def test_cwindow_maximize(self):
        robot = haru.Robot()
        robot.start(['notepad'])
        notepad = robot.Notepad
        notepad.edit.type("hello")
        notepad.maximize()
        notepad.close()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

    @unittest.skipIf(skip, "bypass")
    def testIsMenuChecked(self):
        """Menu checked"""
        robot = haru.Robot()
        robot.start(['notepad.exe'])
        notepad = robot.Notepad
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

    def testStatusBar(self):
        """Test Status Bar"""
        robot = haru.Robot()
        robot.start(['notepad.exe'])
        notepad = robot.Notepad
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

if __name__ == '__main__':
    unittest.main()