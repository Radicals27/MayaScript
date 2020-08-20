import maya.cmds as cmds
import maya.mel as mel
from functools import partial
import pymel.core as pm

#Initialise main window
def ui ():
   global animation_checkbox
    
   #Check if window exsts already, if so delete it before creating new one
   if cmds.window('MaxartScript', exists = True):
      cmds.deleteUI('MaxartScript')

   myWin = cmds.window('MaxartScript')
   cmds.columnLayout( adjustableColumn=True, rs=5)
   cmds.button(label = 'Delete non-deformer history', command = 'deleteNonDeformer()')
   cmds.button(label = 'Delete History', command = 'deleteHistory()')
   cmds.button(label = 'Freeze Transformations', command = 'freezeTransformations()')
   cmds.button(label = 'Center Pivots', command = 'centerPivot()')

   animation_checkbox = cmds.checkBox('animations', label='Bake Animations', onc=partial(checked, 'animations'))
   
   cmds.text( label='Please choose an export location and include <filename>.fbx :')
   cmds.button(label = 'Export to (browse)', command = 'browseLocation()')
   
   cmds.button(label = 'Export', command= 'export()')
   
   cmds.showWindow('MaxartScript')

# Display GUI to browse folder/file structure   
def browseLocation(*args):
   global exportPath
   exportPath = pm.fileDialog2(fm=0, okc='selectFolder', cap='Select Export Folder')[0]
   
# Handle the checking of the "animations" checkbox
def checked(button, *args):
   cmds.checkBox(button, e=True, v=True)

def deleteNonDeformer():
   selection = cmds.ls(sl=True)

   if selection.count != 0:
      print("Deleting Non-deformers...")
      for item in selection:
         mel.eval("doBakeNonDefHistory( 1, {\"prePost\" });")
   else:
      print("Please select an item")

def deleteHistory():
   selection = cmds.ls(sl=True)

   if selection.count != 0:
      print("Deleting history...")
      for item in selection:
         cmds.delete( all=True, ch=True )
   else:
      print("Please select an item")

def freezeTransformations():
   selection = cmds.ls(sl=True)

   if selection.count != 0:
      print("Freezing Transformations...")
      for item in selection:
         mel.eval("makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;")
   else:
      print("Please select an item")

def centerPivot():
   selection = cmds.ls(sl=True)

   if selection.count != 0:
      print("Centering Pivots...")
      for item in selection:
         cmds.xform(cp=True)
   else:
      print("Please select an item")

def export(*args):
   animation_export = cmds.checkBox(animation_checkbox, q=True, v=True)
   if(animation_export):
      print("Exporting with animations")
      mel.eval('FBXExportBakeComplexAnimation -v true;')
   else:
      print("Exporting without animations")
      mel.eval('FBXExportBakeComplexAnimation -v false;')
   
   mel.eval('string $exportPath = `python "exportPath"`;')
   mel.eval('FBXExport -f $exportPath;')
   print('Saving to: ' + exportPath)
   # saves to 'C:\Program Files\Autodesk\Maya2019\bin' if path is unspecified

# Run the program
ui()