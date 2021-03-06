import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import re
from numpy import mean, std
import random
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.base import clone
import scipy.stats as stats
from .models import *
from .forms import *
import numpy as np
import pandas as pd
from scipy.stats import pearsonr


# function to get the Image and plot

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


# enrollment capacity by school trend
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
        ax.bar(x, z, width=0.50, color='gray', label='capacity of school')
        ax.bar(x, y, width=0.25, color='g', label='total enrollment')
        ax.set_ylabel("Total Enrollment / Capacity")
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(10)
            # specify integer or one of preset strings, e.g.
            # tick.label.set_fontsize('x-small')
            tick.label.set_rotation('60')
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


# This graph plots trends of enrollment versus school capacity  for schools in a district for a select academic year
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
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.bar(school, y, width=0.50, color='gray', label='capacity of school')
    ax.bar(school, x, width=0.25, color='g', label='total enrollment')
    ax.set_ylabel("Total Enrollment / Capacity")
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(10)
        # specify integer or one of preset strings, e.g.
        # tick.label.set_fontsize('x-small')
        tick.label.set_rotation(45)
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


def get_grade_plot(**kwargs):
    plt.switch_backend('AGG')
    # the  selected academic year
    year = kwargs.get('academic_year')

    # the selected school
    school_name = kwargs.get('name_of_school')
    data_boys = kwargs.get('data_boys')
    data_girls = kwargs.get('data_girls')
    data_none = kwargs.get('data')

    # get subplots for boys, girls and single gender

    if len(data_none) > 0:
        fig, ax1 = plt.subplots(1, figsize=(10, 8))
        ax1.plot(data_none['grade'], data_none['enrollment'], 'ro')
        ax1.set_title('Enrollment')
        school_title = School.objects.filter(id=school_name).distinct().values_list('school_name', flat=True)
        school_name_title = school_title[0]
        fig.suptitle("Enrollment for " + school_name_title + " - Academic Year " + year)
        plt.xlabel('Grades')
        plt.tight_layout()
        ax1.grid()
        graph = get_image()
        return graph

    elif len(data_girls) > 0 and len(data_boys) > 0:
        fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 8))
        ax1.plot(data_girls['grade'], data_girls['enrollment'], 'go')
        ax1.set_title('Girls Enrollment')
        ax2.plot(data_boys['grade'], data_boys['enrollment'], 'bo')
        ax2.set_title('Boys Enrollment')

        school_title = School.objects.filter(id=school_name).distinct().values_list('school_name', flat=True)
        school_name_title = school_title[0]
        fig.suptitle("Enrollment for " + school_name_title + " - Academic Year " + year)
        plt.xlabel('Grades')
        plt.tight_layout()
        ax1.grid()
        ax2.grid()
        graph = get_image()
        return graph
    else:
        graph = "No data recorded for the selected year"
        return graph


def get_district_grade_plot_girls(**kwargs):
    plt.switch_backend('AGG')
    # the  selected academic year
    year = kwargs.get('academic_year')
    grade = kwargs.get('grade')
    # the selected school
    district_name = kwargs.get('district')
    data_girls = kwargs.get('data_girls')
    school_girls = kwargs.get('school_girls')

    # get subplots for boys, girls and single gender
    fig, ax1 = plt.subplots(1, figsize=(10, 8))
    ax1.plot(data_girls['enrollment'], school_girls, 'go')
    ax1.set_title('Enrollment')
    plt.xticks(np.arange(0, max(data_girls['enrollment']) + 5, 5.0))
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(10)
        # specify integer or one of preset strings, e.g.
        # tick.label.set_fontsize('x-small')
        tick.label.set_rotation(60)
    district_title = School.objects.filter(id=district_name).distinct().values_list('district_name', flat=True)
    district_name_title = district_title[0]
    fig.suptitle("Grade - " + str(grade) + " Girls Enrollment for Academic Year " + year + " for district" + str(
        district_name_title))
    plt.xlabel('Enrollment')
    plt.ylabel('School')
    plt.tight_layout()
    ax1.grid()
    graph = get_image()
    return graph


def get_district_grade_plot_boys(**kwargs):
    plt.switch_backend('AGG')
    # the  selected academic year
    year = kwargs.get('academic_year')
    grade = kwargs.get('grade')
    # the selected school
    district_name = kwargs.get('district')
    data_boys = kwargs.get('data_boys')
    school_boys = kwargs.get('school_boys')

    # get subplots for boys, girls and single gender
    fig, ax1 = plt.subplots(1, figsize=(10, 8))
    ax1.plot(data_boys['enrollment'], school_boys, 'bo')
    ax1.set_title('Enrollment')
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(10)
        # specify integer or one of preset strings, e.g.
        # tick.label.set_fontsize('x-small')
        tick.label.set_rotation(60)
        plt.xticks(np.arange(0, max(data_boys['enrollment']) + 5, 5.0))
    district_title = School.objects.filter(id=district_name).distinct().values_list('district_name', flat=True)
    district_name_title = district_title[0]
    fig.suptitle("Grade - " + str(grade) + " Boys Enrollment for Academic Year " + year + " for district" + str(
        district_name_title))
    plt.xlabel('Enrollment')
    plt.ylabel('School')
    plt.tight_layout()
    ax1.grid()
    graph = get_image()
    return graph


def get_district_grade_plot_none(**kwargs):
    plt.switch_backend('AGG')
    # the  selected academic year
    year = kwargs.get('academic_year')
    grade = kwargs.get('grade')
    # the selected school
    district_name = kwargs.get('district')
    data_none = kwargs.get('data_none')
    school_none = kwargs.get('school_none')

    # get subplots for boys, girls and single gender
    fig, ax1 = plt.subplots(1, figsize=(10, 8))
    ax1.plot(data_none['enrollment'], school_none, 'ro')
    ax1.set_title('Enrollment')
    plt.xticks(np.arange(0, max(data_none['enrollment']) + 5, 5.0))
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(10)
        # specify integer or one of preset strings, e.g.
        # tick.label.set_fontsize('x-small')
        tick.label.set_rotation(60)
    district_title = School.objects.filter(id=district_name).distinct().values_list('district_name', flat=True)
    district_name_title = district_title[0]
    fig.suptitle("Grade - " + str(grade) + " Total Enrollment for Academic Year " + year + " for district" + str(
        district_name_title))
    plt.xlabel('Enrollment')
    plt.ylabel('School')
    plt.tight_layout()
    ax1.grid()
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


