import base64
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
from .models import School


def get_image() -> object:
    # create a byte buffer for the image to save
    buffer = BytesIO()
    # create a plot with the use of bytesio object
    plt.savefig(buffer, format='png')
    # set the cursor to the beginning of the screen
    buffer.seek(0)
    # retrieve the entire content of the file
    image_png = buffer.getvalue()
    # encoding and decoding
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    # free the memory of the buffer
    buffer.close()
    return graph


def get_grade_plot(**kwargs):
    plt.switch_backend('AGG')
    # the enrollment
    x = kwargs.get('x')
    # year = the academic year
    year = kwargs.get('academic_year')
    # the grade
    z = kwargs.get('z')

    school_name = kwargs.get('name_of_school')
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.bar(z, x, width=0.40, color='g', label='if data exist by gender,bottom values ='
                                              ' female enrollment, one value (male = female)'
           , alpha=0.5)
    ax.set_ylabel("Enrollment / Grade / Sex")

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14)
        # specify integer or one of preset strings, e.g.
        # tick.label.set_fontsize('x-small')
        tick.label.set_rotation('vertical')
    for bar in ax.patches:
        # Using Matplotlib annotate function and
        # passing the coordinates where the annotation shall be done
        # x-coordinate: bar.get_x() + bar.get_width() / 2
        # y-coordinate: bar.get_height()
        # free space to be left to make graph pleasing: (0, 8)
        # ha and va stand for the horizontal and vertical alignment
        plt.annotate(format(bar.get_height(), '.2f'),
                     (bar.get_x() + bar.get_width() / 2,
                      bar.get_height()), ha='center', va='center',
                     size=7, xytext=(0, 5),
                     textcoords='offset points')
        school_title = School.objects.filter(id=school_name).distinct().values_list('school_name', flat=True)
        school_name_title = school_title[0]
        plt.title("Enrollment for " + school_name_title + " - Academic Year " + year)
        plt.xlabel('Grades')
        ax.set_ylim([0, max(x) + 12])

        ax.legend()
    plt.tight_layout()
    # plt.grid()
    graph = get_image()
    return graph


def get_district_grade_plot(**kwargs):
    plt.switch_backend('AGG')
    # the enrollment
    x = kwargs.get('x')
    # year = the academic year
    academic_year = kwargs.get('academic_year')
    # the grade
    z = kwargs.get('z')
    school = kwargs.get('name_of_school')
    district = kwargs.get('district')
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.bar(school, x, width=0.40, color='g', label='if data exist by gender,bottom values ='
                                                   ' female enrollment, one value (male = female)'
           , alpha=0.5)
    ax.set_ylabel("District Enrollment / Grade / Sex")

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14)
        # specify integer or one of preset strings, e.g.
        # tick.label.set_fontsize('x-small')
        tick.label.set_rotation('vertical')
    for bar in ax.patches:
        # Using Matplotlib annotate function and
        # passing the coordinates where the annotation shall be done
        # x-coordinate: bar.get_x() + bar.get_width() / 2
        # y-coordinate: bar.get_height()
        # free space to be left to make graph pleasing: (0, 8)
        # ha and va stand for the horizontal and vertical alignment
        plt.annotate(format(bar.get_height(), '.2f'),
                     (bar.get_x() + bar.get_width() / 2,
                      bar.get_height()), ha='center', va='center',
                     size=7, xytext=(0, 5),
                     textcoords='offset points')
        plt.title(
            "Enrollment/School for Grade " + z + " for the academic year " + academic_year +
            " of district  " + district)

    plt.legend()
    plt.xlabel('School')
    ax.set_ylim([0, max(x) + 10])

    plt.tight_layout()
    graph = get_image()
    return graph


def get_pairs(**kwargs):
    plt.switch_backend('AGG')
    # total enrollment
    x = kwargs.get('x')
    # y = capacity of school
    y = kwargs.get('y')
    # selected year

    year = kwargs.get('academic_year')
    school = kwargs.get('name_of_school')
    district = kwargs.get('district_name')
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(school, y, width=0.50, color='b', label='capacity of school', alpha=0.5)
    ax.bar(school, x, width=0.25, color='g', label='total enrollment')
    ax.set_ylabel("Total Enrollment / Capacity")
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14)
        # specify integer or one of preset strings, e.g.
        # tick.label.set_fontsize('x-small')
        tick.label.set_rotation('vertical')
    for bar in ax.patches:
        # Using Matplotlib annotate function and
        # passing the coordinates where the annotation shall be done
        # x-coordinate: bar.get_x() + bar.get_width() / 2
        # y-coordinate: bar.get_height()
        # free space to be left to make graph pleasing: (0, 8)
        # ha and va stand for the horizontal and vertical alignment
        plt.annotate(format(bar.get_height(), '.2f'),
                     (bar.get_x() + bar.get_width() / 2,
                      bar.get_height()), ha='center', va='center',
                     size=8, xytext=(0, 3),
                     textcoords='offset points')
        plt.title("Enrollment/capacity for the academic year " + year + " of district  " + district)

    plt.legend()

    plt.tight_layout()
    graph = get_image()
    return graph


