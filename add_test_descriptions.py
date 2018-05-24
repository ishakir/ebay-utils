from utils.ebay import get_connection, get_all_item_ids, get_item_description, update_item_description

descriptions = {
	'110307363006': 'examples/with_header.html',
	'110307453419': 'examples/without_header.html'
}

api = get_connection('test')

for item_id, desc_file in descriptions.iteritems():
	with open(desc_file, 'r') as f:
		desc = f.read().decode('utf-8')
	update_item_description(api, item_id, desc)
