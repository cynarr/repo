def read_csv_map(filename):
    import csv

    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        return {row[0]: row[1] for row in reader}


def read_csv_set(filename):
    import csv

    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        return {row[0] for row in reader}
