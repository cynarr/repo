def read_csv_map(filename):
    import csv

    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)
        return {row[0]: row[1] for row in reader}


def read_csv_map_set(filename):
    import csv

    res = {}
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            res.setdefault(row[0], set()).add(row[1])
    return res


def read_csv_map_map_set(filename):
    import csv

    res = {}
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            res.setdefault(row[0], {}).setdefault(row[1], set()).add(row[2])
    return res


def read_csv_set(filename):
    import csv

    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)
        return {row[0] for row in reader}
