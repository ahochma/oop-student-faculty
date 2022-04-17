''' Exercise #8. Python Programming.'''
##################################################################################
# Question 1 - do not delete this comment
##################################################################################
# Write the classes of question 1 below this line
class Student:

    def __init__(self, name, id, courses):
        self.name = name
        self.id = id
        self.courses = courses
        if not self.is_valid():
            raise ValueError("Invalid grade - has to be between 0 to 100")

    def is_valid(self):
        for course in self.courses:
            if self.courses[course][1] > 100 or self.courses[course][1] < 0:
                return False
        return True

    def __repr__(self):
        prt = "Name: " + self.name + "\n" + "Id: " + self.id+ "\n" + "Courses list: "
        for course in sorted(self.courses):
            prt += course + " " + str(self.courses[course][0]) + " " + str(self.courses[course][1]) + " "
        return prt

    def get_average(self):
        sum_grades = 0
        sum_points = 0
        for course in self.courses:
            sum_grades += (self.courses[course][0]) * (self.courses[course][1])
            sum_points += self.courses[course][0]
        return sum_grades / sum_points

class GradStudent(Student):

    def __init__(self, name, id, courses, degree):
        Student.__init__(self, name, id, courses)
        self.degree = degree

    def __repr__(self):
        prt = Student.__repr__(self)
        prt += "\n" + "Degree: " + self.degree
        return prt

    def get_average(self):
        avg = Student.get_average(self)
        if self.degree == "msc":
            avg *= 1.05
        else:
            avg *= 1.15
        return min(avg, 100.0)

class InternationalStudent(Student):

    def __init__(self, name, id, courses):
        self.american_grades = courses
        if not self.is_valid():
            raise ValueError("Invalid American grade")
        self.num_grades = self.american_to_num()
        Student.__init__(self, name, id, self.num_grades)

    def is_valid(self):
        for course in self.american_grades:
            if self.american_grades[course][1] not in "ABCDF":
                return False
        return True

    def american_to_num(self):
        retdict = {}
        for course in self.american_grades:
            if self.american_grades[course][1] == "A":
                retdict[course] = (self.american_grades[course][0], 100)
            if self.american_grades[course][1] == "B":
                retdict[course] = (self.american_grades[course][0], 90)
            if self.american_grades[course][1] == "C":
                retdict[course] = (self.american_grades[course][0], 80)
            if self.american_grades[course][1] == "D":
                retdict[course] = (self.american_grades[course][0], 70)
            if self.american_grades[course][1] == "F":
                retdict[course] = (self.american_grades[course][0], 60)
        return retdict

    def __repr__(self):
        self.courses = self.american_grades
        return Student.__repr__(self)

    def get_average(self):
        self.courses = self.num_grades
        return Student.get_average(self)

class Faculty():

    def __init__(self, name, students):
        self.name = name
        self.students = students

    def __repr__(self):
        ret = "Faculty of " + self.name + "\n"
        dict = {}
        for std in self.students:
            for course in std.courses:
                dict[course] = dict.get(course, 0) + 1
        for course in sorted(dict, key=dict.get, reverse=True):
            ret += course + " - " + str(dict[course]) + " students" + "\n"
        return ret



## # Use this code to test your implementation:
##A = Student('Or', '123456789', {'calculus': (7, 80), 'algebra': (7, 90), 'programming': (4, 100)})
##print(A)
##print(A.get_average())
##
##B = GradStudent('Guy', '987654321', {'calculus': (7, 84), 'quantummechanics': (4, 95), 'imageprocessing': (4, 90)},'msc')
##print(B)
##print(B.get_average())
##
##C = GradStudent('Dan', '192837465', {'phdseminar': (4, 95), 'programming': (4, 90)}, 'phd')
##print(C)
##print(C.get_average())
##
##D = InternationalStudent('Nadav', '220376541', {'calculus': (7, 'A'), 'babies 101': (2, 'C')})
##print(D)
##print(D.get_average())
##
##E = Faculty('engineering', [A, B, C, D])
##print(E)


