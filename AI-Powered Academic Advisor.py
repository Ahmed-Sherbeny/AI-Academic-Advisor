# Ahmed Mohammed EL Sherbeny

import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from collections import defaultdict
import itertools

# ------------------- Step 1: Curriculum Graph -------------------

# Courses and courses prerequisites definition
courses = {
    'CS101': [],
    'CS102': ['CS101'],
    'CS103': ['CS102'],
    'CS201': ['CS102'],
    'CS202': ['CS102'],
    'CS203': ['CS102'],
    'CS204': ['CS202'],
    'CS301': ['CS201'],
    'CS302': ['CS201', 'CS203'],
    'CS303': ['CS102'],
    'CS304': ['CS302'],
    'CS305': ['CS102'],
    'CS306': ['CS204', 'CS305'],
    'CS307': ['CS303']
}

# Create a directed graph
G = nx.DiGraph()
for course, prereqs in courses.items():
    G.add_node(course)
    for prereq in prereqs:
        G.add_edge(prereq, course)

# Visualize graph
pos = nx.spring_layout(G, seed=42) 
plt.figure(figsize=(20, 13))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue',
        font_size=10, font_weight='bold', arrows=True, arrowsize=20, edgecolors='black')
plt.title("University Curriculum Graph")
plt.show()

# ------------------- Step 2: Simulate Students -------------------

NUM_STUDENTS = 100
MAX_PASSED_COURSES = 10
INTERESTS = ['AI', 'Security', 'Data Science', 'Software', 'Systems']

def has_prerequisites(course, passed_courses):
    return all(prereq in passed_courses for prereq in courses[course])

students = []

for i in range(NUM_STUDENTS):
    passed_courses = set()
    grades = {}
    course_list = list(courses.keys())
    random.shuffle(course_list)

    for course in course_list:
        if len(passed_courses) >= MAX_PASSED_COURSES:
            break
        if has_prerequisites(course, passed_courses):
            grade = round(np.clip(np.random.normal(loc=3.0, scale=0.7), 0.0, 4.0), 2)
            grades[course] = grade
            if grade >= 2.0:
                passed_courses.add(course)

    gpa = round(np.mean(list(grades.values())), 2) if grades else 0.0
    interests = random.sample(INTERESTS, k=random.randint(1, 2))

    student = {
        'id': i + 1,
        'passed_courses': sorted(list(passed_courses)),
        'grades': grades,
        'GPA': gpa,
        'interests': interests
    }
    students.append(student)

# ------------------- Step 3: Term-by-Term Planning -------------------

MAX_TOTAL_COURSES = 14
MAX_TERM_LOAD = 5
MIN_TERM_LOAD = 3

def get_eligible_courses(passed, failed):
    return [c for c in courses 
            if c not in passed and c not in failed and has_prerequisites(c, passed)]

for student in students:
    term_plan = []
    passed = set(student['passed_courses'])
    failed = {c for c, g in student['grades'].items() if g < 2.0}
    total_taken = len(student['grades'])

    while total_taken < MAX_TOTAL_COURSES:
        term = []

        for course in list(failed):
            if len(term) >= MAX_TERM_LOAD:
                break
            term.append(course)
            failed.remove(course)
            total_taken += 1

        eligible = get_eligible_courses(passed, failed)
        random.shuffle(eligible)
        for course in eligible:
            if len(term) >= MAX_TERM_LOAD:
                break
            term.append(course)
            passed.add(course)
            total_taken += 1

        if term:
            term_plan.append(term)

    student['term_plan'] = term_plan

# ------------------- Part 2: Q-Learning (Reinforcement Learning) -------------------

Q = defaultdict(float)
ALPHA = 0.5
GAMMA = 0.9
EPSILON = 0.2
NUM_EPISODES = 500

def encode_state(student, term):
    return (
        tuple(sorted(student['passed_courses'])),
        round(student['GPA'], 1),
        term,
        tuple(student['interests'])
    )

def available_actions(passed_courses):
    eligible = get_eligible_courses(set(passed_courses), set())
    return list(itertools.combinations(eligible, 3)) + \
           list(itertools.combinations(eligible, 4)) + \
           list(itertools.combinations(eligible, 5))

def compute_reward(courses, student):
    reward = 0
    for course in courses:
        if course.startswith("CS3") and "AI" in student['interests']:
            reward += 1
        if course.startswith("CS30") and "Security" in student['interests']:
            reward += 1
        if course == "CS304" and "Data Science" in student['interests']:
            reward += 1
    if student['GPA'] > 3.0:
        reward += 2
    reward += len(student['passed_courses']) / 14.0 * 2
    return reward

rl_students = students[:100]

for episode in range(NUM_EPISODES):
    for student in rl_students:
        passed = set(student['passed_courses'])
        GPA = student['GPA']
        interests = student['interests']
        term = 1

        while len(passed) < 14:
            state = (tuple(sorted(passed)), round(GPA, 1), term, tuple(interests))
            actions = available_actions(passed)
            if not actions:
                break

            if random.random() < EPSILON:
                action = random.choice(actions)
            else:
                action = max(actions, key=lambda a: Q[(state, a)], default=random.choice(actions))

            passed.update(action)
            GPA = round(np.clip(np.random.normal(loc=3.0, scale=0.7), 0.0, 4.0), 2)
            next_state = (tuple(sorted(passed)), round(GPA, 1), term + 1, tuple(interests))
            reward = compute_reward(action, student)

            future_q = max([Q[(next_state, a)] for a in available_actions(passed)], default=0)
            Q[(state, action)] += ALPHA * (reward + GAMMA * future_q - Q[(state, action)])
            term += 1

# ------------------- Recommendation Feature -------------------

def recommend_next_term_courses(student, term, Q_table):
    passed = set(student['passed_courses'])
    state = (
        tuple(sorted(passed)),
        round(student['GPA'], 1),
        term,
        tuple(student['interests'])
    )
    actions = available_actions(passed)
    
    if not actions:
        return []

    best_action = max(actions, key=lambda a: Q_table.get((state, a), 0))
    return list(best_action)

# ------------------- Output: Profiles + AI Recommendations -------------------

print("\n--- Sample Student Profiles ---")
for student in students[:100]:
    print(f"\nStudent {student['id']}")
    print("  Passed Courses:", student['passed_courses'])
    print("  GPA:", student['GPA'])
    print("  Interests:", student['interests'])
    print("  Term Plan:")
    for t_index, term in enumerate(student['term_plan'], 1):
        print(f"    Term {t_index}: {term}")

print("\n--- AI-Based Next-Term Recommendations ---")
for student in rl_students[:100]:
    term = len(student['term_plan']) + 1
    recommended = recommend_next_term_courses(student, term, Q)
    print(f"\nStudent {student['id']} (Interests: {student['interests']})")
    print(f"  Recommended Courses for Term {term}: {recommended}")
