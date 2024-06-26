import sys
import io
import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import subprocess
from datetime import datetime

class MetricTracker:
    def __init__(self, metrics, filename='metrics_log.csv'):
        self.metrics = metrics
        self.filename = filename
        self.old_filename = 'metrics_log.old.csv'

        # Rename existing file to old file
        if os.path.exists(self.filename):
            if os.path.exists(self.old_filename):
                os.remove(self.old_filename)
            os.rename(self.filename, self.old_filename)

        # Create a new file with a header
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.metrics)

    def log_metrics(self, *args):
        if len(args) != len(self.metrics):
            raise ValueError("Number of arguments does not match the number of metrics initialized.")
        
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(list(args))

    def plot_current_metrics(self):
        df = pd.read_csv(self.filename)
        x_axis = df.columns[0]
        for col in df.columns[1:]:
            plt.plot(df[x_axis], df[col], marker='o', linestyle='-', label=col)
        
        plt.title('Current Metrics')
        plt.xlabel('Time or Counter')
        plt.ylabel('Metric Value')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_comparison(self):
        # Plot old metrics
        if os.path.exists(self.old_filename):
            df_old = pd.read_csv(self.old_filename)
            x_axis = df_old.columns[0]
            for col in df_old.columns[1:]:
                plt.plot(df_old[x_axis], df_old[col], marker='o', linestyle='-', color='gray', label=f"Old {col}")

        # Plot current metrics
        df_new = pd.read_csv(self.filename)
        x_axis = df_new.columns[0]
        for col in df_new.columns[1:]:
            plt.plot(df_new[x_axis], df_new[col], marker='o', linestyle='-', label=f"Current {col}")

        plt.title('Comparison of Current and Old Metrics')
        plt.xlabel('Time or Counter')
        plt.ylabel('Metric Value')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


def get_tags_with_dates(tag_pattern):
    tags = subprocess.check_output(['git', 'tag', '-l', tag_pattern]).decode().strip().split()
    tag_dates = {}
    for tag in tags:
        commit_hash = subprocess.check_output(['git', 'rev-list', '-n', '1', tag]).decode().strip()
        commit_date = subprocess.check_output(['git', 'show', '-s', '--format=%cd', commit_hash]).decode().strip()
        tag_dates[tag] = commit_date
    return tag_dates

def plot_data(tags_with_dates, filename, tag_name):
    plt.figure(figsize=(10, 5))
    plt.title(f'Metrics Over Time for {tag_name}')
    plt.xlabel('Time or Counter')
    plt.ylabel('Metric Value')
    
    for tag, date in tags_with_dates.items():
        file_content = subprocess.check_output(['git', 'show', f"{tag}:{filename}"]).decode()
        df = pd.read_csv(io.StringIO(file_content))

        if tag_name in df.columns:
            metric_column = tag_name
        else:
            metric_column = df.columns[1]  # Fallback to second column
        
        x_axis = df.columns[0]  # Always use the first column for the x-axis
        plt.plot(df[x_axis], df[metric_column], marker='o', linestyle='-', label=f"{tag} ({date})")

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    if len(sys.argv) != 2:
        print("Usage: python MetricTracker.py <tag_name>")
        print("Note: <tag_name> does not include 'plot-' prefix")
        return 1

    tag_name = sys.argv[1]
    tags_dates = get_tags_with_dates(f'plot-{tag_name}*')
    plot_data(tags_dates, 'metrics_log.csv', tag_name)
    return 0

if __name__ == '__main__':
    sys.exit(main())