##################################################################################
# Question 2 - do not delete this comment
##################################################################################
# Write the classes of question 2 below this line

class PrintOrder:

    def __init__(self, client_name, copies):
        self.client_name = client_name
        self.copies = copies
        if not self.is_valid():
            raise ValueError("Invalid input")

    def is_valid(self):
        if len(self.client_name) == 0 or self.copies < 1:
            return False
        return True

    def __repr__(self):
        ret = "Client name: " + self.client_name + ", " + "Copies: " + str(self.copies) + ", "
        return ret

    def calc_cost(self):
        if issubclass(self.__class__, PosterOrder):
            price = 30 * self.size[0] * self.size[1]
        if issubclass(self.__class__, LetterOrder):
            price = self.paper_prices.get(self.paper_type)
        return price * self.copies

class PosterOrder(PrintOrder):

    def __init__(self, client_name, copies, size):
        PrintOrder.__init__(self, client_name, copies)
        if len(size) != 2 or size[0] < 1 or size[1] < 1:
            raise ValueError("Invalid poster size")
        self.size = size

    def __repr__(self):
        ret = "Poster order: " + PrintOrder.__repr__(self) + "Size: " + str(self.size)
        return ret

class LetterOrder(PrintOrder):

    def __init__(self, client_name, copies, paper_type, paper_prices):
        PrintOrder.__init__(self, client_name, copies)
        if paper_type not in paper_prices:
            raise ValueError("Invalid paper type")
        self.paper_type = paper_type
        self.paper_prices = paper_prices

    def __repr__(self):
        ret = "Letter order: " + PrintOrder.__repr__(self) + "Paper_type: " + self.paper_type
        return ret

class PrintShop:

    def __init__(self):
        self.orders = []
        self.revenues = 0

    def  add_order(self,order):
        self.orders.append(order)

    def print_next_order(self):
        if len(self.orders) > 0:
            self.revenues += self.orders[0].calc_cost()
            self.orders.pop(0)
        else:
            print("There is no order to print")

    def __repr__(self):
        dic = {}
        for order in self.orders:
            dic[order.client_name] = dic.get(order.client_name, 0) + 1
        ret = "Print shop orders:" + '\n'
        for client in dic:
            ret += client + ": " + str(dic.get(client)) + " orders" + "\n"
        ret += "Revenues: " + str(self.revenues)
        return ret



hila = PosterOrder('Hila', 5, (2,1))
hila2 = PosterOrder('Hila', 100, (1,5))
noam = LetterOrder('Noam', 10, 'A5 100gr', {'A4 80gr': 4, 'A5100gr': 7})
s = PrintShop()
noa = PosterOrder('Noa', 0, (2,3))
yuval = LetterOrder('Yuval', 1, 'A3 100gr', {'A4 80gr': 4, 'A5100gr': 7})

 

##### Use this code to test your implementation:	
##poster1 = PosterOrder ("Dvir", 1, (1, 1))
##print (poster1)
##print (poster1.calc_cost())
##
##paper_prices = {"A4 80gr": 3, "A5 100gr": 5}
##letter1 = LetterOrder ("Danielle", 1, "A4 80gr", paper_prices)
##print (letter1)
##print (letter1.calc_cost())
##letter2 = LetterOrder ("Roy", 1, "A5 100gr", paper_prices)
##print (letter2)
##print (letter2.calc_cost())
##letter3 = LetterOrder ("Roy", 5, "A5 100gr", paper_prices)
##print (letter3)
##print (letter3.calc_cost())
##
##print_shop = PrintShop()
##print_shop.add_order(poster1)
##print_shop.add_order(letter1)
##print_shop.add_order(letter2)
##print_shop.add_order(letter3)
##
##print (print_shop)
##
##print_shop.print_next_order() #prints poster1 whose cost is 30
##print (print_shop)

