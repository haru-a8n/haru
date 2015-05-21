#Haru Automation#
Windows UI Automation using mostly UIA

##Automate Notepad?
````python
app = App()
app.start(['notepad'])
notepad = app.Notepad
notepad.edit.type("hello")
notepad.close()
notepad.wait_for(object_type='dialog', caption='Notepad')
notepad.Notepad.DontSave.click()
````


##Installation##
* Download 32-bit version of Python 2.7.9 or newer from www.python.org
* Install comtypes
  * Other Windows OS versions
````
      pip install comtypes
````
  * Windows 10 64-bit build 10074 (due to bug, see http://bugs.python.org/issue24127)
````
      python -m pip install comtypes
````		
		
##Related projects##
* http://code.google.com/p/swapy/
* http://code.google.com/p/pywinauto/
* http://stackoverflow.com/questions/22198792/create-a-poker-table-scanner
	
