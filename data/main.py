import random
import os
import datetime
import codecs
from operator import attrgetter
import time

generate_ready = False
try:
    from data.lib.pysat.examples.rc2 import RC2
    from data.lib.pysat.formula import WCNF

    generate_ready = True
except Exception as e:
    generate_ready = False


class Teacher:
    def __init__(self, name, surname, hours=[]):
        self.name = name
        self.surname = surname
        self.unavailable_hours = hours

    def __str__(self):
        return self.surname + " " + self.name

    def __repr__(self):
        return repr((self.name, self.surname))

    def add_unavailable_hours(self, hour):
        self.unavailable_hours.append(hour)
        self.unavailable_hours.sort()

    def del_unavailable_hours(self, hour):
        self.unavailable_hours.remove(hour)


class Room:
    def __init__(self, number, size):
        self.number = number
        self.size = size

    def __str__(self):
        return self.number + "(rozmiar: " + str(self.size) + ")"

    def __repr__(self):
        return repr(self.number)


class Curriculum:
    def __init__(self, name, number_of_students=1):
        self.name = name
        self.number_of_students = number_of_students

    def __str__(self):
        return self.name + "(uczniów: " + str(self.number_of_students) + ")"

    def __repr__(self):
        return repr(self.name)


class Course:
    def __init__(self, name, curriculum, curriculum2, curriculum3, curriculum4, teacher, room=None, lenght=1):
        self.name = name
        self.curriculum = curriculum
        self.curriculum2 = curriculum2
        self.curriculum3 = curriculum3
        self.curriculum4 = curriculum4
        self.teacher = teacher
        self.room = room
        self.lenght = lenght
        self.proposed_room = None

    def __str__(self):
        curriculums = "[" + str(self.curriculum.name)
        room = ""
        if self.curriculum2 is not None:
            curriculums += "|" + str(self.curriculum2.name)
        if self.curriculum3 is not None:
            curriculums += "|" + str(self.curriculum3.name)
        if self.curriculum4 is not None:
            curriculums += "|" + str(self.curriculum4.name)
        if self.room is not None:
            room = " - sala: " + str(self.room.number)
        curriculums += "]"
        return self.name.upper() + " - " + curriculums + " - " + str(self.teacher) + room

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

    global breaks_in_plan
    breaks_in_plan = False

    global last_added
    last_added = "OSTATNIO DODANE ELEMENTY:\n"