def clean_secondary_name(name):
    name = re.sub("[^a-zA-Z]+", "", name)
    name = name.lower().replace('secondary', "")
    name = name.replace('school', "")
    return ' '.join(name.split())


def match_name(name, schools, district_dict):
    for school in schools:
        if clean_secondary_name(name) == clean_secondary_name(getattr(school, 'school_name')):
            district_code = getattr(school, 'district_name_id')
            district_dict[name] = district_code
            return district_code
    return None


def get_district(school_code, schools, district_dict):
    for school in schools:
        if int(getattr(school, 'school_code')) == school_code:
            district = getattr(school, 'district_name_id')
            district_dict[school_code] = district
            return district
    return None


def csec_performance_plot(data, district_1, district_2):
    left_out = set()

    df = pd.DataFrame(data.values())
    plt.switch_backend('AGG')
    years = [int(y) for y in df['year'].drop_duplicates()]
    years.sort()
    min_year = min(years)

    schools = School.objects.all()
    # schools = School.objects.filter(category_of_school='public secondary')

    N_DISTRICTS = District.objects.count()
    scores = np.zeros((len(years), N_DISTRICTS))
    n_tests = np.zeros((len(years), N_DISTRICTS))
    passing_scores = np.zeros((len(years), N_DISTRICTS))

    # cache school to district matches
    district_dict = {}

    for index, row in df.iterrows():
        school_code = int(row['school_id'])
        if school_code in district_dict:
            district = district_dict[school_code]
        else:
            district = get_district(school_code, schools, district_dict)
        if not district:
            left_out.add(row['school_id'])
            continue
        year = int(row['year']) - min_year
        n_tests[year][district - 1] += 1
        score = row['overall_grade']
        if score == 'I' or score == 'II' or score == 'III':
            scores[year][district - 1] += 1

    passing_scores = 100 * scores / n_tests
    passing_scores = pd.DataFrame(passing_scores)

    labels = ['District ' + str(d + 1) for d in range(N_DISTRICTS)]
    if not (district_1 and district_2):
        for d in range(N_DISTRICTS):
            plt.plot(years, passing_scores[d])
    else:
        plt.plot(years, passing_scores[district_1 - 1])
        plt.plot(years, passing_scores[district_2 - 1])
        labels = ['District ' + str(district_1), 'District ' + str(district_2)]
    plt.xticks([min(years), max(years)])
    plt.legend(labels, loc='upper left', bbox_to_anchor=(1, 1.05))
    plt.title("Percentage of Passing Scores (CSEC)")
    plt.tight_layout()
    graph = get_image()

    plt.clf()
    passing_scores = passing_scores.T
    passing_scores.columns = years
    passing_scores.index = ['District ' + str(d + 1) for d in range(N_DISTRICTS)]
    ax = sns.heatmap(passing_scores, annot=True)
    plt.tight_layout()
    heatmap = get_image()
    return [graph, heatmap, left_out]


# ===================================================================
# Outlier detection at district level
# ===================================================================
def get_outlier_district_plot(**kwargs):
    plt.switch_backend('AGG')

    school_enrollment = kwargs.get('x')
    school_name = kwargs.get('y')

    datamean = kwargs.get('data_mean')
    input_school_type = kwargs.get('input_school_type')
    academic_year = kwargs.get('academic_year')
    district_input = kwargs.get('input_district')

    fig, ax1 = plt.subplots(figsize=(10, 8))

    ax1.set_title('Enrollment for District')
    ax1.set_xlabel('School_Name')
    ax1.set_ylabel('School_Scores')

    ax1.bar(school_name, school_enrollment, color='b')

    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(8)
        tick.label.set_rotation('15')
    plt.plot(school_name, datamean, linewidth=5, ls='solid', color='r')

    plt.xlabel("School Name")
    plt.ylabel("Enrollment")

    plt.title(
        "Enrollment for " + input_school_type + " schools for district " + district_input + " and " + academic_year + " academic year ")

    plt.tight_layout()
    graph = get_image()
    return graph

    plt.tight_layout()
    graph = get_image()
    return graph


# ==========================================================================
# Outlier detection at national level
# ==========================================================================

def get_outlier_national_plot(**kwargs):
    plt.switch_backend('AGG')

    school_enrollment = kwargs.get('x')
    school_name = kwargs.get('y')

    datamean = kwargs.get('data_mean')
    input_school_type = kwargs.get('input_school_type')
    academic_year = kwargs.get('academic_year')

    fig, ax1 = plt.subplots(figsize=(12, 10))

    ax1.set_title('Enrollment for Selected Year')
    ax1.set_xlabel('School_Name')

    ax1.bar(school_name, school_enrollment, width=0.1, color='b')
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(10)
        tick.label.set_rotation('vertical')
    plt.plot(school_name, datamean, linewidth=3, ls='solid', color='r')

    plt.xlabel("School Name")
    plt.ylabel("Enrollment")
    plt.title("Enrollment for " + input_school_type + " schools for year " + academic_year)

    plt.tight_layout()
    graph = get_image()
    return graph

    plt.tight_layout()
    graph = get_image()
    return graph


def get_plot_regression(**kwargs):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 8))

    data = kwargs.get('data')
    sns.set_theme(color_codes=True)
    sns.regplot(x=data.enrollment, y=data.gdp_millions, data=data, x_estimator=np.mean, label='GDP');
    sns.regplot(x=data.enrollment, y=data.educational_expenditure, data=data, x_estimator=np.mean,
                label='Educational Expenditure');
    sns.regplot(x=data.enrollment, y=data.government_expenditure, data=data, x_estimator=np.mean,
                label='Government Expenditure');
    plt.xlabel("Enrollment")
    plt.ylabel("Expenditure")
    plt.title("Linear Regression - Enrollment / GDP / Education / government expenditure")
    plt.legend()
    plt.tight_layout()
    graph = get_image()
    return graph


