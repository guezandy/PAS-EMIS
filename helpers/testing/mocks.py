from historical_surveillance.models import District, School
from school.models import Teacher, Student, Course


def generate_district():
    district, _ = District.objects.get_or_create(
        district_code="1",
        district_name="District1",
    )
    return district


def generate_school():
    district = generate_district()
    if School.objects.filter(school_code="1").exists():
        return School.objects.filter(school_code="1").first()

    school, _ = School.objects.get_or_create(
        district_name=district,
        school_code="1",
        school_name="District1",
    )
    return school