def open_from_file(file):
    new_start()
    global teachersArray
    global roomsArray
    global curriculumsArray
    global coursesArray
    global numbers_of_Day
    global numbers_of_Time
    global generated
    global time_array
    global breaks_in_plan
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
    breaks_in_planF = file_lines[2].split("\t")[1]
    if breaks_in_planF == "True":
        breaks_in_plan = True
    else:
        breaks_in_plan = False

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
            # print(l.split("\t"))
            hours = []
            if len(l.split("\t")) == 3:
                for i in l.split("\t")[2].split(","):
                    if i != "":
                        hours.append(int(i))
            teachersArray.append(Teacher(l.split("\t")[0], l.split("\t")[1], hours))
        elif room_now:
            roomsArray.append(Room(l.split("\t")[0], l.split("\t")[1]))
        elif curriculum_now:
            curriculumsArray.append(Curriculum(l.split("\t")[0], l.split("\t")[1]))
        elif course_now:
            # print(l)
            # print(l.split("\t")[1].split(","))
            c1 = curriculumsArray[int(l.split("\t")[1].split(",")[0])]
            c2 = None
            c3 = None
            c4 = None
            room = None
            if len(l.split("\t")[1].split(",")) > 1 and int(l.split("\t")[1].split(",")[1]) != -1:
                c2 = curriculumsArray[int(l.split("\t")[1].split(",")[1])]
            if len(l.split("\t")[1].split(",")) > 2 and int(l.split("\t")[1].split(",")[2]) != -1:
                c3 = curriculumsArray[int(l.split("\t")[1].split(",")[2])]
            if len(l.split("\t")[1].split(",")) > 3 and int(l.split("\t")[1].split(",")[3]) != -1:
                c4 = curriculumsArray[int(l.split("\t")[1].split(",")[3])]
            if int(l.split("\t")[3]) != -1:
                room = roomsArray[int(l.split("\t")[3])]
            coursesArray.append(Course(l.split("\t")[0], c1, c2, c3, c4, teachersArray[int(l.split("\t")[2])], room,
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
    file.write("BREAKS_IN_PLAN\t" + str(breaks_in_plan) + "\n")
    file.write("\n")

    file.write("TEACHERS\n")
    for i in teachersArray:
        file.write(i.name + "\t" + i.surname + "\t")
        for j in i.unavailable_hours:
            file.write(str(j) + ",")
        file.write("\n")
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
        if i.curriculum2 is not None:
            c2 = curriculumsArray.index(i.curriculum2)
        else:
            c2 = -1
        if i.curriculum3 is not None:
            c3 = curriculumsArray.index(i.curriculum3)
        else:
            c3 = -1
        if i.curriculum4 is not None:
            c4 = curriculumsArray.index(i.curriculum4)
        else:
            c4 = -1
        if i.room is not None:
            room_id = roomsArray.index(i.room)
        else:
            room_id = -1
        file.write(
            (i.name + "\t" + str(curriculumsArray.index(i.curriculum)) + "," + str(c2) + "," + str(c3) + "," + str(c4)
             + "\t" + str(teachersArray.index(i.teacher)) + "\t" + str(room_id) + "\t" + str(i.lenght) + "\n"))
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
                    try:
                        file.write(str(coursesArray.index(k)) + "\t")
                    except Exception as e:
                        file.write("-1\t")
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
            f.write("DZIEŃ " + str(d + 1) + "\n")
            for h in range(numbers_of_Time):
                f.write("Godzina " + str(h + 1) + "\t")
                for l in time_array:
                    if l[d * numbers_of_Time + h] is not None and l[d * numbers_of_Time + h].teacher == n:
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


def encode_to_sat():
    formula = []
    soft_map = []
    time_slots = numbers_of_Day * numbers_of_Time
    time_array = list(range(numbers_of_Day * numbers_of_Time))
    # start_time = time.time()

    for k in range(len(coursesArray)):
        curriculum_index1 = curriculumsArray.index(coursesArray[k].curriculum)
        curriculum_index2 = -1
        curriculum_index3 = -1
        curriculum_index4 = -1
        if coursesArray[k].curriculum2 is not None:
            curriculum_index2 = curriculumsArray.index(coursesArray[k].curriculum2)
        if coursesArray[k].curriculum3 is not None:
            curriculum_index3 = curriculumsArray.index(coursesArray[k].curriculum3)
        if coursesArray[k].curriculum4 is not None:
            curriculum_index4 = curriculumsArray.index(coursesArray[k].curriculum4)
        for t1 in range(numbers_of_Time):
            for d in range(numbers_of_Day):
                t = (d * numbers_of_Time) + t1
                formula.append(["-K" + str(k) + "T" + str(t), "P" + str(curriculum_index1) + "T" + str(t)])
                if curriculum_index2 != -1:
                    formula.append(["-K" + str(k) + "T" + str(t), "P" + str(curriculum_index2) + "T" + str(t)])
                if curriculum_index3 != -1:
                    formula.append(["-K" + str(k) + "T" + str(t), "P" + str(curriculum_index3) + "T" + str(t)])
                if curriculum_index4 != -1:
                    formula.append(["-K" + str(k) + "T" + str(t), "P" + str(curriculum_index4) + "T" + str(t)])
    # e = int(time.time() - start_time)
    # print('1) {:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

    for p in range(len(curriculumsArray)):
        for t in range(time_slots):
            klauzula = ["-P" + str(p) + "T" + str(t)]
            for k in range(len(coursesArray)):
                klauzula.append("K" + str(k) + "T" + str(t))
            formula.append(klauzula)
    # e = int(time.time() - start_time)
    # print('2) {:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

    for k in range(len(coursesArray)):
        if coursesArray[k].room is None:
            klauzula = []
            roomsArray2 = sorted(roomsArray, key=attrgetter('size'))
            for s in range(len(roomsArray)):
                klauzula.append("K" + str(k) + "S" + str(roomsArray.index(roomsArray2[s])))
            formula.append(klauzula)
    # e = int(time.time() - start_time)
    # print('3) {:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

    for p in range(len(curriculumsArray)):
        for t in range(time_slots):
            klauzula = ["-P" + str(p) + "T" + str(t)]
            for k in range(len(coursesArray)):
                if curriculumsArray[p] == coursesArray[k].curriculum or curriculumsArray[p] == coursesArray[
                    k].curriculum2 or curriculumsArray[p] == coursesArray[k].curriculum3 or curriculumsArray[p] == \
                        coursesArray[k].curriculum4:
                    klauzula.append("K" + str(k) + "T" + str(t))
            formula.append(klauzula)
    # e = int(time.time() - start_time)
    # print('4) {:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

    for k1 in range(len(coursesArray)):
        for k2 in range(k1 + 1, len(coursesArray)):
            if (coursesArray[k1].curriculum == coursesArray[k2].curriculum or coursesArray[k1].curriculum ==
                coursesArray[k2].curriculum2 or coursesArray[k1].curriculum == coursesArray[k2].curriculum3 or
                coursesArray[k1].curriculum == coursesArray[k2].curriculum4 or
                (coursesArray[k1].curriculum2 is not None and coursesArray[k1].curriculum2 == coursesArray[
                    k2].curriculum) or (
                        coursesArray[k1].curriculum2 is not None and coursesArray[k1].curriculum2 == coursesArray[
                    k2].curriculum2) or (
                        coursesArray[k1].curriculum2 is not None and coursesArray[k1].curriculum2 == coursesArray[
                    k2].curriculum3) or (
                        coursesArray[k1].curriculum2 is not None and coursesArray[k1].curriculum2 == coursesArray[
                    k2].curriculum4) or
                (coursesArray[k1].curriculum3 is not None and coursesArray[k1].curriculum3 == coursesArray[
                    k2].curriculum) or (
                        coursesArray[k1].curriculum3 is not None and coursesArray[k1].curriculum3 == coursesArray[
                    k2].curriculum2) or (
                        coursesArray[k1].curriculum3 is not None and coursesArray[k1].curriculum3 == coursesArray[
                    k2].curriculum3) or (
                        coursesArray[k1].curriculum3 is not None and coursesArray[k1].curriculum3 == coursesArray[
                    k2].curriculum4) or
                (coursesArray[k1].curriculum4 is not None and coursesArray[k1].curriculum4 == coursesArray[
                    k2].curriculum) or (
                        coursesArray[k1].curriculum4 is not None and coursesArray[k1].curriculum4 == coursesArray[
                    k2].curriculum2) or (
                        coursesArray[k1].curriculum4 is not None and coursesArray[k1].curriculum4 == coursesArray[
                    k2].curriculum4) or (
                        coursesArray[k1].curriculum4 is not None and coursesArray[k1].curriculum4 == coursesArray[
                    k2].curriculum4)) or \
                    (coursesArray[k1].teacher == coursesArray[k2].teacher):
                for t in range(time_slots):
                    formula.append(["-K" + str(k1) + "T" + str(t), "-K" + str(k2) + "T" + str(t)])
    # e = int(time.time() - start_time)
    # print('5) {:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

    for k1 in range(len(coursesArray)):
        if coursesArray[k1].room is not None:
            room_index = roomsArray.index(coursesArray[k1].room)
            formula.append(["K" + str(k1) + "S" + str(room_index)])
        for k2 in range(k1 + 1, len(coursesArray)):
            # if coursesArray[k1].room is None and coursesArray[k2].room is None:
            for s in range(len(roomsArray)):
                for t in range(time_slots):
                    formula.append(
                        ["-K" + str(k1) + "T" + str(t), "-K" + str(k2) + "T" + str(t), "-K" + str(k1) + "S" + str(s),
                         "-K" + str(k2) + "S" + str(s)])
    # e = int(time.time() - start_time)
    # print('6) {:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

    for k in range(len(coursesArray)):
        klauzula = []
        for t in range(numbers_of_Time):
            for d in range(numbers_of_Day):
                klauzula.append("K" + str(k) + "T" + str((d * numbers_of_Time) + t))
        formula.append(klauzula)
    # e = int(time.time() - start_time)
    # print('7) {:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

    for k in range(len(coursesArray)):
        for t1 in range(time_slots):
            if t1 % numbers_of_Time != numbers_of_Time - 1:
                for t2 in range(t1+1, time_slots):
                    # l = t2 + coursesArray[k].lenght
                    # if l <= numbers_of_Time:
                    formula.append(["-K" + str(k) + "T" + str(t1), "-K" + str(k) + "T" + str(t2)])
    # e = int(time.time() - start_time)
    # print('8) {:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

    # for k in range(len(coursesArray)):
    #     if int(coursesArray[k].lenght) > 1:
    #         for t in range(time_slots):
    #             if t % numbers_of_Time + int(coursesArray[k].lenght) - 1 <= numbers_of_Time:
    #                 for n in range(int(coursesArray[k].lenght) - 1):
    #                     klauzula = []
    #                     for i in range(n):
    #                         klauzula.append("-K" + str(k) + "T" + str(t + i))
    #                     klauzula.append("K" + str(k) + "T" + str(t + n))
    #                     print(klauzula)
    #                     formula.append(klauzula)

    for k in range(len(coursesArray)):
        for t in range(time_slots):
            if t in coursesArray[k].teacher.unavailable_hours:
                formula.append(["-K" + str(k) + "T" + str(t)])
    # e = int(time.time() - start_time)
    # print('9) {:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

    for k in range(len(coursesArray)):
        needed_size = int(coursesArray[k].curriculum.number_of_students)
        if coursesArray[k].curriculum2 is not None:
            needed_size += int(coursesArray[k].curriculum2.number_of_students)
        if coursesArray[k].curriculum3 is not None:
            needed_size += int(coursesArray[k].curriculum3.number_of_students)
        if coursesArray[k].curriculum4 is not None:
            needed_size += int(coursesArray[k].curriculum4.number_of_students)
        for s in range(len(roomsArray)):
            if needed_size > int(roomsArray[s].size):
                formula.append(["-K" + str(k) + "S" + str(s)])
    # e = int(time.time() - start_time)
    # print('10) {:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

    if not breaks_in_plan:
        for p in range(len(curriculumsArray)):
            for t1 in range(numbers_of_Time):
                for d in range(numbers_of_Day):
                    t = (d * numbers_of_Time) + t1
                    if t % numbers_of_Time < numbers_of_Time - 1:
                        formula.append(["P" + str(p) + "T" + str(t), "-P" + str(p) + "T" + str(t + 1)])
    else:
        for p in range(len(curriculumsArray)):
            for t1 in range(numbers_of_Time):
                for d in range(numbers_of_Day):
                    t = (d * numbers_of_Time) + t1
                    if 0 < t % numbers_of_Time < numbers_of_Time - 1:
                        formula.append(["-P" + str(p) + "T" + str(t), "P" + str(p) + "T" + str(t - 1),
                                         "P" + str(p) + "T" + str(t + 1)])
                        #formula.append(["-P" + str(p) + "T" + str(t), "P" + str(p) + "T" + str(t + 1)])
                        #formula.append(["-P" + str(p) + "T" + str(t), "P" + str(p) + "T" + str(t - 1)])
                    elif t % numbers_of_Time == 0:
                        formula.append(["-P" + str(p) + "T" + str(t), "P" + str(p) + "T" + str(t + 1)])
                    else:
                        formula.append(["-P" + str(p) + "T" + str(t), "P" + str(p) + "T" + str(t - 1)])
                    soft_map.append(len(formula) - 1)

    # e = int(time.time() - start_time)
    # print('11) {:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))
    return formula, soft_map


def encode_to_wcnf(formula, soft_map):
    hard = 10
    soft = 1
    variable_int = 1
    lines_array = []
    f = open("F1tmp.wcnf", "w")
    global variables_map
    variables_map = {}
    index = 0
    for i in formula:
        if index in soft_map:
            line = str(soft) + " "
        else:
            line = str(hard) + " "
        for j in i:
            if j[0] == "-":
                j = j[1:]
                line += "-"
            if j not in variables_map.keys():
                variables_map[j] = variable_int
                variable_int += 1
            line += str(variables_map[j]) + " "
        line += "0\n"
        lines_array.append(line)
        index += 1

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
    global result
    global time_array
    timetable = ""
    time_array.clear()
    i = 0
    while i < len(curriculumsArray):
        time_array.append([None for y in range(numbers_of_Day * numbers_of_Time)])
        i += 1
    for i in variables_map:
        if result[variables_map[i] - 1] > 0:
            if i[0] == "K" and len(i.split("T")) == 2:
                value = coursesArray[int(i.split("T")[0][1:])]
                # print(i + " - " + str(value))
                time_array[curriculumsArray.index(value.curriculum)][int(i.split("T")[1])] = value
                if value.curriculum2 is not None:
                    time_array[curriculumsArray.index(value.curriculum2)][int(i.split("T")[1])] = value
                if value.curriculum3 is not None:
                    time_array[curriculumsArray.index(value.curriculum3)][int(i.split("T")[1])] = value
                if value.curriculum4 is not None:
                    time_array[curriculumsArray.index(value.curriculum4)][int(i.split("T")[1])] = value
            elif i[0] == "K" and len(i.split("S")) == 2:
                value = coursesArray[int(i.split("S")[0][1:])]
                value.room = roomsArray[int(i.split("S")[1])]
    # print(time_array)
    # print(variables)
    # print(cost)
    return time_array


def generate():
    start_time = time.time()
    global generated
    formula, soft_map = encode_to_sat()
    encode_to_wcnf(formula, soft_map)
    if solve_wcnf():
        generated = True
        # e = int(time.time() - start_time)
        # print('KONIEC) {:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))
        return True, show_result()
    else:
        return False, []


def remove_curriculum(id):
    element_to_del = []
    for x in coursesArray:
        if x.curriculum == curriculumsArray[id]:
            x.curriculum = None
            if x.curriculum4 is not None:
                x.curriculum = x.curriculum4
                x.curriculum4 = None
            elif x.curriculum3 is not None:
                x.curriculum = x.curriculum3
                x.curriculum3 = None
            elif x.curriculum2 is not None:
                x.curriculum = x.curriculum2
                x.curriculum2 = None
            else:
                element_to_del.append(x)
        elif x.curriculum2 == curriculumsArray[id]:
            x.curriculum2 = None
        elif x.curriculum3 == curriculumsArray[id]:
            x.curriculum3 = None
        elif x.curriculum4 == curriculumsArray[id]:
            x.curriculum4 = None
    for x in element_to_del:
        coursesArray.remove(x)
    del curriculumsArray[id]


def remove_teacher(id):
    element_to_del = []
    for x in coursesArray:
        if x.teacher == teachersArray[id]:
            element_to_del.append(x)
    for x in element_to_del:
        coursesArray.remove(x)
    del teachersArray[id]


def remove_room(id):
    for x in coursesArray:
        if x.room == roomsArray[id]:
            x.room = None
    del roomsArray[id]


teachersArray = []
roomsArray = []
curriculumsArray = []
coursesArray = []
result = []
time_array = []
generated = False
numbers_of_Time = 8
numbers_of_Day = 5
breaks_in_plan = False
last_added = ""

new_start()
