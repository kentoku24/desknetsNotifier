dim fso
set fso = createObject("Scripting.FileSystemObject")
currentdir = fso.getParentFolderName(WScript.ScriptFullName)

command = "cmd /c " & currentdir & "\_backgroundRunner.bat"

Set objWShell = CreateObject("Wscript.Shell") 
objWShell.run command, vbHide 