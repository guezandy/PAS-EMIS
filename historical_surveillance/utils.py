import base64
from io import BytesIO
import matplotlib.pyplot as plt
from .models import School

import numpy as np
import pandas as pd

def get_image():
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
    data = kwargs.get('data')
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



#===========================================================
#Outlier detection plot at district level
#===========================================================

def get_outlier_district_plot(**kwargs):

    plt.switch_backend('AGG')

    
    school_enrollment = kwargs.get('x')
    school_name = kwargs.get('y')
    
    datamean = kwargs.get('data_mean')
    input_school_type = kwargs.get('input_school_type')
    academic_year = kwargs.get('academic_year')
    district_input = kwargs.get('input_district')
    



    fig, ax1 = plt.subplots(figsize=(10,6))

    
    ax1.set_title('Enrollment for District')
    ax1.set_xlabel('School_Name')
    ax1.set_ylabel('School_Scores')

    ax1.bar(school_name, school_enrollment, color='#7CFC00', edgecolor='#000000')

    for tick in ax1.xaxis.get_major_ticks():
            tick.label.set_fontsize(14)
            tick.label.set_rotation('vertical')
    plt.plot(school_name, datamean, linewidth = 5, ls = 'solid', color = '#4B0082' )
    

    plt.xlabel("School Name")
    plt.ylabel("Enrollment") 
      
    plt.title("Enrollment for " + input_school_type +" schools for district " + district_input + " and "+  academic_year +  " academic year ")
    plt.tight_layout()
    graph = get_image()
    return graph


#==========================================================================
#Outlier detection at national level
#==========================================================================

def get_outlier_national_plot(**kwargs):

    plt.switch_backend('AGG')

    
    school_enrollment = kwargs.get('x')
    school_name = kwargs.get('y')
    
    datamean = kwargs.get('data_mean')
    input_school_type = kwargs.get('input_school_type')
    academic_year = kwargs.get('academic_year')
    

    fig, ax1 = plt.subplots(figsize=(11,6))



    ax1.set_title('Enrollment for Selected Year')
    ax1.set_xlabel('School_Name')
    

    ax1.bar(school_name, school_enrollment, color='#7CFC00', edgecolor='#000000')
    for tick in ax1.xaxis.get_major_ticks():
            tick.label.set_fontsize(14)
            tick.label.set_rotation('vertical')
    plt.plot(school_name, datamean, linewidth = 5, ls = 'solid', color = '#4B0082')
    

    plt.xlabel("School Name")
    plt.ylabel("Enrollment")    
    plt.title("Enrollment for " + input_school_type +" schools for year " + academic_year)

    plt.tight_layout()
    graph = get_image()
    return graph


