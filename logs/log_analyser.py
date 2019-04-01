import codecs
import csv
import argparse
import re
import datetime

METRIC_FILE = 'logs/chatbot_metrics.txt'
CLASSES_FILE = 'logs/class_correspondances.csv'
PROPERTIES_FILE = 'logs/property_correspondances.csv'
UNDER_BRACKETS_RE = re.compile('\[(.*?)\]')
DATE_FORMAT = '%Y-%m-%d %H:%M:%S,%f'

CSV_PROPERTIES_HEADER = ['domain_field', 'domain_class', 'property_uri', 'field_range', 'decision']
CSV_CLASSES_HEADER = ['field_name', 'class_uri', 'decision']

CSV_DELIMITER = '|'
REPLACE_DELIMITER = ' '

METRIC_FILE_TREMPLATE = '''nb_semantized_dataset: {}
nb_canceled_semantization: {}
nb_failed_semantization: {}
avg_semantization_time: {}sec'''


def generate_files(datasets):
    nb_semantization_begin = 0
    nb_finished_semantization = 0
    nb_aborted_semantization = 0
    total_seconds_semantization = 0
    nb_failed_semantization = 0
    total_avg_time = 0
    with codecs.open(PROPERTIES_FILE, "w") as properties_file:
        properties_file_writer = csv.writer(properties_file, delimiter=CSV_DELIMITER)
        properties_file_writer.writerow(CSV_PROPERTIES_HEADER)
        with codecs.open(CLASSES_FILE, "w") as classes_file:
            classes_file_writer = csv.writer(classes_file, delimiter=CSV_DELIMITER)
            classes_file_writer.writerow(CSV_CLASSES_HEADER)
            for dataset_id, dataset_semantization in datasets.items():
                # Metrics update
                if dataset_semantization['start_time']:
                    nb_semantization_begin += 1
                    if dataset_semantization['end_time']:
                        nb_finished_semantization += 1
                        time_difference = (dataset_semantization['end_time'] - dataset_semantization['start_time']).total_seconds()
                        # TODO log time to semantize (not an estimation)
                        if 10 < time_difference < 1800:
                            total_avg_time += 1
                            total_seconds_semantization += time_difference
                else:
                    nb_failed_semantization += 1
                # CSV update
                # Classes
                for class_correspondance in dataset_semantization['correspondances']['classes']:
                    row = []
                    for column_name in CSV_CLASSES_HEADER:
                        row.append(class_correspondance[column_name])
                    classes_file_writer.writerow(row)
                for property_correspondance in dataset_semantization['correspondances']['properties']:
                    row = []
                    for column_name in CSV_PROPERTIES_HEADER:
                        row.append(property_correspondance[column_name])
                    properties_file_writer.writerow(row)
    avg_semantization_time_per_dataset = total_seconds_semantization / total_avg_time
    nb_aborted_semantization = nb_semantization_begin - nb_finished_semantization
    with open(METRIC_FILE, 'w') as metric_file:
        metric_file.write(METRIC_FILE_TREMPLATE.format(nb_finished_semantization,
                                                       nb_aborted_semantization,
                                                       nb_failed_semantization,
                                                       avg_semantization_time_per_dataset))


def parse_line(line, datasets):
    strings_under_brackets = re.findall(UNDER_BRACKETS_RE, line)
    if strings_under_brackets:
        dataset_id = strings_under_brackets[3]
        if not datasets.get(dataset_id):
            datasets[dataset_id] = {'start_time': None, 'end_time':None, 'correspondances': {'properties':[], 'classes':[]}}
        if 'Starting semantization' in line:
            # Starting semantization time:
            # e.g:[2018-12-13 08:34:09,391] [INFO] [correspondance_api] [roman-emperors@public] Starting semantization
            if not datasets[dataset_id]['start_time']:
                t = datetime.datetime.strptime(strings_under_brackets[0], DATE_FORMAT)
                datasets[dataset_id]['start_time'] = t
        elif 'semantization complete' in line:
            # Semantization complete time:
            # e.g:[2018-12-13 09:41:12,713] [INFO] [correspondance_api] [roman-emperors@public] semantization complete
            if not datasets[dataset_id]['end_time']:
                t = datetime.datetime.strptime(strings_under_brackets[0], DATE_FORMAT)
                datasets[dataset_id]['end_time'] = t
        elif 'No correspondances found' in line:
            # No classes found for this dataset
            # e.g:[2018-12-14 09:43:56,440] [INFO] [correspondance_api] [roman-emperors@public] No correspondances found
            return
        elif len(strings_under_brackets) > 8:
            # Property correspondance
            # e.g:[2018-12-13 09:41:12,680] [INFO] [correspondance_api] [roman-emperors@public]...
            # [Property] [CONFIRMED] field_domain:[name] class_domain[Royalty]...
            # -- uri:[http://www.loc.gov/mads/rdf/v1#birthPlace] --> field_range:[birth_cty]
            property_correspondance = {'decision': strings_under_brackets[5],
                                       'domain_field': strings_under_brackets[6],
                                       'domain_class': strings_under_brackets[7],
                                       'property_uri': strings_under_brackets[8],
                                       'field_range': strings_under_brackets[9]}
            datasets[dataset_id]['correspondances']['properties'].append(property_correspondance)
        else:
            # Class correspondance
            # e.g: [2018-12-13 09:41:12,680] [INFO] [correspondance_api] [roman-emperors@public] [Class] [CONFIRMED]...
            # field:[birth_cty] uri:[http://dbpedia.org/ontology/Settlement]
            class_correspondance = {'decision': strings_under_brackets[5],
                                    'field_name': strings_under_brackets[6],
                                    'class_uri': strings_under_brackets[7]}
            datasets[dataset_id]['correspondances']['classes'].append(class_correspondance)


def main():
    parser = argparse.ArgumentParser(prog='log_analyser', description='return statistics on chatbot usage')
    parser.add_argument('log_file_path', metavar='FP', type=str, nargs='+',
                        help='Path to the log file to analyse')
    args = parser.parse_args()
    filepath = args.log_file_path[0]
    datasets = {}
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            parse_line(fp.readline().strip(), datasets)
            line = fp.readline()
    generate_files(datasets)


if __name__ == "__main__":
    main()