def get_plot_gdp_regress(**kwargs):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 8))
    data = kwargs.get('data')
    sns.set_theme(color_codes=True)
    sns.jointplot(x=data.enrollment, y=data.gdp_millions, data=data, x_estimator=np.mean,
                  label='GDP', kind="reg");
    plt.xlabel("Enrollment")
    plt.ylabel("Expenditure")
    plt.tight_layout()
    graph = get_image()
    return graph


def get_enrollment_joint_pearsons(**kwargs):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 8))
    data = kwargs.get('data')
    sns.set_theme(color_codes=True)
    import scipy.stats as stats
    graph = sns.jointplot(data=data, x=data.enrollment, y=data.gdp_millions)
    r, p = stats.pearsonr(x=data.enrollment, y=data.gdp_millions)
    phantom, = graph.ax_joint.plot([], [], linestyle="", alpha=0)
    # here graph is not a ax but a joint grid, so we access the axis through ax_joint method
    graph.ax_joint.legend([phantom], ['r={:f}, p={:f}'.format(r, p)])
    plt.tight_layout()
    graph = get_image()
    return graph


def get_enrollment_joint_spearman(**kwargs):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 8))
    data = kwargs.get('data')
    sns.set_theme(color_codes=True)
    graph = sns.jointplot(data=data, x=data.enrollment, y=data.gdp_millions)
    r, p = stats.spearmanr(data.enrollment, data.gdp_millions)
    phantom, = graph.ax_joint.plot([], [], linestyle="", alpha=0)
    # here graph is not a ax but a joint grid, so we access the axis through ax_joint method

    graph.ax_joint.legend([phantom], ['r={:f}, p={:f}'.format(r, p)])
    plt.tight_layout()
    graph = get_image()
    return graph


def get_enrollment_multicollinearity(**kwargs):
    plt.figure(figsize=(10, 8))
    plt.switch_backend('AGG')
    data = kwargs.get('data')
    data = data[["educational_expenditure", "gdp_millions", "government_expenditure", "primary_school_expenditure",
                 "secondary_school_expenditure", "enrollment", "age_5_to_11_years", "age_12_to_16_years"]]
    sns.set(style='white')
    corr = data.corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(12, 10))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.9, center=0, square=True, linewidths=.5, annot=True,
                cbar_kws={'shrink': .5});
    plt.tight_layout()
    graph = get_image()
    return graph


def get_kernel_density(**kwargs):
    plt.figure(figsize=(10, 8))
    plt.switch_backend('AGG')
    data = kwargs.get('data')
    sns.kdeplot(data=data.enrollment)
    sns.despine()
    plt.tight_layout()
    graph = get_image()
    return graph


def plot_national_gender_enrollment(**kwargs):
    plt.switch_backend('AGG')
    data_boys_primary = kwargs.get('data_boys_primary')
    data_boys_secondary = kwargs.get('data_boys_secondary')
    data_girls_primary = kwargs.get('data_girls_primary')
    data_girls_secondary = kwargs.get('data_girls_secondary')
    title = 'Trend in enrollments over time'
    plt.figure(figsize=(10, 8))
    plt.title(title)
    plt.plot(data_boys_primary['academic_year'], data_boys_primary['enrollment'], 'b-',
             label='Boys enrolled in Primary School')
    plt.plot(data_boys_secondary['academic_year'], data_boys_secondary['enrollment'], 'bo',
             label='Boys enrolled in Secondary School')
    plt.plot(data_girls_primary['academic_year'], data_girls_primary['enrollment'], 'r-',
             label='Girls enrolled in Primary School')
    plt.plot(data_girls_secondary['academic_year'], data_girls_secondary['enrollment'], 'ro',
             label='Girls enrolled in secondary School')

    plt.xticks(rotation=60)
    # plt.ylim(0, max(y) + 100)
    plt.ylabel("National Enrollment Trends")
    plt.xlabel("Academic Year")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    graph = get_image()
    return graph


def national_gender_enrollment_hist(**kwargs):
    data_boys_primary = kwargs.get('data_boys_primary')
    data_boys_secondary = kwargs.get('data_boys_secondary')
    data_girls_primary = kwargs.get('data_girls_primary')
    data_girls_secondary = kwargs.get('data_girls_secondary')

    # boys primary mean of distribution
    mu_boys_primary = mean(data_boys_primary.enrollment)
    mu_girls_primary = mean(data_girls_primary.enrollment)
    mu_boys_secondary = mean(data_boys_secondary.enrollment)
    mu_girls_secondary = mean(data_girls_secondary.enrollment)

    sigma_boys_primary = std(data_boys_primary.enrollment)
    sigma_girls_primary = std(data_girls_primary.enrollment)
    sigma_boys_secondary = std(data_boys_secondary.enrollment)
    sigma_girls_secondary = std(data_girls_secondary.enrollment)

    x_mu_boys_primary = mu_boys_primary + sigma_boys_primary * np.random.randn(437)
    x_mu_girls_primary = mu_girls_primary + sigma_girls_primary * np.random.randn(437)
    x_mu_boys_secondary = mu_boys_secondary + sigma_boys_secondary * np.random.randn(437)
    x_mu_girls_secondary = mu_girls_secondary + sigma_girls_secondary * np.random.randn(437)
    num_bins = 50

    # fig, ax = plt.subplots()

    fig, axs = plt.subplots(2, 2, figsize=(15, 15))

    # the histogram of the data
    n_boys_primary, bins_boys_primary, patches_boys_primary = axs[0, 0].hist(x_mu_boys_primary, num_bins, density=True)
    n_boys_secondary, bins_boys_secondary, patches_boys_secondary = axs[0, 1].hist(x_mu_boys_secondary, num_bins,
                                                                                   density=True)
    n_girls_primary, bins_girls_primary, patches_girls_primary = axs[1, 0].hist(x_mu_girls_primary, num_bins,
                                                                                density=True)
    n_girls_secondary, bins_girls_secondary, patches_girls_secondary = axs[1, 1].hist(x_mu_girls_secondary, num_bins,
                                                                                      density=True)
    # add a 'best fit' line
    y_boys_primary = ((1 / (np.sqrt(2 * np.pi) * sigma_boys_primary)) *
                      np.exp(-0.5 * (1 / sigma_boys_primary * (bins_boys_primary - mu_boys_primary)) ** 2))
    y_boys_secondary = ((1 / (np.sqrt(2 * np.pi) * sigma_boys_secondary)) *
                        np.exp(-0.5 * (1 / sigma_boys_secondary * (bins_boys_secondary - mu_boys_secondary)) ** 2))
    y_girls_primary = ((1 / (np.sqrt(2 * np.pi) * sigma_girls_primary)) *
                       np.exp(-0.5 * (1 / sigma_girls_primary * (bins_girls_primary - mu_girls_primary)) ** 2))

    y_girls_secondary = ((1 / (np.sqrt(2 * np.pi) * sigma_girls_secondary)) *
                         np.exp(-0.5 * (1 / sigma_girls_secondary * (bins_girls_secondary - mu_girls_secondary)) ** 2))

    for ax in axs.flat:
        ax.set(xlabel='Enrollment', ylabel='Probability Density')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    axs[0, 0].plot(bins_boys_primary, y_boys_primary, '--')
    axs[0, 0].set_title('Primary-Boys')

    axs[0, 1].plot(bins_boys_secondary, y_boys_secondary, '--')
    axs[0, 1].set_title('Secondary-Boys')

    axs[1, 0].plot(bins_girls_primary, y_girls_primary, '--')
    axs[1, 0].set_title('Primary-Girls')

    axs[1, 1].plot(bins_girls_secondary, y_girls_secondary, '--')
    axs[1, 1].set_title('Secondary-Girls')

    plt.tight_layout()
    graph = get_image()
    return graph


