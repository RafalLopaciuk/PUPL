import random
import os
import datetime
import codecs





class Teacher:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.unavailable_hours = []

    def __str__(self):
        return self.surname + " " + self.name

    def __repr__(self):
        return repr((self.name, self.surname))

    def add_unavailable_hours(self, hour):
        self.unavailable_hours.append(hour)

    def del_unavailable_hours(self, hour):
        self.unavailable_hours.remove(hour)


class Room:
    def __init__(self, number, size):
        self.number = number
        self.size = size

    def __str__(self):
        return self.number + " - rozmiar: " + str(self.size)

    def __repr__(self):
        return repr(self.number)


class Curriculum:
    def __init__(self, name, number_of_students=1):
        self.name = name
        self.number_of_students = number_of_students

    def __str__(self):
        return self.name + " - uczniów: " + str(self.number_of_students)

    def __repr__(self):
        return repr(self.name)


class Course:
    def __init__(self, name, curriculum, teacher, room=None, lenght=1):
        self.name = name
        self.curriculum = curriculum
        self.teacher = teacher
        self.room = room
        self.lenght = lenght

    def __str__(self):
        if self.room is not None:
            return self.name.upper() + " (" + str(self.lenght) + "h) - " + str(self.curriculum.name) + " - " \
                   + str(self.teacher) + " - sala:" + str(self.room.number)
        else:
            return self.name.upper() + " (" + str(self.lenght) + "h) - " + str(self.curriculum.name) + " - " \
                   + str(self.teacher)

    def __repr__(self):
        return repr(self.name)


def find_teacher_by_name(name):
    for x in teachersArray:
        if str(x) in name:
            return x
    return None


def new_start():
    global teachersArray
    global roomsArray
    global curriculumsArray
    global coursesArray
    teachersArray.clear()
    roomsArray.clear()
    curriculumsArray.clear()
    coursesArray.clear()
    global numbers_of_Time
    global numbers_of_Day
    numbers_of_Time = 8
    numbers_of_Day = 5

    global result
    global time_array
    global generated
    result = []
    time_array = []
    generated = False


def open_from_file(file):
    global teachersArray
    global roomsArray
    global curriculumsArray
    global coursesArray
    global numbers_of_Day
    global numbers_of_Time
    global generated
    global time_array
    new_start()
    file_lines = file.read().split("\n")
    teachers_now = False
    room_now = False
    curriculum_now = False
    course_now = False
    time_array_now = False
    start = 0

    numbers_of_Day = int(file_lines[0].split("\t")[1])
    numbers_of_Time = int(file_lines[1].split("\t")[1])

    for l in file_lines:
        if l is "":
            teachers_now = False
            curriculum_now = False
            room_now = False
            course_now = False
            time_array_now = False
        elif l == "TEACHERS":
            teachers_now = True
        elif l == "ROOMS":
            room_now = True
        elif l == "CURRICULUMS":
            curriculum_now = True
        elif l == "COURSES":
            course_now = True
        elif "GENERATE" in l:
            if l.split("\t")[1] == "True":
                generated = True
        elif l == "TIME ARRAY":
            time_array_now = True
        elif teachers_now:
            teachersArray.append(Teacher(l.split("\t")[0], l.split("\t")[1]))
        elif room_now:
            roomsArray.append(Room(l.split("\t")[0], l.split("\t")[1]))
        elif curriculum_now:
            curriculumsArray.append(Curriculum(l.split("\t")[0], l.split("\t")[1]))
        elif course_now:
            if int(l.split("\t")[3]) == -1:
                coursesArray.append(Course(l.split("\t")[0], curriculumsArray[int(l.split("\t")[1])],
                                           teachersArray[int(l.split("\t")[2])], None, int(l.split("\t")[4])))
            else:
                coursesArray.append(Course(l.split("\t")[0], curriculumsArray[int(l.split("\t")[1])],
                                           teachersArray[int(l.split("\t")[2])], roomsArray[int(l.split("\t")[3])],
                                           int(l.split("\t")[4])))
        elif time_array_now:
            if "CLASS" in l:
                time_array.append([])
                start = int(l.split("\t")[1])
            else:
                for x in l.split("\t"):
                    if x:
                        if x == "-1":
                            time_array[start].append(None)
                        else:
                            time_array[start].append(coursesArray[int(x)])

    # print(teachersArray)
    # print(roomsArray)
    # print(curriculumsArray)
    # print(coursesArray)
    # print("Time array+ " + str(time_array))


