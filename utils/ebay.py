from ebaysdk.trading import Connection

ENTRIES_PER_PAGE = 100

def get_connection(instance):
    print "Constructing eBay API instance for '{}'".format(instance)
    if instance == 'test':
        return Connection(domain='api.sandbox.ebay.com')
    else:
        raise ValueError("Don't recognise instance '{}'".format(instance))
        

# Get items dealing with pagination
def get_all_item_ids(api):
    item_ids = []

    first_response = api.execute('GetSellerList', {
        'StartTimeFrom': '2018-05-01T07:12:09.000Z',
        'StartTimeTo': '2018-07-01T07:12:09.000Z',
        'Pagination': {
            'EntriesPerPage': ENTRIES_PER_PAGE
        }
    }).dict()

    total_pages = int(first_response['PaginationResult']['TotalNumberOfPages'])

    for page_number in range(1, total_pages + 1):
        print "Getting page number {}/{}".format(page_number, total_pages)
        page_response = first_response = api.execute('GetSellerList', {
            'StartTimeFrom': '2018-05-01T07:12:09.000Z',
            'StartTimeTo': '2018-07-01T07:12:09.000Z',
            'Pagination': {
                'EntriesPerPage': ENTRIES_PER_PAGE,
                'PageNumber': page_number
            }
        }).dict()

        items = page_response['ItemArray']['Item']
        if isinstance(items, dict):
            item_ids.append(items['ItemID'])
        elif isinstance(items, list):
            for item_desc in items:
                item_ids.append(item_desc['ItemID'])
        else:
            raise ValueError("Wasn't sure how to interpret {}".format(str(items)))

    print "Fetched all item_ids"
    return item_ids

def get_item_description(api, item_id):
    print "Fetching description for ItemId={}".format(item_id)

    get_response = api.execute('GetItem', {
        'ItemID': item_id,
        'DetailLevel': 'ItemReturnDescription'
    }).dict()

    return get_response['Item']['Description']

def update_item_description(api, item_id, description):
    print "Updating description for ItemID={}".format(item_id)

    update_response = api.execute('ReviseItem', {
        'Item': {
            'ItemID': item_id,
            'Description': "<![CDATA[{}]]>".format(description.encode('utf-8'))
        }    
    })


def create_item(api):
    response = api.execute('AddItem', {
        'Item': {
            'PrimaryCategory': {
                'CategoryID': 184440
            },
            'StartPrice': '200',
            'Currency': 'USD',
            'Country': 'HK',
            'ListingType': 'FixedPriceItem',
            'ListingDuration': 'GTC',
            'Location': 'HK',
            'Description': 'Hello, my item 22342349',
            'Title': 'Item 178',
            'DispatchTimeMax': 1,
            'ShippingDetails': {
                'ShippingType': 'Flat',
                'ShippingServiceOptions': {
                    'ShippingServicePriority': 1,
                    'ShippingService': 'USPSMedia',
                    'ShippingServiceCost': '2.50'
                }
            },
            'PaymentMethods': 'PayPal',
            'PayPalEmailAddress': 'fake.email@gmail.com',
            'ReturnPolicy': {
                'ReturnsAcceptedOption': 'ReturnsNotAccepted'
            }
        }
    })

    pprint(response.dict())
