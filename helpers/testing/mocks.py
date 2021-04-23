from historical_surveillance.models import District, School
from school.models import Teacher, Student, Course, Subject, SubjectGroup, CourseGrade


def generate_district():
    district, created = District.objects.get_or_create(
        district_code="1",
        district_name="District1",
        created_at="2021-04-20",
        created_by="andrew",
        updated_by="andrew",
        updated_at="2021-04-20",
    )
    return district


def generate_school():
    district = generate_district()
    if School.objects.filter(school_code="1").exists():
        return School.objects.filter(school_code="1").first()

    school, created = School.objects.get_or_create(
        district_name=district,
        school_code="1",
        school_name="District1",
        created_at="2021-04-20",
        created_by="andrew",
        updated_by="andrew",
        updated_at="2021-04-20",
    )
    return district
