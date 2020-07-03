import os
import re
import argparse

from django.conf import settings
import yaml
import matplotlib.pyplot as plt
import numpy as np

from utils.ods_api.iterators import CatalogIterator
import chatbot.automatic as AutoSemanticBot

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot_app.settings")

ODS_POPULAR_THEMES = ['Administration, Gouvernement, Finances publiques, Citoyenneté',
                      'Référentiels géographiques',
                      'Transports, Déplacements',
                      'Economie, Business, PME, Développement économique, Emploi',
                      'Spatial planning, Town planning, Buildings, Equipment, Housing',
                      'Environment',
                      'World',
                      'Economy, Business, SME, Economic development, Employment',
                      'Santé',
                      'SPort, Loisirs'
                      ]
ODS_LANGUAGES = ['fr', 'en']

REGEX_REFERENCE_FIELD = re.compile('\$\((.*?)\)')


def main(type, number):
    api_key = settings.DATA_API_KEY
    if type == 'theme':
        labels = ODS_POPULAR_THEMES
    else:
        labels = ODS_LANGUAGES
    score_labels = []
    for label in labels:
        if type == 'theme':
            catalog = datasets_by_theme(label)
        else:
            catalog = datasets_by_lang(label)
        cpt = 0
        score_label = 0
        for i in range(0, number):
            print(f'{label} {i}/{number}')
            try:
                dataset = catalog.__next__()
                rml_mapping = AutoSemanticBot.semantize(dataset.domain_id, dataset.dataset_id, api_key)
                cpt += 1
                score_label += evamap_get_score(rml_mapping, dataset)
            except StopIteration:
                pass
        score_labels.append(score_label/cpt)
    plot(labels, score_labels, type)


def datasets_by_lang(lang):
    # default order: most popular
    return CatalogIterator('data', where=f"language='{lang}' AND source_domain_title='Public'", rows=10)


def datasets_by_theme(theme):
    # default order: most popular
    return CatalogIterator('data', refine=f"theme='{theme}' AND source_domain_title='Public'", rows=10)


def evamap_get_score(rml_mapping, dataset):
    return (evamap_graph_connectivity(rml_mapping)+evamap_vertical_coverage(rml_mapping, dataset.fields))/2


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


def evamap_vertical_coverage(rml_mapping, dataset_fields):
    referenced_fields = re.findall(REGEX_REFERENCE_FIELD, rml_mapping)
    if referenced_fields:
        refs = set()
        for referenced_field in referenced_fields:
            refs.add(referenced_field)
        return len(refs)/len(dataset_fields)
    return 0


def plot(labels, score_label, type):
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x, score_label, width)
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('EvaMap score (Connectability & Coverability) max=1.0')
    ax.set_title(f'Average quality of RDF mappings grouped by {type}')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    autolabel(rects1)
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Auto SemanticBot experience.')
    parser.add_argument('-t', '-type', type=str, help='theme or language', required=True)
    parser.add_argument('-n', '-number', type=int, help='number of datasets in each category', required=True)
    args = parser.parse_args()
    main(args.t, args.n)
