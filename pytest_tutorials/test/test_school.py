import pytest
from source.school import Classroom, Teacher, Student, Toomanystudents

# Fixtures (Characters from Harry Potter)
@pytest.fixture
def harry():
    return Student("Harry Potter")

@pytest.fixture
def hermione():
    return Student("Hermione Granger")

@pytest.fixture
def ron():
    return Student("Ron Weasley")

@pytest.fixture
def dumbledore():
    return Teacher("Albus Dumbledore")

@pytest.fixture
def snape():
    return Teacher("Severus Snape")

@pytest.fixture
def initial_students(harry, hermione, ron):
    return [harry, hermione, ron]

@pytest.fixture
def defense_classroom(dumbledore, initial_students):
    return Classroom(dumbledore, initial_students, "Defense Against the Dark Arts")

# Parametrized test for adding students under 10
@pytest.mark.parametrize("student_name", [
    "Neville Longbottom",
    "Draco Malfoy",
    "Luna Lovegood",
    "Ginny Weasley",
    "Fred Weasley",
    "George Weasley",
    "Cho Chang"
])
def test_add_students_successfully(defense_classroom, student_name):
    new_student = Student(student_name)
    defense_classroom.add_students(new_student)
    assert new_student in defense_classroom.students

# Test exception when too many students enroll
def test_too_many_students_exception(defense_classroom):
    # Fill up to 10 students
    extra_students = [Student(f"Student {i}") for i in range(7)]
    for student in extra_students:
        defense_classroom.add_students(student)

    # The 11th student (Hogwarts max cap test)
    with pytest.raises(Toomanystudents):
        defense_classroom.add_students(Student("Random First Year"))

# Test removing a student
def test_remove_student(defense_classroom):
    defense_classroom.remove_students("Hermione Granger")
    assert all(student.name != "Hermione Granger" for student in defense_classroom.students)

# Test changing the teacher (Snape taking over 😬)
def test_change_teacher(defense_classroom, snape):
    defense_classroom.change_teacher(snape)
    assert defense_classroom.teacher == snape