def save_to_file(file):
    file.write("NUMBER_OF_DAY\t" + str(numbers_of_Day) + "\n")
    file.write("NUMBER_OF_TIME\t" + str(numbers_of_Time) + "\n")
    file.write("\n")

    file.write("TEACHERS\n")
    for i in teachersArray:
        file.write(i.name + "\t" + i.surname + "\n")
    file.write("\n")

    file.write("ROOMS\n")
    for i in roomsArray:
        file.write(i.number + "\t" + str(i.size) + "\n")
    file.write("\n")

    file.write("CURRICULUMS\n")
    for i in curriculumsArray:
        file.write(i.name + "\t" + str(i.number_of_students) + "\n")
    file.write("\n")

    file.write("COURSES\n")
    for i in coursesArray:
        if i.room is not None:
            room_id = roomsArray.index(i.room)
        else:
            room_id = -1
        file.write(
            (i.name + "\t" + str(curriculumsArray.index(i.curriculum)) + "\t" + str(
                teachersArray.index(i.teacher))
             + "\t" + str(room_id) + "\t" + str(i.lenght) + "\n"))
    file.write("\n")

    file.write("GENERATE" + "\t" + str(generated) + "\n")
    file.write("\n")

    if generated:
        file.write("TIME ARRAY\n")
        index = 0
        for j in time_array:
            file.write("CLASS\t" + str(index) + "\n")
            for k in j:
                if k is not None:
                    file.write(str(coursesArray.index(k)) + "\t")
                else:
                    file.write("-1\t")
            file.write("\n")
            index += 1


def export_project(path):
    path = path + "/export " + str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M"))
    if not os.path.exists(path + "/Nauczyciele"):
        os.makedirs(path + "/Nauczyciele")
    for n in teachersArray:
        f = codecs.open(path + "/Nauczyciele/" + str(n.name) + " " + str(n.surname) + ".txt", "w", "utf-8")
        for d in range(numbers_of_Day):
            f.write("DZIEŃ " + str(d+1) + "\n")
            for h in range(numbers_of_Time):
                f.write("Godzina " + str(h+1) + "\t")
                for l in time_array:
                    if l[d*numbers_of_Time + h] is not None and l[d * numbers_of_Time + h].teacher == n:
                        f.write(str(l[d * numbers_of_Time + h]))
                        break
                f.write("\n")
            f.write("\n")
        f.close()
    if not os.path.exists(path + "/Klasy"):
        os.makedirs(path + "/Klasy")
    for n in curriculumsArray:
        f = codecs.open(path + "/Klasy/" + str(n.name) + ".txt", "w", "utf-8")
        for d in range(numbers_of_Day):
            f.write("DZIEŃ " + str(d + 1) + "\n")
            for h in range(numbers_of_Time):
                f.write("Godzina " + str(h + 1) + "\t")
                for l in time_array:
                    if l[d * numbers_of_Time + h] is not None and l[d * numbers_of_Time + h].curriculum == n:
                        f.write(str(l[d * numbers_of_Time + h]))
                        break
                f.write("\n")
            f.write("\n")
        f.close()