def plot_national_education_census(**kwargs):
    plt.switch_backend('AGG')
    data = kwargs.get('data')

    title = 'Education Census Over time'
    plt.figure(figsize=(10, 8))
    plt.title(title)
    plt.plot(data['academic_year'], data['age_3_to_4_years'], 'b-',
             label='Population of Age Group 3-4')
    plt.plot(data['academic_year'], data['age_5_to_11_years'], 'y-',
             label='Population of Age Group > 5 and less than 12')
    plt.plot(data['academic_year'], data['age_12_to_16_years'], 'r-',
             label='population of children above 12 years old')

    plt.xticks(rotation=60)
    # plt.ylim(0, max(y) + 100)
    plt.ylabel("Education Census Trends")
    plt.xlabel("Academic Year")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    graph = get_image()
    return graph


def national_education_census_hist(**kwargs):
    data = kwargs.get('data')
    # boys primary mean of distribution
    mu_data_3_4 = mean(data.age_3_to_4_years)
    mu_data_5_11 = mean(data.age_5_to_11_years)
    mu_data_12_16 = mean(data.age_12_to_16_years)

    sigma_data_3_4 = std(data.age_3_to_4_years)
    sigma_data_5_11 = std(data.age_5_to_11_years)
    sigma_data_12_16 = std(data.age_12_to_16_years)

    x_mu_data_3_4 = mu_data_3_4 + sigma_data_3_4 * np.random.randn(437)
    x_mu_data_5_11 = mu_data_5_11 + sigma_data_5_11 * np.random.randn(437)
    x_mu_data_12_16 = mu_data_12_16 + sigma_data_12_16 * np.random.randn(437)
    num_bins = 50

    # fig, ax = plt.subplots()

    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(15, 15))

    # the histogram of the data
    n_3_4, bins_3_4, patches_3_4 = ax1.hist(x_mu_data_3_4, num_bins, density=True)
    n_5_11, bins_5_11, patches_5_11 = ax2.hist(x_mu_data_5_11, num_bins, density=True)
    n_12_16, bins_12_16, patches_12_16 = ax3.hist(x_mu_data_12_16, num_bins, density=True)

    # add a 'best fit' line
    y_3_4 = ((1 / (np.sqrt(2 * np.pi) * sigma_data_3_4)) *
             np.exp(-0.5 * (1 / sigma_data_3_4 * (bins_3_4 - mu_data_3_4)) ** 2))
    y_5_11 = ((1 / (np.sqrt(2 * np.pi) * sigma_data_5_11)) *
              np.exp(-0.5 * (1 / sigma_data_5_11 * (bins_5_11 - mu_data_5_11)) ** 2))
    y_12_16 = ((1 / (np.sqrt(2 * np.pi) * sigma_data_12_16)) *
               np.exp(-0.5 * (1 / sigma_data_12_16 * (bins_12_16 - mu_data_12_16)) ** 2))

    ax1.plot(bins_3_4, y_3_4, '--')
    ax1.set_title('3 - 4 years')

    ax2.plot(bins_5_11, y_5_11, '--')
    ax2.set_title('Greater / equal 5, Less than 12')

    ax3.plot(bins_12_16, y_12_16, '--')
    ax3.set_title('>=12 years')

    plt.tight_layout()
    graph = get_image()
    return graph


def plot_national_expenditure(**kwargs):
    plt.switch_backend('AGG')
    data = kwargs.get('data')
    title = 'Education Expenditure'
    plt.figure(figsize=(10, 8))
    plt.title(title)
    plt.plot(data['academic_year'], data.educational_expenditure, 'b-',
             label='Educational Expenditure')
    plt.plot(data['academic_year'], data['gdp_millions'], 'y-',
             label='GDP (Million XCD)')
    plt.plot(data['academic_year'], data['government_expenditure'], 'r-',
             label='Government Expenditure')
    plt.plot(data['academic_year'], data['primary_school_expenditure'], 'g-',
             label='Primary School Expenditure')
    plt.plot(data['academic_year'], data['secondary_school_expenditure'], 'k-',
             label='Secondary School Expenditure')

    plt.xticks(rotation=60)
    # plt.ylim(0, max(y) + 100)
    plt.ylabel("Expenditure Trends")
    plt.xlabel("Academic Year")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    graph = get_image()
    return graph


