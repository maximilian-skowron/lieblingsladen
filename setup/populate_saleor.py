import requests
import os

GRAPHQL_URL = 'http://localhost:8000/graphql/'
GRAPHQL_BEAR_TOKEN = os.environ.get('GRAPHQL_BEAR_TOKEN')


def execute_querry(query: str):
    headers = {"Authorization": "Bearer {0}".format(GRAPHQL_BEAR_TOKEN)}

    r = requests.post(GRAPHQL_URL, json={'query': query}, headers=headers)
    print(r.json())
    return r


def get_query_create_category(name: str, parrent_id: str = None):

    parrent_part = ', parent: "{0}"'.format(parrent_id)

    query = """ mutation testCreate {
            categoryCreate(input: { name: "%s"} %s) {
                category {
                    name
                    id
                }
            }
        }""" % (name, '' if parrent_id is None else parrent_part)

    return query


def create_categories():
    categories = [
        ('Verpfelgung', ['Säfte', 'Alkoholische Getränke',
                         'Obst', 'Gemüse', 'Lieferservices']),

        ('Haushalt', ['Reinigungsutensilien', 'Verbrauchsgüter']),
        ('Freizeit', ['Veranstaltungen', 'Aktivitäten']),
    ]

    category_id_dict = {}

    for category in categories:
        root_category_name, sub_category_name_list = category

        r_json = execute_querry(
            get_query_create_category(root_category_name)).json()

        p_id = r_json['data']['categoryCreate']['category']['id']

        for sub_category in sub_category_name_list:
            r_json = execute_querry(get_query_create_category(
                sub_category, parrent_id=p_id))

            name = r_json['data']['categoryCreate']['category']['name']
            s_id = r_json['data']['categoryCreate']['category']['name']

            category_id_dict[name] = s_id

    return category_id_dict


if __name__ == '__main__':
    category_dict = create_categories()

    pass
