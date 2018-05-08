from argparse import ArgumentParser
import datetime
import sys
from time import sleep

from utils import prompt_warning
from utils.ebay import get_connection, get_all_item_ids, get_item_description, update_item_description
from utils.description import fix_description


def run(domain, max_items, accepted_item_ids, sleep_time):
    if domain != 'test':
        prompt_warning("Domain '{}' is not a testing environment".format(domain))
    if max_items is None:
        if not accepted_item_ids:
            prompt_warning('This process will update every single listing')
        if len(accepted_item_ids) > 5:
            prompt_warning('This process will update {} listing(s)'.format(len(accepted_item_ids)))
    if max_items > 5:
        if not accepted_item_ids:
            prompt_warning('This process will update {} listing(s)'.format(max_items))
        else:
            prompt_warning('This process will update {} listing(s)'.format(min([max_items, len(accepted_item_ids)])))

    api = get_connection('test')
    item_ids = get_all_item_ids(api)

    if accepted_item_ids:
        filtered_items = [item_id for item_id in item_ids if item_id in accepted_item_ids]
    else:
        filtered_items = item_ids

    if max_items:
        filtered_items = filtered_items[:max_items]

    for item_id in filtered_items:
        description = get_item_description(api, item_id)
        update_item_description(api, item_id, fix_description(description))
        sleep(sleep_time)

# TODO: Pass sleep time in (ask again if sleep time is too high)
if __name__ == '__main__':
    parser = ArgumentParser(description='Update EBay item descriptions')
    parser.add_argument('--domain', required=True)
    parser.add_argument('--sleep-time', type=int, required=True)
    parser.add_argument('--item-ids', nargs="*")
    parser.add_argument('--max-items', type=int)
    args = parser.parse_args()

    run(args.domain, args.max_items, args.item_ids)

    
