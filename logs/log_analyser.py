import codecs
import csv
import argparse
import re

METRIC_FILE = 'logs/chatbot_metrics.txt'
CLASSES_FILE = 'logs/class_correspondances.csv'
PROPERTIES_FILE = 'logs/property_correspondances.csv'
UNDER_BRACKETS_RE = re.compile('\[(.*?)\]')
DATE_FORMAT = '%Y-%m-%d %H:%M:%S,%f'

CSV_PROPERTIES_HEADER = ['domain_field',
                         'domain_class',
                         'property_uri',
                         'field_range',
                         'decision',
                         'field_type',
                         'field_is_facet']

CSV_CLASSES_HEADER = ['field_name',
                      'class_uri',
                      'decision',
                      'field_type',
                      'field_is_facet']

CSV_DELIMITER = '|'
REPLACE_DELIMITER = ' '

METRIC_FILE_TREMPLATE = '''nb_semantized_dataset: {}
nb_canceled_semantization: {}
nb_failed_semantization: {}
avg_server_time: {}sec
avg_client_time: {}sec
avg_total_time: {}sec'''


def generate_files(datasets):
    avg_server_time = []
    avg_client_time = []
    with codecs.open(PROPERTIES_FILE, "w") as properties_file:
        properties_file_writer = csv.writer(properties_file, delimiter=CSV_DELIMITER)
        properties_file_writer.writerow(CSV_PROPERTIES_HEADER)
        with codecs.open(CLASSES_FILE, "w") as classes_file:
            classes_file_writer = csv.writer(classes_file, delimiter=CSV_DELIMITER)
            classes_file_writer.writerow(CSV_CLASSES_HEADER)
            for dataset_id, dataset_semantization in datasets['datasets'].items():
                # Metrics update
                if dataset_semantization['server_time'] and dataset_semantization['client_time']:
                    avg_server_time.append(sum(dataset_semantization['server_time'])/len(dataset_semantization['server_time']))
                    avg_client_time.append(sum(dataset_semantization['client_time'])/len(dataset_semantization['client_time']))
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
    nb_aborted_semantization = datasets['nb_semantization_begin'] - datasets['nb_semantization_finished']
    with open(METRIC_FILE, 'w') as metric_file:
        if avg_server_time and avg_client_time:
            avg_server_time = sum(avg_server_time)/len(avg_server_time)
            avg_client_time = sum(avg_client_time)/len(avg_client_time)
        avg_total_time = avg_server_time + avg_client_time
        metric_file.write(METRIC_FILE_TREMPLATE.format(datasets['nb_semantization_finished'],
                                                       nb_aborted_semantization,
                                                       datasets['nb_semantization_failed'],
                                                       avg_server_time,
                                                       avg_client_time,
                                                       avg_total_time))


def parse_line(line, datasets):
    strings_under_brackets = re.findall(UNDER_BRACKETS_RE, line)
    if strings_under_brackets:
        dataset_id = strings_under_brackets[3]
        if not datasets['datasets'].get(dataset_id):
            datasets['datasets'][dataset_id] = {'server_time': [], 'client_time':[], 'correspondances': {'properties': [], 'classes': []}}
        if 'Starting semantization' in line:
            # Starting semantization:
            # e.g:[2018-12-13 08:34:09,391] [INFO] [correspondance_api] [roman-emperors@public] Starting semantization
            datasets['nb_semantization_begin'] += 1
        elif 'semantization complete' in line:
            # Semantization complete:
            # e.g:[2018-12-13 09:41:12,713] [INFO] [correspondance_api] [roman-emperors@public] semantization complete
            datasets['nb_semantization_finished'] += 1
        elif 'No correspondances found' in line:
            # No classes found for this dataset
            # e.g:[2018-12-14 09:43:56,440] [INFO] [correspondance_api] [roman-emperors@public] No correspondances found
            datasets['nb_semantization_failed'] += 1
        elif '[Time]' in line:
            # Semantization time:
            # e.g:[2019-04-18 10:22:17,209] [INFO] [correspondance_api] [roman-emperors@public] [Time]...
            # server_time:[42] client_time:[35]
            datasets['datasets'][dataset_id]['server_time'].append(int(strings_under_brackets[5]))
            datasets['datasets'][dataset_id]['client_time'].append(int(strings_under_brackets[6]))
        elif len(strings_under_brackets) == 12:
            # Property correspondance
            # e.g:[2018-12-13 09:41:12,680] [INFO] [correspondance_api] [roman-emperors@public]...
            # [Property] [CONFIRMED] field_domain:[name] class_domain[Royalty]...
            # -- uri:[http://www.loc.gov/mads/rdf/v1#birthPlace] --> field_range:[birth_cty]
            # field_type:[text] field_is_facet:[False]
            property_correspondance = {'decision': strings_under_brackets[5],
                                       'domain_field': strings_under_brackets[6],
                                       'domain_class': strings_under_brackets[7],
                                       'property_uri': strings_under_brackets[8],
                                       'field_range': strings_under_brackets[9],
                                       'field_type': strings_under_brackets[10],
                                       'field_is_facet': strings_under_brackets[11]}
            datasets['datasets'][dataset_id]['correspondances']['properties'].append(property_correspondance)
        elif len(strings_under_brackets) == 10:
            # Class correspondance
            # e.g: [2018-12-13 09:41:12,680] [INFO] [correspondance_api] [roman-emperors@public] [Class] [CONFIRMED]...
            # field:[birth_cty] uri:[http://dbpedia.org/ontology/Settlement]
            # field_type:[text] field_is_facet:[False]
            class_correspondance = {'decision': strings_under_brackets[5],
                                    'field_name': strings_under_brackets[6],
                                    'class_uri': strings_under_brackets[7],
                                    'field_type': strings_under_brackets[8],
                                    'field_is_facet': strings_under_brackets[9]}
            datasets['datasets'][dataset_id]['correspondances']['classes'].append(class_correspondance)


def main():
    parser = argparse.ArgumentParser(prog='log_analyser', description='return statistics on chatbot usage')
    parser.add_argument('log_file_path', metavar='FP', type=str, nargs='+',
                        help='Path to the log file to analyse')
    args = parser.parse_args()
    filepath = args.log_file_path[0]
    datasets = {'nb_semantization_begin': 0, 'nb_semantization_finished': 0, 'nb_semantization_failed': 0, 'datasets': {}}
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            parse_line(line.strip(), datasets)
            line = fp.readline()
    generate_files(datasets)


if __name__ == "__main__":
    main()
