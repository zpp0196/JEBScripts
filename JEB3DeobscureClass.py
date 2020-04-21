# -*- coding: utf-8 -*-
"""
Deobscure class name(use debug directives as source name) for PNF Software's JEB3.
Thank for: https://github.com/S3cuRiTy-Er1C/JebScripts/blob/master/JEB2DeobscureClass.py
"""

__author__ = 'zpp0196'

from com.pnfsoftware.jeb.client.api import IScript, IconType, ButtonGroupType
from com.pnfsoftware.jeb.core import RuntimeProjectUtil
from com.pnfsoftware.jeb.core.units.code import ICodeUnit, ICodeItem
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit
from com.pnfsoftware.jeb.core.actions import Actions, ActionContext, ActionCommentData, ActionRenameData
from java.lang import Runnable

class JEB3DeobscureClass(IScript):
    def run(self, ctx):
        projects = ctx.getEnginesContext().getProjects()
        if not projects:
            ctx.displayMessageBox('Warnning', 'Please open a project first!', IconType.WARNING, ButtonGroupType.OK)
            return
        ctx.executeAsync('Running deobscure class ...', RenameRunnable(projects[0]))

class RenameRunnable(Runnable):
    def __init__(self, project):
        self.project = project

    def run(self):
        print('Deobscure class start ...')
        units = RuntimeProjectUtil.findUnitsByType(self.project, IDexUnit, False)
        for i, unit in enumerate(units):
            print('Process %s(%s/%s)'%(unit, i + 1, units.size()))
            classes = unit.getClasses()
            if not classes:
                continue
            rep = {}
            for clz in classes:
                if not clz.getName(): # Anonymous inner class
                   continue
                adr = str(clz.getAddress())
                if '$' in adr: # Inner class
                    continue
                sidx = clz.getSourceStringIndex()
                if sidx == -1: # Not keep SourceFile attributes
                    continue
                sname = str(unit.getString(sidx))
                ignored = ('ProGuard', "SourceFile")
                if sname in ignored: # -renamesourcefileattribute SourceFile
                    continue
                if sname.endswith('.java'):
                    sname = sname[:-5]
                elif sname.endswith('.kt'):
                    sname = sname[:-3]
                key = adr[:adr.rfind('/') + 1] + sname
                cname = rep.get(key, 0)
                rep[key] = cname + 1
                if self.isKeeped(sname, clz): # There is no need to rename
                    continue
                if cname > 0:
                    sname += '$$$' + str(cname)
                ret = self.commentClass(unit, clz, adr) and self.renameClass(unit, clz, sname)
                print('%s -> %s %s'%(adr, sname, ret))
        print('Done')

    def renameClass(self, unit, clz, sname):
        ctx = ActionContext(unit, Actions.RENAME, clz.getItemId(), clz.getAddress())
        data = ActionRenameData()
        data.setNewName(sname)
        if not unit.prepareExecution(ctx, data):
            return False
        try:
            return unit.executeAction(ctx, data)
        except Exception as e:
            print(Exception, e)
        return False

    def commentClass(self, unit, clz, adr):
        ctx = ActionContext(unit, Actions.COMMENT, clz.getItemId(), clz.getAddress())
        data = ActionCommentData()
        data.setNewComment(adr.replace('/', ".")[1:-1])
        if not unit.prepareExecution(ctx, data):
            return False
        try:
            return unit.executeAction(ctx, data)
        except Exception as e:
            print(Exception, e)
        return False

    def isKeeped(self, name, clz):
        adr = str(clz.getAddress())
        sn = adr[adr.rfind('/') + 1:-1]
        return sn == name
