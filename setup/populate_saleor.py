import requests
import os
import random
import os
from aiogqlc import GraphQLClient
from urllib.request import urlretrieve
import asyncio
import itertools
import cgi
import tempfile


GRAPHQL_URL = 'http://localhost:8000/graphql/'
GRAPHQL_BEAR_TOKEN = os.environ.get('GRAPHQL_BEAR_TOKEN')


async def execute_querry_upload_file(query: str, file_path):
    variables = {
        'file': open(file_path, 'rb'),
    }
    headers = {"Authorization": "Bearer {0}".format(GRAPHQL_BEAR_TOKEN)}

    client = GraphQLClient(GRAPHQL_URL, headers=headers)
    r = await client.execute(query, variables=variables)
    print(await r.json())


def execute_querry(query: str):
    headers = {"Authorization": "Bearer {0}".format(GRAPHQL_BEAR_TOKEN)}

    r = requests.post(GRAPHQL_URL, json={'query': query}, headers=headers)
    print(r.json())
    return r.json()


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
            productCreate (input: {name:"%s", productType:"%s", category:"%s", basePrice:"%.2f", description:"%s", isPublished:true}){
                product {
                name
                id
                }
            }
        }""" % (name, product_type_id, category_id, random.uniform(0.5, 9.9), lorem_ipsum)

    return query


def get_query_create_product_type(name: str):
    query = """mutation exampleProductType {
            productTypeCreate (input: {name:"%s", }){
                    productType{
                        name
                        id
                    }
            }
        }""" % (name)

    return query


def get_query_product_img_upload(product_id: str, image_name: str):
    query = """mutation exampleProductImage($file: Upload!) {
        productImageCreate (input: {product: "%s", image: $file}){
            productErrors{message}
            image{id}
        }
    }""" % (product_id)
    return query


def create_p_types():
    types = [
        ('DefaultProduct'),
        ('Veranstaltung'),
        ('Getränk'),
        ('Frischwaare'),
        ('Lieferservice'),
    ]

    id_dict = {}

    for type_name in types:
        r_json = execute_querry(get_query_create_product_type(type_name))
        t_id = r_json['data']['productTypeCreate']['productType']['id']
        id_dict[type_name] = t_id

    return id_dict


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
            get_query_create_category(root_category_name))

        p_id = r_json['data']['categoryCreate']['category']['id']

        for sub_category in sub_category_name_list:
            r_json = execute_querry(get_query_create_category(
                sub_category, parrent_id=p_id))
            print(r_json)
            name = r_json['data']['categoryCreate']['category']['name']
            s_id = r_json['data']['categoryCreate']['category']['id']

            category_id_dict[name] = s_id

    return category_id_dict


def create_products(category_dict: dict, p_type_dict: dict):
    products = [
        ('Orangensaft', p_type_dict['Getränk'], category_dict['Säfte']),
        ('Apfelsaft', p_type_dict['Getränk'], category_dict['Säfte']),
        ('Wein', p_type_dict['Getränk'],
         category_dict['Alkoholische Getränke']),
        ('Bier', p_type_dict['Getränk'],
         category_dict['Alkoholische Getränke']),
        ('Banane', p_type_dict['Frischwaare'], category_dict['Obst']),
        ('Birne', p_type_dict['Frischwaare'], category_dict['Obst']),
        ('Gurke', p_type_dict['Frischwaare'], category_dict['Gemüse']),
        ('Tomate', p_type_dict['Frischwaare'], category_dict['Gemüse']),
        ('Blitzbringer', p_type_dict['Lieferservice'],
         category_dict['Lieferservices']),
        ('Windgeschwind', p_type_dict['Lieferservice'],
         category_dict['Lieferservices']),
        ('Super Lappen', p_type_dict['DefaultProduct'],
         category_dict['Reinigungsutensilien']),
        ('Spüli', p_type_dict['DefaultProduct'],
         category_dict['Reinigungsutensilien']),
        ('Klopapier', p_type_dict['DefaultProduct'],
         category_dict['Verbrauchsgüter']),
        ('Zahnpasta', p_type_dict['DefaultProduct'],
         category_dict['Verbrauchsgüter']),
        ('Trash Gera', p_type_dict['Veranstaltung'],
         category_dict['Veranstaltungen']),
        ('Seven Club', p_type_dict['Veranstaltung'],
         category_dict['Veranstaltungen']),
        ('Tierpark Gera',
         p_type_dict['Veranstaltung'], category_dict['Aktivitäten']),
        ('Sky Motion Team',
         p_type_dict['Veranstaltung'], category_dict['Aktivitäten']),
    ]

    product_id_dict = {}

    for product in products:
        name, product_type_id, category_id = product
        # print(get_query_create_example_product(
        #   name, product_type_id, category_id))
        r_json = execute_querry(get_query_create_example_product(
            name, product_type_id, category_id))

        name = r_json['data']['productCreate']['product']['name']
        p_id = r_json['data']['productCreate']['product']['id']

        product_id_dict[name] = p_id
    return product_id_dict


def createProductImages(product_id_dict: dict):
    images = [
        ('248747', product_id_dict['Windgeschwind']),
        ('1337824', product_id_dict['Orangensaft']),
        ('616833', product_id_dict['Apfelsaft']),
        ('3596690', product_id_dict['Wein']),
        ('1672304', product_id_dict['Bier']),
        ('61127', product_id_dict['Banane']),
        ('568471', product_id_dict['Birne']),
        ('128420', product_id_dict['Gurke']),
        ('5617', product_id_dict['Tomate']),
        ('1114690', product_id_dict['Blitzbringer']),
        ('4239035', product_id_dict['Super Lappen']),
        ('4239117', product_id_dict['Spüli']),
        ('3958212', product_id_dict['Klopapier']),
        ('298611', product_id_dict['Zahnpasta']),
        ('2111015', product_id_dict['Trash Gera']),
        ('2747446', product_id_dict['Seven Club']),
        ('56733', product_id_dict['Tierpark Gera']),
        ('3876395', product_id_dict['Sky Motion Team']),
    ]

    args = []
    for image_req in images:
        image_id, product_id = image_req
        r = requests.get(
            'http://www.pexels.com/photo/{0}/download/'.format(image_id))

        _, params = cgi.parse_header(r.headers['Content-Disposition'])
        open(params['filename'], 'wb').write(r.content)

        query = get_query_product_img_upload(product_id, params['filename'])
        print(query)
        args.append((query, params['filename']))

    tasks = itertools.starmap(
        execute_querry_upload_file, args)
    asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))


if __name__ == '__main__':
    category_dict = create_categories()
    p_type_dict = create_p_types()

    p_id_dict = create_products(category_dict, p_type_dict)

    createProductImages(p_id_dict)
    pass