def init():
    c1 = Curriculum("1A", 20)
    curriculumsArray.append(c1)
    c2 = Curriculum("1B", 20)
    curriculumsArray.append(c2)
    c3 = Curriculum("1C", 15)
    curriculumsArray.append(c3)
    c4 = Curriculum("2A", 20)
    curriculumsArray.append(c4)
    c5 = Curriculum("2B", 20)
    curriculumsArray.append(c5)
    c6 = Curriculum("2C", 15)
    curriculumsArray.append(c6)
    c7 = Curriculum("3A", 20)
    curriculumsArray.append(c7)
    c8 = Curriculum("3B", 20)
    curriculumsArray.append(c8)
    c9 = Curriculum("3C", 15)
    curriculumsArray.append(c9)

    t1 = Teacher("Jan", "Kowalski")
    teachersArray.append(t1)
    t2 = Teacher("Marek", "Nowak")
    teachersArray.append(t2)
    t3 = Teacher("Zbigniew", "Wloń")
    teachersArray.append(t3)
    t4 = Teacher("Tadeusz", "Norek")
    teachersArray.append(t4)
    t5 = Teacher("Ewa", "Kow-Schreder")
    teachersArray.append(t5)
    t6 = Teacher("Jarosław", "Naurek")
    teachersArray.append(t6)

    r1 = Room("10", 25)
    roomsArray.append(r1)
    r2 = Room("20", 25)
    roomsArray.append(r2)
    r3 = Room("101", 30)
    roomsArray.append(r3)
    r4 = Room("102", 30)
    roomsArray.append(r4)
    r5 = Room("211", 30)
    roomsArray.append(r5)
    r6 = Room("Sala gimnastyczna 1", 150)
    roomsArray.append(r6)

    k1 = Course("Matematyka", c1, t1, r1)
    coursesArray.append(k1)
    k1 = Course("Matematyka", c2, t1, r1)
    coursesArray.append(k1)
    k1 = Course("Matematyka", c3, t1, r1)
    coursesArray.append(k1)
    k1 = Course("Matematyka", c4, t1, r1)
    coursesArray.append(k1)
    k1 = Course("Matematyka", c5, t1, r1)
    coursesArray.append(k1)
    k1 = Course("Matematyka", c6, t1, r1)
    coursesArray.append(k1)
    k1 = Course("Matematyka", c7, t1, r1)
    coursesArray.append(k1)
    k1 = Course("Matematyka", c8, t1, r1)
    coursesArray.append(k1)
    k1 = Course("Matematyka", c9, t1, r1)
    coursesArray.append(k1)

    k1 = Course("Język polski", c1, t2, r2)
    coursesArray.append(k1)
    k1 = Course("Język polski", c2, t2, r2)
    coursesArray.append(k1)
    k1 = Course("Język polski", c3, t2, r2)
    coursesArray.append(k1)
    k1 = Course("Język polski", c4, t2, r2)
    coursesArray.append(k1)
    k1 = Course("Język polski", c5, t2, r2)
    coursesArray.append(k1)
    k1 = Course("Język polski", c6, t2, r2)
    coursesArray.append(k1)
    k1 = Course("Język polski", c7, t2, r2)
    coursesArray.append(k1)
    k1 = Course("Język polski", c8, t2, r2)
    coursesArray.append(k1)
    k1 = Course("Język polski", c9, t2, r2)
    coursesArray.append(k1)

    k1 = Course("Fizyka", c1, t3, r3)
    coursesArray.append(k1)
    k1 = Course("Fizyka", c2, t3, r3)
    coursesArray.append(k1)
    k1 = Course("Fizyka", c3, t3, r3)
    coursesArray.append(k1)
    k1 = Course("Fizyka", c4, t3, r3)
    coursesArray.append(k1)
    k1 = Course("Fizyka", c5, t3, r3)
    coursesArray.append(k1)
    k1 = Course("Fizyka", c6, t3, r3)
    coursesArray.append(k1)
    k1 = Course("Fizyka", c7, t3, r3)
    coursesArray.append(k1)
    k1 = Course("Fizyka", c8, t3, r3)
    coursesArray.append(k1)
    k1 = Course("Fizyka", c9, t3, r3)
    coursesArray.append(k1)

    k1 = Course("Chemia", c1, t4, r4)
    coursesArray.append(k1)
    k1 = Course("Chemia", c2, t4, r4)
    coursesArray.append(k1)
    k1 = Course("Chemia", c3, t4, r4)
    coursesArray.append(k1)
    k1 = Course("Chemia", c4, t4, r4)
    coursesArray.append(k1)
    k1 = Course("Chemia", c5, t4, r4)
    coursesArray.append(k1)
    k1 = Course("Chemia", c6, t4, r4)
    coursesArray.append(k1)
    k1 = Course("Chemia", c7, t4, r4)
    coursesArray.append(k1)
    k1 = Course("Chemia", c8, t4, r4)
    coursesArray.append(k1)
    k1 = Course("Chemia", c9, t4, r4)
    coursesArray.append(k1)

    k1 = Course("Język niemiecki", c1, t5, r5)
    coursesArray.append(k1)
    k1 = Course("Język niemiecki", c2, t5, r5)
    coursesArray.append(k1)
    k1 = Course("Język niemiecki", c3, t5, r5)
    coursesArray.append(k1)
    k1 = Course("Język niemiecki", c4, t5, r5)
    coursesArray.append(k1)
    k1 = Course("Język niemiecki", c5, t5, r5)
    coursesArray.append(k1)
    k1 = Course("Język niemiecki", c6, t5, r5)
    coursesArray.append(k1)
    k1 = Course("Język niemiecki", c7, t5, r5)
    coursesArray.append(k1)
    k1 = Course("Język niemiecki", c8, t5, r5)
    coursesArray.append(k1)
    k1 = Course("Język niemiecki", c9, t5, r5)
    coursesArray.append(k1)

    k1 = Course("WF", c1, t6, r6)
    coursesArray.append(k1)
    k1 = Course("WF", c2, t6, r6)
    coursesArray.append(k1)
    k1 = Course("WF", c3, t6, r6)
    coursesArray.append(k1)
    k1 = Course("WF", c4, t6, r6)
    coursesArray.append(k1)
    k1 = Course("WF", c5, t6, r6)
    coursesArray.append(k1)
    k1 = Course("WF", c6, t6, r6)
    coursesArray.append(k1)
    k1 = Course("WF", c7, t6, r6)
    coursesArray.append(k1)
    k1 = Course("WF", c8, t6, r6)
    coursesArray.append(k1)
    k1 = Course("WF", c9, t6, r6)
    coursesArray.append(k1)


