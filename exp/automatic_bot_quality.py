import os
import re
import argparse

from django.conf import settings
import yaml
import matplotlib.pyplot as plt
import numpy as np

from utils.ods_api.iterators import CatalogIterator
import chatbot.automatic as AutoSemanticBot
from chatbot.semantic_engine import _get_uri_suffix

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot_app.settings")

ODS_LANGUAGES = ['fr', 'en']

REGEX_REFERENCE_FIELD = re.compile('\$\((.*?)\)')


def main(number):
    api_key = settings.DATA_API_KEY
    labels = ODS_LANGUAGES
    score_labels = []
    score_labels_cov = []
    score_labels_con = []
    classes = {}
    themes_quality = {}
    for label in labels:
        catalog = datasets_by_lang(label)
        cpt = 0
        score_label = 0
        score_label_cov = 0
        score_label_con = 0
        for i in range(0, number):
            print(f'{label} {i}/{number}')
            try:
                dataset = catalog.__next__()
                rml_mapping = AutoSemanticBot.semantize(dataset.domain_id, dataset.dataset_id, api_key)
                cpt += 1
                scores = evamap_get_score(rml_mapping, dataset)
                # lang
                score_label += scores['total']
                score_label_cov += scores['coverability']
                score_label_con += scores['connectivity']
                # classes
                update_classes(classes, rml_mapping)
                # themes
                if dataset.themes:
                    for theme in dataset.themes:
                        if theme in themes_quality:
                            themes_quality[theme]['score'] = themes_quality[theme]['score'] + scores['total']
                            themes_quality[theme]['n'] = themes_quality[theme]['n'] + 1
                        else:
                            themes_quality[theme] = {'score': scores['total'], 'n': 1}
            except StopIteration:
                pass
        score_labels.append(round(score_label/cpt, 3))
        score_labels_cov.append(round(score_label_cov/cpt, 3))
        score_labels_con.append(round(score_label_con/cpt, 3))
    plot_lang_quality(labels, score_labels, score_labels_cov, score_labels_con)
    plot_class(classes)
    plot_theme_quality(themes_quality)


def datasets_by_lang(lang):
    # default order: most popular
    return CatalogIterator('data', where=f"language='{lang}' AND source_domain_title='Public'", rows=10)


def evamap_get_score(rml_mapping, dataset):
    coverability = evamap_vertical_coverage(rml_mapping, dataset.fields)
    connectivity = evamap_graph_connectivity(rml_mapping)
    score = {'total': ((coverability + connectivity)/2),
     'coverability': coverability,
     'connectivity': connectivity}
    return score


def evamap_graph_connectivity(rml_mapping):
    mapping = yaml.load(rml_mapping, Loader=yaml.FullLoader)
    connection_dict = {k: {k} for k in mapping['mappings']}
    if connection_dict:
        for i in range(0, len(connection_dict)):
            for resource, value in mapping['mappings'].items():
                for po in value['predicateobjects']:
                    if isinstance(po, dict):
                        object_resource = po['objects'][0]['mapping']
                        connection_dict[resource] |= connection_dict[object_resource]
                        connection_dict[object_resource] |= connection_dict[resource]
        isolated_graphs = set()
        for resource, connec in connection_dict.items():
            isolated_graphs.add(len(connec))
        return 1/len(isolated_graphs)
    return 0


def update_classes(classes, rml_mapping):
    mapping = yaml.load(rml_mapping, Loader=yaml.FullLoader)
    for resource, value in mapping['mappings'].items():
        for po in value['predicateobjects']:
            if isinstance(po, list):
                if po[0] == 'a':
                    cl = _get_uri_suffix(po[1])
                    if cl in classes:
                        classes[cl] = classes[cl] + 1
                    else:
                        classes[cl] = 1


def evamap_vertical_coverage(rml_mapping, dataset_fields):
    referenced_fields = re.findall(REGEX_REFERENCE_FIELD, rml_mapping)
    if referenced_fields:
        refs = set()
        for referenced_field in referenced_fields:
            refs.add(referenced_field)
        return len(refs)/len(dataset_fields)
    return 0


def plot_lang_quality(labels, score_label, score_labels_cov, score_labels_con):
    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width, score_label, width, label='Average')
    rects2 = ax.bar(x, score_labels_cov, width, label='Coverability')
    rects3 = ax.bar(x + width, score_labels_con, width, label='Connectability')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('EvaMap score (Connectability & Coverability) max=1.0')
    ax.set_title(f'Average quality of RDF mappings grouped by language')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 3, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    fig.tight_layout()
    plt.show()


def plot_theme_quality(theme_quality):
    labels = [label for label in theme_quality]
    scores = []
    for label, value in theme_quality.items():
        scores.append(round(value['score']/value['n'], 3))
        print(f"{label}: {round(value['score']/value['n'],3)}")
    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars
    fig, ax = plt.subplots()
    rects = ax.bar(x, scores, width)
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('EvaMap score (Connectability & Coverability) max=1.0')
    ax.set_title(f'Average quality of RDF mappings grouped by theme')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 3, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    autolabel(rects)
    fig.tight_layout()
    plt.show()


def plot_class(classes):
    labels = []
    tot = 0
    sizes = []
    for cls, value in classes.items():
        labels.append(cls)
        tot += value
        sizes.append(value)
    fig1, ax1 = plt.subplots()
    ax1.set_title(f'Classes discovered by the SeamnticBot')
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Auto SemanticBot experience.')
    parser.add_argument('-n', '-number', type=int, help='number of datasets in each category', required=True)
    args = parser.parse_args()
    main(args.n)
