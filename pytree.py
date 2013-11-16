#!/usr/bin/python 
import os
import uuid
import json

class PyTree:
	def __init__(self,fileDir):
		self.fileDir = fileDir
		self.fileObjTree = None
		self.__createPyTreePath()	
		
	def tree(self):
		self.fileObjTree = {
			'isDir': True,
			'name': self.fileDir,
			'uuid': self.__newId(),
			'parent': None,
			'childList': []
		}	
		self.__walk(self.fileDir,self.fileObjTree)
		self.__writeToJsonFile()
	def getFileIdList(self):
		pass

	def isJsonFileExist(self):
		return os.path.isfile(self.getJsonFilePath())
	
	def getPyTreePath(self):
		return self.fileDir + "/.pytree"

	def getJsonFilePath(self):
		return self.getPyTreePath() + "/filetree.json"	

	def __createPyTreePath(self):
		pyTreePath = self.getPyTreePath()
		if not os.path.exists(pyTreePath):
			os.makedirs(pyTreePath)

 	def __readFromJsonFile(self):
		f = open(self.getJsonFilePath())
		str =  f.read()
		f.close()
		self.fileObjTree = json.loads(str)		

	def __writeToJsonFile(self):
		str = json.dumps(self.fileObjTree)
		f = open(self.getJsonFilePath(),'w')
		f.write(str)
		f.close()

	def __newId(self):
		return str(uuid.uuid1())
		

	def __walk(self,fileDir,parentFileObj):
		for fileObjName in os.listdir(fileDir):
			if self.__isHidden(fileObjName):
				continue
			file = os.path.join(fileDir,fileObjName)
			isDir = os.path.isdir(file)
			thisFileObj = {}
			thisFileObj['isDir'] = isDir
			thisFileObj['name'] = fileObjName
			thisFileObj['uuid'] = self.__newId()
			thisFileObj['parent'] = parentFileObj['uuid']
			thisFileObj['childList'] = []
			parentFileObj['childList'].append(thisFileObj)	
			if isDir:
				self.__walk(file,thisFileObj)
			else:
				print file	

	def __isHidden(self,fileObjName):
		if fileObjName!="." and fileObjName[0] == ".":
			return True
		else:
			return False
 


def main():
	pyTree = PyTree(".")
	pyTree.tree()

	
if __name__ == '__main__':
	main()