def national_expenditure_hist(**kwargs):
    data = kwargs.get('data')
    mu_educational_expenditure = mean(data['educational_expenditure'])
    mu_gdp_millions = mean(data['gdp_millions'])
    mu_government_expenditure = mean(data['government_expenditure'])
    mu_primary_school_expenditure = mean(data['primary_school_expenditure'])
    mu_secondary_school_expenditure = mean(data['secondary_school_expenditure'])

    sigma_educational_expenditure = std(data.educational_expenditure)
    sigma_gdp_millions = std(data.gdp_millions)
    sigma_government_expenditure = std(data.government_expenditure)
    sigma_primary_school_expenditure = std(data.primary_school_expenditure)
    sigma_secondary_school_expenditure = std(data.secondary_school_expenditure)

    x_mu_educational_expenditure = mu_educational_expenditure + sigma_educational_expenditure * np.random.randn(437)
    x_mu_gdp_millions = mu_gdp_millions + sigma_gdp_millions * np.random.randn(437)
    x_mu_government_expenditure = mu_government_expenditure + sigma_government_expenditure * np.random.randn(437)
    x_mu_primary_school_expenditure = mu_primary_school_expenditure + sigma_primary_school_expenditure * np.random.randn(
        437)
    x_mu_secondary_school_expenditure = mu_secondary_school_expenditure + sigma_secondary_school_expenditure * np.random.randn(
        437)
    num_bins = 50

    # fig, ax = plt.subplots()

    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, figsize=(15, 15))

    # the histogram of the data
    n_educational_expenditure, bins_educational_expenditure, patches_educational_expenditure = \
        ax1.hist(x_mu_educational_expenditure, num_bins, density=True)
    n_gdp_millions, bins_gdp_millions, patches_gdp_millions = \
        ax2.hist(x_mu_gdp_millions, num_bins, density=True)
    n_government_expenditure, bins_government_expenditure, patches_government_expenditure = \
        ax3.hist(x_mu_government_expenditure, num_bins, density=True)
    n_primary_school_expenditure, bins_primary_school_expenditure, patches_primary_school_expenditure = \
        ax4.hist(x_mu_primary_school_expenditure, num_bins, density=True)
    n_secondary_school_expenditure, bins_secondary_school_expenditure, patches_secondary_school_expenditure = \
        ax5.hist(x_mu_secondary_school_expenditure, num_bins, density=True)
    # add a 'best fit' line
    y_educational_expenditure = ((1 / (np.sqrt(2 * np.pi) * sigma_educational_expenditure)) *
                                 np.exp(-0.5 * (1 / sigma_educational_expenditure * (
                                         bins_educational_expenditure - mu_educational_expenditure)) ** 2))
    y_gdp_millions = ((1 / (np.sqrt(2 * np.pi) * sigma_gdp_millions)) *
                      np.exp(-0.5 * (1 / sigma_gdp_millions * (bins_gdp_millions - mu_gdp_millions)) ** 2))
    y_government_expenditure = ((1 / (np.sqrt(2 * np.pi) * sigma_government_expenditure)) *
                                np.exp(-0.5 * (1 / sigma_government_expenditure * (
                                        bins_government_expenditure - mu_government_expenditure)) ** 2))
    y_primary_school_expenditure = ((1 / (np.sqrt(2 * np.pi) * sigma_primary_school_expenditure)) *
                                    np.exp(-0.5 * (1 / sigma_primary_school_expenditure * (
                                            bins_primary_school_expenditure - mu_primary_school_expenditure)) ** 2))
    y_secondary_school_expenditure = ((1 / (np.sqrt(2 * np.pi) * sigma_secondary_school_expenditure)) *
                                      np.exp(-0.5 * (1 / sigma_secondary_school_expenditure * (
                                              bins_secondary_school_expenditure - mu_secondary_school_expenditure)) ** 2))

    ax1.plot(bins_educational_expenditure, y_educational_expenditure, '--')
    ax1.set_title('Educational Expenditure')

    ax2.plot(bins_gdp_millions, y_gdp_millions, '--')
    ax2.set_title('gdp(Million XCD)')

    ax3.plot(bins_government_expenditure, y_government_expenditure, '--')
    ax3.set_title('Government Expenditure')

    ax4.plot(bins_primary_school_expenditure, y_primary_school_expenditure, '--')
    ax4.set_title('Primary School Expenditure')

    ax5.plot(bins_secondary_school_expenditure, y_secondary_school_expenditure, '--')
    ax5.set_title('Secondary School Expenditure')

    plt.tight_layout()
    graph = get_image()
    return graph


def primary_performance_plot(data, district_1, district_2):
    df = pd.DataFrame(data.values())
    plt.switch_backend('AGG')
    years = df['academic_year'].drop_duplicates().str.split("/")
    years = [int(y[1]) for y in years]
    min_year = min(years)

    N_DISTRICTS = District.objects.count()

    tests = np.zeros((len(years), N_DISTRICTS), dtype=int)
    above_avg = np.zeros((len(years), N_DISTRICTS), dtype=int)
    performance = np.zeros((len(years), N_DISTRICTS), dtype=float)

    for index, row in df.iterrows():
        year = int(row['academic_year'].split('/')[1])
        school_code = row['school_id']
        school = School.objects.get(school_code=school_code)
        district = getattr(school, 'district_name_id')
        n_tests = int(row['tests_sat'])
        n_above_avg = int(row['above_average_scores'])
        if np.isnan(n_tests) or np.isnan(n_above_avg):
            continue
        tests[year - min_year][district - 1] += n_tests
        above_avg[year - min_year][district - 1] += n_above_avg

    for y in range(len(years)):
        performance[y] = 100 * above_avg[y] / tests[y]
    performance = pd.DataFrame(performance)
    labels = ['District ' + str(d + 1) for d in range(N_DISTRICTS)]
    if not (district_1 and district_2):
        for d in range(N_DISTRICTS):
            plt.plot(years, performance[d])
    else:
        plt.plot(years, performance[district_1 - 1])
        plt.plot(years, performance[district_2 - 1])
        labels = ['District ' + str(district_1), 'District' + str(district_2)]
    plt.xticks([min(years), max(years)])
    plt.legend(labels, loc='upper left', bbox_to_anchor=(1, 1.05))
    plt.title("Percentage of Students Scoring Above Mean (CEE)")
    plt.tight_layout()
    graph = get_image()

    plt.clf()
    performance = performance.T
    performance.columns = np.arange(1999, 2018, step=1)
    performance.index = ['District ' + str(d + 1) for d in range(N_DISTRICTS)]
    ax = sns.heatmap(performance, annot=True)
    ax.set_title("Percentage of Students Scoring above Mean (CEE)")
    plt.tight_layout()
    heatmap = get_image()
    return [graph, heatmap]