def get_plot(chart_type, **kwargs):
    plt.switch_backend('AGG')
    # academic year
    x = kwargs.get('x')
    # y = total enrollment
    y = kwargs.get('y')
    # z = capacity of school
    z = kwargs.get('z')
    school_name = kwargs.get('name_of_school')

    if chart_type == 'barplot':
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.bar(x, z, width=0.50, color='b', label='capacity of school', alpha=0.5)
        ax.bar(x, y, width=0.25, color='g', label='total enrollment')
        ax.set_ylabel("Total Enrollment / Capacity")
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(14)
            # specify integer or one of preset strings, e.g.
            # tick.label.set_fontsize('x-small')
            tick.label.set_rotation('vertical')
        for bar in ax.patches:
            # Using Matplotlib annotate function and
            # passing the coordinates where the annotation shall be done
            # x-coordinate: bar.get_x() + bar.get_width() / 2
            # y-coordinate: bar.get_height()
            # free space to be left to make graph pleasing: (0, 8)
            # ha and va stand for the horizontal and vertical alignment
            plt.annotate(format(bar.get_height(), '.2f'),
                         (bar.get_x() + bar.get_width() / 2,
                          bar.get_height()), ha='center', va='center',
                         size=8, xytext=(0, 3),
                         textcoords='offset points')
            plt.title(school_name)
        ax.set_ylim([0, max(z) + 300])
        ax.legend()

    else:
        title = school_name
        plt.figure(figsize=(10, 8))
        plt.title(title)
        plt.plot(x, y, 'b-', label='enrollments')
        plt.plot(x, z, 'g-', label='capacity')
        # plt.ylim(0, max(y) + 100)
        plt.ylabel("Total Enrollment / Capacity")
        plt.xlabel("Academic Year")
        plt.legend()
    plt.tight_layout()
    graph = get_image()
    return graph


def get_plot_boys_primary(**kwargs):
    plt.switch_backend('AGG')
    data = kwargs.get('data')
    for _ in data.shape:
        ger = (data['enrollment'] / data['age_5_to_11_years']) * 100
        academic_year = data.academic_year
    sns.set(font_scale=1)
    sns.set_style("white")
    ax = ger.plot.bar(figsize=(15, 6))
    sns.despine(left=True, bottom=True)
    # label and title
    ax.set_xticklabels(np.arange(len(academic_year)))
    ax.set_title('Gross Enrollment Ratio (%) for Boys in Primary School In St. Lucia', size=18)
    ax.set_xticklabels(academic_year)
    for tick in ax.get_xticklabels():
        tick.set_rotation(-30)
    ax.set(xlabel='Academic Year', ylabel='Gross enrollment rate (%)')

    # annotations
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points')
    # adjust legend

    plt.tight_layout()
    graph = get_image()
    return graph


def get_plot_girls_primary(**kwargs):
    plt.switch_backend('AGG')
    data = kwargs.get('data')
    for _ in data.shape:
        ger = (data['enrollment'] / data['age_5_to_11_years']) * 100
        academic_year = data.academic_year
    sns.set(font_scale=1)
    sns.set_style("white")
    ax = ger.plot.bar(figsize=(15, 6), color='green')
    sns.despine(left=True, bottom=True)
    # label and title
    ax.set_xticklabels(np.arange(len(academic_year)))
    ax.set_title('Gross Enrollment Ratio (%) for Girls in Primary School In St. Lucia', size=18)
    ax.set_xticklabels(academic_year)
    for tick in ax.get_xticklabels():
        tick.set_rotation(-30)
    ax.set(xlabel='Academic Year', ylabel='Gross enrollment rate (%)')

    # annotations
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points')
    # adjust legend

    plt.tight_layout()
    graph = get_image()
    return graph


