import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO


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


def get_plot(chart_type, *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10, 4))
    x = kwargs.get('x')
    y = kwargs.get('y')
    z = kwargs.get('z')
    school_name = kwargs.get('name_of_school')
    data = kwargs.get('data')

    if chart_type == 'barplot':
        width = 0.35
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.bar(x, y, width, label='total enrollment')
        ax.bar(x, z, width, bottom=y,
               label='capacity of school')
        ax.set_ylabel('Total Enrollment / Capacity')
        ax.set_title(school_name)
        ax.legend()

    else:
        title = school_name
        plt.title(title)
        plt.plot(x, y, 'b-')
        plt.plot(x, z, 'r-')
    # else:
    # title = school_name
    # plt.title(title)
    # sns.countplot('name_of_school', data=data)
    plt.tight_layout()
    graph = get_image()
    return graph
