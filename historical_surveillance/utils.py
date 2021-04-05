import base64
from io import BytesIO
import matplotlib.pyplot as plt


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
    # commented out but to be used later for stacked bar plots

    # fig, ax = plt.subplots(figsize=(10, 8))
    # ax.bar(x, y, color='b', width=0.25, label='total enrollment')
    # ax.bar(x, z, color='g', width=0.25, bottom=y, label='capacity of school')
    # ax.set_title(school_name)

    else:
        title = school_name
        plt.figure(figsize=(10, 8))
        plt.title(title)
        plt.plot(x, y, 'b-', label='enrollments')
        plt.plot(x, z, 'g-', label='capacity')
        #plt.ylim(0, max(y) + 100)
        plt.ylabel("Total Enrollment / Capacity")
        plt.xlabel("Academic Year")
        plt.legend()
    # else:
    # title = school_name
    # plt.title(title)
    # sns.countplot('name_of_school', data=data)
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


"""
def get_school_plot(chart_type, **kwargs):
    plt.switch_backend('AGG')
    # total enrollment
    x = kwargs.get('x')
    # y = capacity of school
    y = kwargs.get('y')
    # selected year

    year = kwargs.get('academic_year')
    school = kwargs.get('name_of_school')
    district = kwargs.get('district_name')
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
    # commented out but to be used later for stacked bar plots

    # fig, ax = plt.subplots(figsize=(10, 8))
    # ax.bar(x, y, color='b', width=0.25, label='total enrollment')
    # ax.bar(x, z, color='g', width=0.25, bottom=y, label='capacity of school')
    # ax.set_title(school_name)

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
    # else:
    # title = school_name
    # plt.title(title)
    # sns.countplot('name_of_school', data=data)
    plt.tight_layout()
    graph = get_image()
    return graph
"""
