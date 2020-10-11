import requests
import os
import random
import os
from aiogqlc import GraphQLClient
from urllib.request import urlretrieve
import asyncio
import itertools
import cgi
import io
import tempfile
import logging


logging.basicConfig(
    format='[%(filename)s][%(levelname)s]: %(message)s', level=logging.INFO)

GRAPHQL_URL = 'http://localhost:8000/graphql/'
GRAPHQL_BEAR_TOKEN = os.environ.get('GRAPHQL_BEAR_TOKEN')


async def execute_querry_upload_file(query: str, pexels_id):
    logging.info('Download {0} from pexels'.format(pexels_id))
    r = requests.get(
        'http://www.pexels.com/photo/{0}/download/'.format(pexels_id))
    _, params = cgi.parse_header(r.headers['Content-Disposition'])
    # tempfile and BytesIO dos not work for some reason
    file = open(params['filename'], 'wb+')
    file.write(r.content)
    file.seek(0)  # set read head to statr

    variables = {
        'file': file,
    }
    headers = {"Authorization": "Bearer {0}".format(GRAPHQL_BEAR_TOKEN)}

    client = GraphQLClient(GRAPHQL_URL, headers=headers)
    logging.info('Upload Image {0} to saleor'.format(params['filename']))
    r = await client.execute(query, variables=variables)
    # print(await r.json())

    file.close()
    logging.info('Delete {0} from drive'.format(params['filename']))
    os.remove(params['filename'])


def execute_querry(query: str):
    # discovered GraphQLClient to late -> not time to rewrite code

    headers = {"Authorization": "Bearer {0}".format(GRAPHQL_BEAR_TOKEN)}

    r = requests.post(GRAPHQL_URL, json={'query': query}, headers=headers)
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


def get_query_update_category_picture(id: str):
    query = """mutation updateCategoryPicture($file: Upload!) {
                categoryUpdate (id: "%s", input: { backgroundImage: $file}){
                    productErrors{
                        message
                        field
                    }
                    category{
                        id
                    }
                }
        }""" % (id)

    return query


def get_query_create_example_product(name: str, product_type_id: str, category_id: str, warehouse_id: str):
    lorem_ipsum = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. "
    json_data = '{\\"blocks\\": [{\\"key\\": \\"\\", \\"data\\": {}, \\"text\\": \\"%s\\", \\"type\\": \\"unstyled\\", \\"depth\\": 0, \\"entityRanges\\": [], \\"inlineStyleRanges\\": []}], \\"entityMap\\": {}}' % (
        lorem_ipsum)

    query = """mutation exampleProduct {
            productCreate (input: {name:"%s", productType:"%s", category:"%s", basePrice:"%.2f", description:"%s", descriptionJson:"%s", isPublished:true, stocks:{ warehouse: "%s" , quantity:10 }}){
                product {
                name
                id
                }
            }
        }""" % (name, product_type_id, category_id, random.uniform(0.5, 9.9), lorem_ipsum, json_data, warehouse_id)

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


def get_query_product_img_upload(product_id: str):
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

        logging.info('Product Type {0} with id {1} created'.format(
            type_name, t_id))

        id_dict[type_name] = t_id

    return id_dict


def create_categories():
    categories = [
        ('Verpfelgung', '3025236', ['Säfte', 'Alkoholische Getränke',
                                    'Obst', 'Gemüse', 'Lieferservices']),

        ('Haushalt', '584399', ['Reinigungsutensilien', 'Verbrauchsgüter']),
        ('Freizeit', '6332', ['Veranstaltungen', 'Aktivitäten']),
    ]

    category_id_dict = {}
    upload_args = []

    for category in categories:
        root_category_name, root_img_id, sub_category_name_list = category

        r_json = execute_querry(
            get_query_create_category(root_category_name))

        p_id = r_json['data']['categoryCreate']['category']['id']
        logging.info('Category {0} with id {1} created'.format(
            root_category_name, p_id))

        query = get_query_update_category_picture(p_id)
        upload_args.append((query, root_img_id))

        for sub_category in sub_category_name_list:
            r_json = execute_querry(get_query_create_category(
                sub_category, parrent_id=p_id))
            # print(r_json)
            name = r_json['data']['categoryCreate']['category']['name']
            s_id = r_json['data']['categoryCreate']['category']['id']

            logging.info(
                'Subcategory {0} with id {1} created'.format(name, s_id))

            category_id_dict[name] = s_id

    tasks = itertools.starmap(execute_querry_upload_file, upload_args)
    asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))

    return category_id_dict


def create_products(category_dict: dict, p_type_dict: dict, warehouse_id: str):
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
            name, product_type_id, category_id, warehouse_id))
        print(r_json)

        name = r_json['data']['productCreate']['product']['name']
        p_id = r_json['data']['productCreate']['product']['id']

        logging.info('Product {0} with id {1} created'.format(name, p_id))

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
        query = get_query_product_img_upload(product_id)
        # print(query)
        args.append((query, image_id))

    tasks = itertools.starmap(
        execute_querry_upload_file, args)
    asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))


def create_warehouse():
    query = """mutation warehouse{
        createWarehouse(input: {companyName: "lieblingsladen gmbh", name:"Arcarden", email:"lieblingsladen@gera.de" address: {streetAddress1:"blumenstraße", city:"gera", country:DE, postalCode: "07545"}}){
            warehouse{
                id
            }
            warehouseErrors{
                field
                message
            }
        }
    }"""

    r_json = execute_querry(query)
    print(r_json)

    return r_json['data']['createWarehouse']['warehouse']['id']


if __name__ == '__main__':
    warehouse_id = create_warehouse()

    category_dict = create_categories()
    p_type_dict = create_p_types()

    p_id_dict = create_products(category_dict, p_type_dict, warehouse_id)

    # createProductImages(p_id_dict)
    pass
