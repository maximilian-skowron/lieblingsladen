import requests
import os
import random

GRAPHQL_URL = 'http://localhost:8000/graphql/'
GRAPHQL_BEAR_TOKEN = os.environ.get('GRAPHQL_BEAR_TOKEN')


def execute_querry(query: str):
    headers = {"Authorization": "Bearer {0}".format(GRAPHQL_BEAR_TOKEN)}

    r = requests.post(GRAPHQL_URL, json={'query': query}, headers=headers)
    print(r.json())
    return r


def get_query_create_category(name: str, parrent_id: str = None):

    parrent_part = ', parent: "{0}"'.format(parrent_id)

    query = """ mutation c_category {
            categoryCreate(input: { name: "%s"} %s) {
                category {
                    name
                    id
                }
            }
        }""" % (name, '' if parrent_id is None else parrent_part)

    return query


def get_query_create_example_product(name: str, product_type_id: str, category_id: str):
    lorem_ipsum = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. "

    query = """mutation exampleProduct {
            productCreate (input: {name:"%s", productType:"%s", category:"%s", basePrice:"%s", description:"%s", isPublished:true}){
                product {
                name
                }
            }
        }""" % (name, product_type_id, category_id, random.uniform(0.5, 9.9), lorem_ipsum)

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


def create_products(category_dict):
    products = [
        ('Orangensaft', '', category_dict['Säfte']),
        ('Apfelsaft', '', category_dict['Säfte']),
        ('Wein', '', category_dict['Alkoholische Getränke']),
        ('Bier', '', category_dict['Alkoholische Getränke']),
        ('Banane', '', category_dict['Obst']),
        ('Birne', '', category_dict['Obst']),
        ('Gurke', '', category_dict['Gemüse']),
        ('Tomate', '', category_dict['Gemüse']),
        ('Blitzbringer', '', category_dict['Lieferservices']),
        ('Windgeschwind', '', category_dict['Lieferservices']),
        ('Super Lappen', '', category_dict['Reinigungsutensilien']),
        ('Spüli', '', category_dict['Reinigungsutensilien']),
        ('Klopapier', '', category_dict['Verbrauchsgüter']),
        ('Zahnpasta', '', category_dict['Verbrauchsgüter']),
        ('Trash Gera', '', category_dict['Veranstaltungen']),
        ('Seven Club', '', category_dict['Veranstaltungen']),
        ('Tierpark Gera', '', category_dict['Aktivitäten']),
        ('Sky Motion Team', '', category_dict['Aktivitäten']),
    ]

    for product in products:
        name, product_type_id, category_id = product
        execute_querry(get_query_create_example_product(
            name, product_type_id, category_id))


if __name__ == '__main__':
    category_dict = create_categories()
    create_products(category_dict)
    pass
