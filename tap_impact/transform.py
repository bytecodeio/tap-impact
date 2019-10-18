import re
import singer

LOGGER = singer.get_logger()

# Convert camelCase to snake_case
def convert(name):
    regsub = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', regsub).lower()


# Convert keys in json array
def convert_array(arr):
    new_arr = []
    for i in arr:
        if isinstance(i, list):
            new_arr.append(convert_array(i))
        elif isinstance(i, dict):
            new_arr.append(convert_json(i))
        else:
            new_arr.append(i)
    return new_arr


# Convert keys in json
def convert_json(this_json):
    out = {}
    for key in this_json:
        new_key = convert(key)
        if isinstance(this_json[key], dict):
            out[new_key] = convert_json(this_json[key])
        elif isinstance(this_json[key], list):
            out[new_key] = convert_array(this_json[key])
        else:
            out[new_key] = this_json[key]
    return out


# Replace system/reserved field 'oid' with 'order_id'
def replace_order_id(this_json, data_key):
    i = 0
    for record in this_json[data_key]:
        order_id = record.get('oid')
        this_json[data_key][i]['order_id'] = order_id
        this_json[data_key][i].pop('oid', None)
        i = i + 1
    return this_json


# Run all transforms: convert camelCase to snake_case for fieldname keys
def transform_json(this_json, stream_name, data_key):
    converted_json = convert_json(this_json)
    converted_data_key = convert(data_key)
    if stream_name in ('actions', 'action_updates'):
        transformed_json = replace_order_id(converted_json, converted_data_key)[converted_data_key]
    else:
        transformed_json = converted_json[converted_data_key]
    return transformed_json
