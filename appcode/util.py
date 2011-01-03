#Function takes a list of dictionaries then creates a new dictionary with the
#key being one of the fields identified in each dictionary row.
#eg: converts:
#[{u'name': u'entity_name', u'value': u'sadsadsa'}, {u'name': u'entity_desc', u'value': u'asdsaddasdsadsad'}, {u'name': u'entity_tags', u'value': u'sdsadsadad'}, {u'name': u'entity_is_default', u'value': u'on'}]
# to
#
from google.appengine.api import users

def convert_list_to_dict(old_dict, key_field):
    new_dict = {}
    for dictRow in old_dict:
        new_key = dictRow[key_field]
        new_dict[dictRow[key_field]] = dictRow
    return new_dict

