import unittest
import sys
sys.path.append('..')
import haru

skip = False


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

    def testFileExit(self):
        """Test File | Exit"""

        robot = haru.Robot()
        robot.start('notepad.exe')
        notepad = robot.Notepad
        notepad.edit.type("hello world")
        notepad.Menu.File.Exit.click()
        notepad.wait_for(object_type='dialog', caption='Notepad')
        notepad.Notepad.DontSave.click()

if __name__ == '__main__':
    unittest.main()