def get_plot_primary(**kwargs):
    plt.switch_backend('AGG')
    data = kwargs.get('data')
    data_boys = kwargs.get('data_boys')
    data_girls = kwargs.get('data_girls')

    for _ in data.shape:
        ger_boys = (data_boys['enrollment'] / data_boys['age_5_to_11_years']) * 100
        ger_girls = (data_girls['enrollment'] / data_girls['age_5_to_11_years']) * 100
        academic_year = data_girls.academic_year
        title = 'Trend of GER for Primary Schools in St. Lucia'
        plt.figure(figsize=(10, 8))
        plt.title(title)
        plt.plot(academic_year, ger_boys, 'b-', label='boys')
        plt.plot(academic_year, ger_girls, 'g-', label='girls')
        plt.xticks(rotation=60)
        # plt.ylim(0, max(y) + 100)
        plt.ylabel("Gross Enrollment Ratio for boys and girls in St. Lucia")
        plt.xlabel("Academic Year")
        plt.legend()
        plt.grid()
    plt.tight_layout()
    graph = get_image()
    return graph


def get_plot_boys_secondary(**kwargs):
    plt.switch_backend('AGG')
    data = kwargs.get('data')
    for _ in data.shape:
        ger = (data['enrollment'] / data['age_12_to_16_years']) * 100
        academic_year = data.academic_year
    sns.set(font_scale=1)
    sns.set_style("white")
    ax = ger.plot.bar(figsize=(15, 6))
    sns.despine(left=True, bottom=True)
    # label and title
    ax.set_xticklabels(np.arange(len(academic_year)))
    ax.set_title('Gross Enrollment Ratio (%) for Boys in Secondary School In St. Lucia', size=18)
    ax.set_xticklabels(academic_year)
    for tick in ax.get_xticklabels():
        tick.set_rotation(-30)
    ax.set(xlabel='Academic Year', ylabel='Gross enrollment rate (%)')

    # annotations
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points')
    # adjust legend

    plt.tight_layout()
    graph = get_image()
    return graph


def get_plot_girls_secondary(**kwargs):
    plt.switch_backend('AGG')
    data = kwargs.get('data')
    for _ in data.shape:
        ger = (data['enrollment'] / data['age_12_to_16_years']) * 100
        academic_year = data.academic_year
    sns.set(font_scale=1)
    sns.set_style("white")
    ax = ger.plot.bar(figsize=(15, 6), color='green')
    sns.despine(left=True, bottom=True)
    # label and title
    ax.set_xticklabels(np.arange(len(academic_year)))
    ax.set_title('Gross Enrollment Ratio (%) for Girls in secondary School In St. Lucia', size=18)
    ax.set_xticklabels(academic_year)
    for tick in ax.get_xticklabels():
        tick.set_rotation(-30)
    ax.set(xlabel='Academic Year', ylabel='Gross enrollment rate (%)')

    # annotations
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.2f'),
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points')
    # adjust legend

    plt.tight_layout()
    graph = get_image()
    return graph


def get_plot_secondary(**kwargs):
    plt.switch_backend('AGG')
    data = kwargs.get('data')
    data_boys = kwargs.get('data_boys')
    data_girls = kwargs.get('data_girls')

    for _ in data.shape:
        ger_boys = (data_boys['enrollment'] / data_boys['age_12_to_16_years']) * 100
        ger_girls = (data_girls['enrollment'] / data_girls['age_12_to_16_years']) * 100
        academic_year = data_girls.academic_year
        title = 'Trend of GER for Primary Schools in St. Lucia'
        plt.figure(figsize=(10, 8))
        plt.title(title)
        plt.plot(academic_year, ger_boys, 'b-', label='boys')
        plt.plot(academic_year, ger_girls, 'g-', label='girls')
        plt.xticks(rotation=60)
        # plt.ylim(0, max(y) + 100)
        plt.ylabel("Gross Enrollment Ratio for boys and girls in Secondary School")
        plt.xlabel("Academic Year")
        plt.legend()
        plt.grid()
    plt.tight_layout()
    graph = get_image()
    return graph


def get_plot_regression(**kwargs):
    plt.switch_backend('AGG')
    data = kwargs.get('data')
    data_boys_primary = kwargs.get('data_boys_primary')
    data_girls_primary = kwargs.get('data_girls_primary')
    data_boys_secondary = kwargs.get('data_boys_secondary')
    data_girls_secondary = kwargs.get('data_girls_secondary')