def get_sex(character):
    if character == "F":
        return "female"
    else:
        return "male"


def store_scores(data, required_fields, user_data, type):
    result = {}
    lines = data.replace("\r", "").split("\n")
    field_names = lines[0].split(",")
    if not set(required_fields).issubset(set(field_names)):
        diff = set(required_fields) - set(field_names)
        missing_fields = []
        for d in diff:
            missing_fields.append(d)
        result['missing_fields'] = missing_fields
        result['error_message'] = 'The following fields are missing:\n'
        result['n_scores'] = 0
    else:
        succeeded = 0
        failed = 0
        for line in lines[1:]:
            if line:
                fields = line.split(",")
                data = {}
                for required_field in required_fields:
                    if required_field == "school_id":
                        data["school"] = fields[field_names.index("school_id")]
                    elif required_field == "primsch_id":
                        data["primsch"] = fields[field_names.index("primsch_id")]
                    elif required_field == "secsch_id":
                        data["secsch"] = fields[field_names.index("secsch_id")]
                    elif required_field == "district_id":
                        data["district"] = fields[field_names.index("district_id")]
                    elif required_field == "sex":
                        data["sex"] = get_sex(fields[field_names.index(required_field)])
                    else:
                        data[required_field] = fields[field_names.index(required_field)]
                data = {**data, **user_data}
                if type == "CEE":
                    form = CEEForm(data)
                if type == "CSEC":
                    form = CSECForm(data)
                if form.is_valid():
                    form.save()
                    succeeded += 1
                else:
                    failed += 1
        result['n_scores'] = succeeded
        result['failed'] = failed
    return result


# =======================================================================================
# Box plots at district level
# =======================================================================================

def get_boxplot_district_plot(**kwargs):
    plt.switch_backend('AGG')

    school_enrollment = kwargs.get('x')
    school_name = kwargs.get('y')

    input_school_type = kwargs.get('input_school_type')
    academic_year = kwargs.get('academic_year')
    district_input = kwargs.get('input_district')

    fig, ax1 = plt.subplots(figsize=(11, 6))

    plt.boxplot(school_enrollment, patch_artist=True,
                boxprops=dict(facecolor='purple'),
                meanline=True, showmeans=True)

    plt.xticks([1], [input_school_type])
    plt.ylabel('Enrollment')
    plt.title(
        "Box Plot for Enrollment in " + input_school_type + " schools  in " + " District" + district_input + " and academic year " + academic_year)

    plt.tight_layout()
    graph = get_image()
    return graph


# =========================================================================================
# Box plots at national level
# =========================================================================================

def get_boxplot_national_plot(**kwargs):
    plt.switch_backend('AGG')

    school_enrollment = kwargs.get('x')
    school_name = kwargs.get('y')

    input_school_type = kwargs.get('input_school_type')
    academic_year = kwargs.get('academic_year')

    fig, ax1 = plt.subplots(figsize=(11, 6))

    plt.boxplot(school_enrollment, patch_artist=True,
                boxprops=dict(facecolor='purple'),
                meanline=True, showmeans=True)

    plt.xticks([1], [input_school_type])
    plt.ylabel('Enrollment')
    plt.title("Box Plot for Enrollment in " + input_school_type + " schools " + " for academic year " + academic_year)

    plt.tight_layout()
    graph = get_image()
    return graph


def plot_national_ratio_trend(**kwargs):
    plt.switch_backend('AGG')
    data_primary = kwargs.get('data_primary')
    data_secondary = kwargs.get('data_secondary')
    for _ in data_secondary.shape:
        school_enrollment = data_secondary.total_enrollment
        total_number_of_teachers_secondary = data_secondary.total_number_of_teachers
        academic_year = data_secondary.academic_year
        student_teacher_ratio_secondary = (
            (school_enrollment / total_number_of_teachers_secondary).replace(np.inf, 0)).astype(float)
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.bar(academic_year, student_teacher_ratio_secondary, width=0.8, color='b',
               label='Student to teacher ratio in Secondary Schools'
               , alpha=0.5)
        ax.set_ylabel("Student - Teacher Ratio (7-11)")

        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(10)
            tick.label.set_rotation(45)
        for bar in ax.patches:
            plt.annotate(format(bar.get_height(), '.2f'),
                         (bar.get_x() + bar.get_width() / 2,
                          bar.get_height()), ha='center', va='center',
                         size=7, xytext=(0, 5),
                         textcoords='offset points')
            plt.title("Student to Teacher Ratio Trends in Secondary Schools")
            plt.xlabel('Academic Year')
            ax.set_ylim([0, max(student_teacher_ratio_secondary) + 100])

            ax.legend()

    plt.tight_layout()
    # plt.grid()
    graph = get_image()
    return graph


def plot_national_ratio_trend_primary(**kwargs):
    plt.switch_backend('AGG')
    data_primary = kwargs.get('data_primary')
    for _ in data_primary.shape:
        school_enrollment = data_primary.total_enrollment
        total_number_of_teachers_primary = data_primary.total_number_of_teachers
        academic_year = data_primary.academic_year
        student_teacher_ratio_primary = (
            (school_enrollment / total_number_of_teachers_primary).replace(np.inf, 0)).astype(float)
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.bar(academic_year, student_teacher_ratio_primary, width=0.8, color='g',
               label='Student to teacher ratio in Primary Schools'
               , alpha=0.5)
        ax.set_ylabel("Student - Teacher Ratio (k-6)")

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(10)
        tick.label.set_rotation(45)
    for bar in ax.patches:
        plt.annotate(format(bar.get_height(), '.2f'),
                     (bar.get_x() + bar.get_width() / 2,
                      bar.get_height()), ha='center', va='center',
                     size=7, xytext=(0, 5),
                     textcoords='offset points')
        plt.title("Student to Teacher Ratio Trends in Primary Schools")
        plt.xlabel('Academic Year')
        ax.set_ylim([0, max(student_teacher_ratio_primary) + 100])

        ax.legend()
    plt.tight_layout()
    # plt.grid()
    graph = get_image()
    return graph


