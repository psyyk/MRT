import collections


class Shop(object):
	active_staff = []
	def __init__(self, staff):
		self.staff = staff
		
	def addActiveEmployee(self, ID):
		for temp in self.staff:
			if temp.ID == ID:
				self.active_staff.append(temp)
		return

	def removeActiveEmployeeByID(self, ID):
		for temp in self.active_staff:
			if temp.ID == ID:
				self.active_staff.remove(temp)

		return

	def getNumberOfStaffInShop(self):
		return len(self.active_staff)

	def checkIdentity(self, ID):
		for temp in self.staff:
			if temp.ID == ID:
				return True
			
		return False

	def checkIsActive(self, ID):
		for temp in self.active_staff:
			if temp.ID == ID:
				return True
			
		return False
	def findNameById(self, ID):
		for temp in self.staff:
			if temp.ID == ID:
				return temp.name
		return False


class Employee(object):
	
	def __init__(self, name, ID):
		self.name = name
		self.ID = ID

	def printInfo(self):
		print("Name: " + self.name + " ID: " + str(self.ID))
		return

		








