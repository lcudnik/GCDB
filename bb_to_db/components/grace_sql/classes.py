class Student:
    idLocation = ""
    idBlackbaud = ""
    idRenWeb = ""
    nameLast = ""
    nameMiddle  = ""
    nameFirst = ""
    namePreferred = ""
    gradeLevel = ""
    emailAddress = ""
    gender = ""
    graduationYear = ""
    birthDate = ""
    ethnicity = ""
    race = ""
    sam = ""
    userName = ""
    AccessCard = ""

    def __str__(self):
        return self.idBlackbaud
    
    def toHeader(self):
        return [key for key in self.__dict__.keys()]
    
    def toIterable(self):
        return [getattr(self, key,"") for key in self.__dict__.keys()]
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
    

class Staff:
    idLocation = ""
    idBlackbaud = ""
    idRenWeb = ""
    nameLast = ""
    nameMiddle  = ""
    nameFirst = ""
    namePreferred = ""
    jobBusiness = ""
    emailAddress = ""
    jobTitle = ""
    jobOrg = ""
    sam = ""
    userName = ""
    groupCA = bool
    groupHS = bool
    groupMS78 = bool
    groupMS56 = bool
    groupEL = bool
    groupGU = bool
    groupGAFE = bool
    groupSUB = bool

    def __str__(self):
        return self.idBlackbaud
    
    def toHeader(self):
        return [key for key in self.__dict__.keys()]
    
    def toIterable(self):
        return [getattr(self, key,"") for key in self.__dict__.keys()]
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

class Enrollment():
    idRoster = ""
    idClass = ""
    idSection = ""
    idBlackbaud = ""
    idLocation = ""

    def __str__(self):
        return self.idRoster
    
    def toHeader(self):
        return [key for key in self.__dict__.keys()]
    
    def toIterable(self):
        return [getattr(self, key,"") for key in self.__dict__.keys()]
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
    
class Course():
    idCourse = ""
    idLocation = ""
    courseTitle = ""

    def __str__(self):
        return self.idCourse
    
    def toHeader(self):
        return [key for key in self.__dict__.keys()]
    
    def toIterable(self):
        return [getattr(self, key,"") for key in self.__dict__.keys()]
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
    
class ClassSelection():
    idClass  = ""
    idCourse  = ""
    idLocation  = ""
    classNumber  = ""
    idInstructor  = ""

    def __str__(self):
        return self.idClass
    
    def toHeader(self):
        return [key for key in self.__dict__.keys()]
    
    def toIterable(self):
        return [getattr(self, key,"") for key in self.__dict__.keys()]
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
    
    
class Location():
    idLocation  = "",
    campusCode  = "",
    campusName  = "",
    schoolOU  = ""

    def __str__(self):
        return self.idLocation
    
    def toHeader(self):
        return [key for key in self.__dict__.keys()]
    
    def toIterable(self):
        return [getattr(self, key,"") for key in self.__dict__.keys()]