def encode_to_sat():
    formula = []
    time_array = list(range(numbers_of_Day * numbers_of_Time))
    for i in range(len(coursesArray)):
        curriculum_index = curriculumsArray.index(coursesArray[i].curriculum)
        all = []
        for k in range(numbers_of_Day * numbers_of_Time):
            all.append("K" + str(i) + "T" + str(k))
            for j in range(i):
                if coursesArray[i].curriculum == coursesArray[j].curriculum or \
                        coursesArray[i].teacher == coursesArray[j].teacher:
                    clausule = ["-K" + str(j) + "T" + str(k), "-K" + str(i) + "T" + str(k)]
                    formula.append(clausule)
            clausule = ["-K" + str(i) + "T" + str(k), "P" + str(curriculum_index) + "T" + str(k)]
            formula.append(clausule)
        formula.append(all)
    # print(formula)
    # print(len(coursesArray) * numbersOfTime)
    return formula


def encode_to_wcnf(formula):
    hard = 10
    variable_int = 1
    lines_array = []
    f = open("F1tmp.wcnf", "w")
    # formula = [["X1", "X2"], ["X2", "X3"]]
    global variables_map
    variables_map = {}
    for i in formula:
        line = str(hard) + " "
        for j in i:
            # print(j)
            if j[0] == "-":
                j = j[1:]
                line += "-"
            if j not in variables_map.keys():
                variables_map[j] = variable_int
                variable_int += 1
            line += str(variables_map[j]) + " "
        line += "0\n"
        lines_array.append(line)

    f.write("p wcnf " + str(len(variables_map)) + " " + str(len(formula)) + " " + str(hard) + "\r")
    for l in lines_array:
        f.write(l)
    f.close()


def solve_wcnf():
    wcnf = WCNF(from_file='F1tmp.wcnf')
    global result
    global cost
    with RC2(wcnf) as rc2:
        result = rc2.compute()
        cost = rc2.cost
        # for m in rc2.enumerate():
        #         #    print(m)
        #         # print(rc2.adapt_am1())
        #         # print(result)

    os.remove("F1tmp.wcnf")

    if result:
        return True
    else:
        return False


def show_result():
    # timetable = ""
    # variables = {}
    # time_array = [[] for y in range(numbers_of_Time)]
    # for i in variables_map:
    #     if result[variables_map[i]-1] > 0:
    #         variables[i] = True
    #         if i[0] == "K":
    #             # print(int(i.split("T")[0][1:]))
    #             value = coursesArray[int(i.split("T")[0][1:])]
    #             time_array[int(i.split("T")[1])].append(value)
    #     else:
    #         variables[i] = False
    #

    # print(variables)
    # print(time_array)
    # time = 1
    # for i in time_array:
    #     line = "Godzina " + str(time) + ":"
    #     for j in i:
    #         line += " [" + str(j) + "]"
    #     # print("Godzina " + str(time) + ": " + str(i))
    #     # print("123")
    #     timetable += line + "\n"
    #     time += 1

    global result
    global time_array
    # print(result)
    timetable = ""
    variables = {}
    time_array.clear()
    i = 0
    while i < len(curriculumsArray):
        time_array.append([None for y in range(numbers_of_Day * numbers_of_Time)])
        i += 1
    for i in variables_map:
        if result[variables_map[i] - 1] > 0:
            variables[i] = True
            if i[0] == "K":
                # print(int(i.split("T")[0][1:]))
                value = coursesArray[int(i.split("T")[0][1:])]
                time_array[curriculumsArray.index(value.curriculum)][int(i.split("T")[1])] = value
        else:
            variables[i] = False
    # print(time_array)
    return time_array
    # print(variables)
    # print(cost)


def generate1():
    global generated
    encode_to_wcnf(encode_to_sat())
    print("Time to solve")
    if solve_wcnf():
        generated = True
        return True, show_result()
    else:
        return False, []


def add_teacher(name, surname):
    t = Teacher(name, surname)
    teachersArray.append(t)


# if __name__ == "__main__":
teachersArray = []
roomsArray = []
curriculumsArray = []
coursesArray = []
result = []
time_array = []
generated = False
numbers_of_Time = 8
numbers_of_Day = 5

new_start()
# init()
# encode_to_wcnf(encode_to_sat())
# solve_wcnf()
# print(show_result())
# print(123)