def national_ratio_hist(**kwargs):
    plt.switch_backend('AGG')
    data = kwargs.get('data')
    mu_total_enrollment = mean(data['total_enrollment'])
    mu_number_of_trained_male_teachers = mean(data['number_of_trained_male_teachers'])
    mu_number_of_trained_female_teachers = mean(data['number_of_trained_female_teachers'])
    mu_number_of_untrained_male_teachers = mean(data['number_of_untrained_male_teachers'])
    mu_number_of_untrained_female_teachers = mean(data['number_of_untrained_female_teachers'])
    mu_total_no_of_teachers = mean(data['total_number_of_teachers'])

    sigma_total_enrollment = std(data['total_enrollment'])
    sigma_number_of_trained_male_teachers = std(data['number_of_trained_male_teachers'])
    sigma_number_of_trained_female_teachers = std(data['number_of_trained_female_teachers'])
    sigma_number_of_untrained_male_teachers = std(data['number_of_untrained_male_teachers'])
    sigma_number_of_untrained_female_teachers = std(data['number_of_untrained_female_teachers'])
    sigma_total_no_of_teachers = std(data['total_number_of_teachers'])

    x_mu_total_enrollment = mu_total_enrollment + sigma_total_enrollment * np.random.randn(437)
    x_mu_number_of_trained_male_teachers = mu_number_of_trained_male_teachers + sigma_number_of_trained_male_teachers * np.random.randn(
        437)
    x_mu_number_of_trained_female_teachers = mu_number_of_trained_female_teachers + sigma_number_of_trained_female_teachers * np.random.randn(
        437)
    x_mu_number_of_untrained_male_teachers = mu_number_of_untrained_male_teachers + sigma_number_of_untrained_male_teachers * np.random.randn(
        437)
    x_mu_number_of_untrained_female_teachers = mu_number_of_untrained_female_teachers + sigma_number_of_untrained_female_teachers * np.random.randn(
        437)
    x_mu_total_no_of_teachers = mu_total_no_of_teachers + sigma_total_no_of_teachers * np.random.randn(
        437)
    num_bins = 50

    # fig, ax = plt.subplots()

    fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, figsize=(15, 15))

    # the histogram of the data
    n_total_enrollment, bins_total_enrollment, patches_total_enrollment = \
        ax1.hist(x_mu_total_enrollment, num_bins, density=True)
    n_number_of_trained_male_teachers, bins_number_of_trained_male_teachers, patches_number_of_trained_male_teachers = \
        ax2.hist(x_mu_number_of_trained_male_teachers, num_bins, density=True)
    n_number_of_trained_female_teachers, bins_number_of_trained_female_teachers, patches_number_of_trained_female_teachers = \
        ax3.hist(x_mu_number_of_trained_female_teachers, num_bins, density=True)
    n_number_of_untrained_male_teachers, bins_number_of_untrained_male_teachers, patches_number_of_untrained_male_teachers = \
        ax4.hist(x_mu_number_of_untrained_male_teachers, num_bins, density=True)
    n_number_of_untrained_female_teachers, bins_number_of_untrained_female_teachers, patches_number_of_untrained_female_teachers = \
        ax5.hist(x_mu_number_of_untrained_female_teachers, num_bins, density=True)
    n_total_number_of_teachers, bins_total_number_of_teachers, patches_total_number_of_teachers = \
        ax6.hist(x_mu_total_no_of_teachers, num_bins, density=True)
    # add a 'best fit' line
    y_total_enrollment = ((1 / (np.sqrt(2 * np.pi) * sigma_total_enrollment)) *
                          np.exp(-0.5 * (1 / sigma_total_enrollment * (
                                  bins_total_enrollment - mu_total_enrollment)) ** 2))
    y_number_of_trained_male_teachers = ((1 / (np.sqrt(2 * np.pi) * sigma_number_of_trained_male_teachers)) *
                                         np.exp(-0.5 * (1 / sigma_number_of_trained_male_teachers * (
                                                 bins_number_of_trained_male_teachers - mu_number_of_trained_male_teachers)) ** 2))
    y_number_of_trained_female_teachers = ((1 / (np.sqrt(2 * np.pi) * sigma_number_of_trained_female_teachers)) *
                                           np.exp(-0.5 * (1 / sigma_number_of_trained_female_teachers * (
                                                   bins_number_of_trained_female_teachers - mu_number_of_trained_female_teachers)) ** 2))
    y_number_of_untrained_male_teachers = ((1 / (np.sqrt(2 * np.pi) * sigma_number_of_untrained_male_teachers)) *
                                           np.exp(-0.5 * (1 / sigma_number_of_untrained_male_teachers * (
                                                   bins_number_of_untrained_male_teachers - mu_number_of_untrained_male_teachers)) ** 2))
    y_number_of_untrained_female_teachers = ((1 / (np.sqrt(2 * np.pi) * sigma_number_of_untrained_female_teachers)) *
                                             np.exp(-0.5 * (1 / sigma_number_of_untrained_female_teachers * (
                                                     bins_number_of_untrained_female_teachers - mu_number_of_untrained_female_teachers)) ** 2))
    y_total_no_of_teachers = ((1 / (np.sqrt(2 * np.pi) * sigma_total_no_of_teachers)) *
                              np.exp(-0.5 * (1 / sigma_total_no_of_teachers * (
                                      bins_total_number_of_teachers - mu_total_no_of_teachers)) ** 2))

    ax1.plot(bins_total_enrollment, y_total_enrollment, '--')
    ax1.set_title('Total Enrollment')

    ax2.plot(bins_number_of_trained_male_teachers, y_number_of_trained_male_teachers, '--')
    ax2.set_title('Number of Trained Male Teachers')

    ax3.plot(bins_number_of_trained_female_teachers, y_number_of_trained_female_teachers, '--')
    ax3.set_title('Number of Trained Female Teachers')

    ax4.plot(bins_number_of_untrained_male_teachers, y_number_of_untrained_male_teachers, '--')
    ax4.set_title('Number of Untrained Male Teachers')

    ax5.plot(bins_number_of_untrained_female_teachers, y_number_of_untrained_female_teachers, '--')
    ax5.set_title('Untrained Female Teachers')

    ax6.plot(bins_total_number_of_teachers, y_total_no_of_teachers, '--')
    ax6.set_title('Total Number of Teachers')

    plt.tight_layout()
    graph = get_image()
    return graph


