import re
import random

def email_regex(email):
    '''
    Matches a string against a regex to determine it it has @cpp.edu suffix

    Keyword arguments:
        email (string)
    '''
    if not re.match(r"^[_A-Za-z0-9-]+@cpp\.edu$", email):
        return False
    else:
        return True

def map_options(course):
    '''Creates a mapping between option ids and ranks and weights

    Keyword arguments:
        course (ProfessorCourseMapping)
    '''
    option_map = {}
    for q in course.config.questions.all():
        for o in q.question_options.all():
            option_map.update({o.id: {'rank': o.rank, 'weight': q.relative_weight}})
    return option_map

def get_larger_groups(size, data):
    '''Partitions a list into groups the number of 'size' 

    Keyword arguments:
        size (int) 
        data (list) -- should be a sorted list of StudentCourseMappings, but can take any list data
    '''
    larger_group_length = len(data)/size
    remainder = len(data)%size
    larger_groups = []
    for i in range(0, size):
        larger_groups.append(data[i*larger_group_length:(i+1)*larger_group_length])
    if remainder != 0:
        larger_groups[-1] += data[-remainder:]
    return larger_groups

def group_students(size, data):
    '''Picks randomly from each of larger groups to populate groups of length 'size'. Remainder elements
        are either randomly assigned to groups or made into another group if length of remainder
        is 'size' - 1.

    Keyword arguments:
        size (int)
        data (list) -- should be a sorted list of StudentCourseMappings, but can take any list data
    '''
    larger_groups = get_larger_groups(size, data)
    groups = []
    while len(larger_groups[0]) != 0:
        group = []
        for lst in larger_groups:
            random_index = random.randint(0, len(lst) - 1)
            group.append(lst.pop(random_index))
        groups.append(group)

    remainders = larger_groups[-1]
    if len(remainders) > 0:
        if len(remainders) == size - 1: # This is a bit iffy
            groups.append(remainders)
        else:
            while len(remainders) != 0:
                random_index = random.randint(0, len(groups) - 1)
                if len(groups[random_index]) == size:
                    groups[random_index].append(remainders.pop())
    return groups


def rank_students(student_course_mappings, course):
    '''Assigns ranks to students based on option.rank and question.relative_weight

    Keyword arguments:
        student_course_mappings (list of StudentCourseMappings)
        course (Course) -- course should match the course attribute in all student_course_mappings
    '''
    option_map = map_options(course)

    for student in student_course_mappings:
        rank = 0
        for option in student.options.all():
            opt = option_map[option.id]
            rank += opt['rank']*opt['weight']
        student.rank = rank

    students = sorted(student_course_mappings, key=lambda k:k.rank)

    return students