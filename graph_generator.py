import pandas as pd
import matplotlib.pyplot as plt

# Adding colors to distinguish each bar
colors = ['blue', 'green', 'red', 'purple', 'orange', 'magenta']


def get_total_jobs_report_02(filename):
    """
    Creates a graph, for report 2, that plots the all cities
    total jobs as a histogram.

    Parameters
    ----------
    filename : str

    Returns
    -------
    N/A

    """
    file = pd.read_csv(filename)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(file['Area'], file['Area Totals'], color=colors)
    plt.xlabel('Location')
    plt.ylabel('Number of Jobs')
    plt.title('Total Jobs in each location')
    plt.xticks(rotation=45, ha='right')

    legend_labels = []
    for city in file['Area']:
        legend_labels.append(city)

    plt.legend(bars, legend_labels, title='Legend')

    plt.tight_layout()
    plt.show()


def get_difference_in_jobs_report_01(filename):
    """
    Creates graphs, for report 1, that plots the differences of each job
    in all the cities in a histogram.

    Parameters
    ----------
    filename : str

    Returns
    -------
    N/A

    """
    file = pd.read_csv(filename)

    for job in file.columns[1:]:
        plt.figure(figsize=(10, 6))
        bars = plt.bar(file['Area'], file[job], color=colors)
        plt.title(f'{job} in each location')
        plt.xlabel('Location')
        plt.ylabel('Number of Jobs')
        plt.xticks(rotation=45)

        legend_labels = []
        for loc in file['Area']:
            legend_labels.append(loc)

        plt.legend(bars, legend_labels, title='Legend')

        plt.tight_layout()
        plt.show()


def get_total_each_job_in_city(filename):
    """
    Creates graphs, for report 1, that plots the distribution for each
    city's jobs.

    Parameters
    ----------
    filename : str

    Returns
    -------
    N/A

    """
    file = pd.read_csv(filename)

    for i, row in file.iterrows():
        area = row['Area']
        data = row[1:]
        job = file.columns[1:]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(job, data, color=colors)
        plt.title(f'Distribution of jobs in {area}')
        plt.xlabel('Job Type')
        plt.ylabel('Number of Jobs')
        plt.xticks(rotation=45)

        plt.legend(bars, job, title='Legend')

        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
     get_total_jobs_report_02('Values_02.csv')
    # get_difference_in_jobs_report_01('Values_01.csv')
    # get_total_each_job_in_city('Values_01.csv')