def get_prev_yr(year_string):
    year = int(year_string.split("/")[0])
    prev_year = year - 1
    return str(prev_year) + "/" + str(year)


def get_previous_performance(data):
    previous = []
    for index, row in data.iterrows():
        previous_year = data.loc[(data['school_id'] == row['school_id']) &
                                 (data['academic_year'] == get_prev_yr(row['academic_year']))]
        if not previous_year.empty:
            previous.append(previous_year['performance'].values[0])
        else:
            previous.append(np.nan)

    previous = pd.Series(previous)
    data['previous'] = previous
    return data


def get_enrollment(data):
    enrollment = []
    capacity = []
    found = 0
    not_found = 0
    for index, row in data.iterrows():
        school = AggregateEnrollment.objects.filter(name_of_school_id=row['school_id'],
                                                    academic_year=row['academic_year'])
        if school:
            enr = getattr(school[0], 'total_enrollment')
            enrollment.append(enr)
            capacity.append(enr / getattr(school[0], 'capacity_of_school'))
        else:
            enrollment.append(np.nan)
            capacity.append(np.nan)

    enrollment = pd.Series(enrollment)
    data['enrollment'] = enrollment
    capacity = pd.Series(capacity)
    data['capacity'] = capacity
    return data


def divide_by_enrollment(data):
    data['teachers'] = data['enrollment'] / data['teachers']
    data['girls'] = data['girls'] / data['enrollment']
    data['total_bursaries'] = data['total_bursaries'] / data['enrollment']
    data['feeding_program'] = data['feeding_program'] / data['enrollment']
    data['repeaters'] = data['repeaters'] / data['enrollment']
    data['trained_teachers'] = data['trained_teachers'] / data['teachers']
    data['primary_enrollment'] = data['primary_enrollment'] / data['enrollment']
    return data


def correlations(data, excluded_fields):
    plt.switch_backend('AGG')
    data = pd.DataFrame(data.values())
    data['performance'] = data['above_average_scores'] / data['tests_sat']
    data = data.drop(columns=excluded_fields)

    data = get_previous_performance(data)
    data = get_enrollment(data)

    data = data.drop(columns=['academic_year', 'school_id', 'above_average_scores', 'tests_sat'])
    data = data.apply(pd.to_numeric)
    data = divide_by_enrollment(data)

    correlation = []
    spearman = []
    for f in data.columns:
        if f == 'performance':
            continue
        df = data[data[f].notna()]
        x = df[f]
        y = df['performance']
        correlation.append(stats.pearsonr(x, y))
        spearman.append(stats.spearmanr(x, y))
    correlation = pd.DataFrame(correlation)
    spearman = pd.DataFrame(spearman)
    correlation.columns = ['r (Pe)', 'p (Pe)']
    correlation.index = data.columns.drop('performance')
    spearman.index = data.columns.drop('performance')
    correlation['r (Sp)'] = spearman['correlation']
    correlation['p (Sp)'] = spearman['pvalue']

    mask = np.zeros((len(correlation), 4))
    mask[:, 3] = True
    mask[:, 1] = True
    ax = sns.heatmap(correlation, annot=True, mask=mask)
    ax.set_title("Correlations between School Factors and Exam Performance")

    for (j, i), label in np.ndenumerate(correlation.values):
        label = "{:.2e}".format(label)
        if i == 1 or i == 3:
            ax.text(i + 0.5, j + 0.5, label,
                    fontdict=dict(ha='center', va='center', color='black'))
    plt.tight_layout()
    graph = get_image()
    return graph


def dropcol_importances(rf, X_train, y_train):
    r = random.randint(1, 999)
    rf_ = clone(rf)
    rf_.random_state = r
    rf_.fit(X_train, y_train)
    baseline = rf_.oob_score_
    imp = []
    for col in X_train.columns:
        X = X_train.drop(col, axis=1)
        rf_ = clone(rf)
        rf_.random_state = r
        rf_.fit(X, y_train)
        o = rf_.oob_score_
        imp.append(baseline - o)
    imp = np.array(imp)
    I = pd.DataFrame(
        data={'Feature': X_train.columns,
              'Importance': imp})
    I = I.set_index('Feature')
    I = I.sort_values('Importance', ascending=True)
    return I


def rf_model(data, excluded_fields, random):
    plt.switch_backend('AGG')
    data = pd.DataFrame(data.values())
    data['performance'] = data['above_average_scores'] / data['tests_sat']
    data = data.drop(columns=excluded_fields)

    data = get_previous_performance(data)
    data = get_enrollment(data)
    data = data.drop(columns=['academic_year', 'school_id', 'above_average_scores', 'tests_sat'])

    data = data.apply(pd.to_numeric)
    data = divide_by_enrollment(data)

    imp_mean = SimpleImputer(missing_values=np.nan, strategy='median')
    imp_mean.fit(data)
    SimpleImputer()
    imputed_data = pd.DataFrame(imp_mean.transform(data))
    imputed_data.columns = data.columns
    imputed_data.index = data.index

    data = imputed_data

    performance = data['performance']
    data = data.drop(columns=['performance'])

    X_train, X_test, y_train, y_test = train_test_split(data, performance, train_size=0.8)

    clf = RandomForestRegressor(max_features=None, oob_score=True)
    clf.fit(X_train, y_train)

    accuracy = round(clf.score(X_test, y_test), 3)

    data = data.drop(columns=['previous'])
    if random:
        data['random'] = pd.Series([random.random() for x in range(len(data))])
    importance = dropcol_importances(clf, data, performance)

    # plot feature importance
    ax = pd.Series(importance['Importance']).plot(kind='barh')
    y_labels = importance.index
    ax.set_yticklabels(y_labels)
    plt.xlabel("Change in OOB Error")
    plt.title("Random Forest Regression Feature Importance")

    plt.tight_layout()
    graph = get_image()
    return [graph, accuracy]
