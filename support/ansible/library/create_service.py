from pymongo import MongoClient

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.mongo_document import accumulate_result_dicts, ensure

module_args = {
    "mongo_connection_string": {
        "type": "str",
        "required": True,
    },
    "service_name": {
        "type": "str",
        "required": True,
    },
    "client_id": {
        "type": "str",
        "required": True,
    },
    "title_ids": {
        "type": "list",
        "required": True,
        "options": {"sub_param": {"type": "str"}},
    },
    "device": {
        "type": "int",
        "required": True,
    },
    "aes_key": {
        "type": "str",
        "required": True,
    },
    "access_levels": {
        "type": "list",
        "required": True,
        "options": {"sub_param": {"type": "str"}},
    },
    "state": {
        "type": "str",
        "default": "present",
        "choices": ["present", "absent"],
    },
}


def run_module():
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    mongo_connection_string = module.params["mongo_connection_string"]
    service_name = module.params["service_name"]
    client_id = module.params["client_id"]
    title_ids = module.params["title_ids"]
    device = module.params["device"]
    aes_key = module.params["aes_key"]
    access_levels = module.params["access_levels"]
    state = module.params["state"]

    mongo = MongoClient(mongo_connection_string)
    db = mongo.get_default_database()
    servers = db.get_collection("servers")

    # Assuming unique service names
    # TODO: maybe use some kind of unique ID in the future? Idk if _id can be specified by the user

    result = {}

    for level in access_levels:
        document = {
            "service_name": service_name,
            "service_type": "service",
            "client_id": client_id,
            "title_ids": title_ids,
            "device": device,
            "aes_key": aes_key,
            "access_mode": level,
        }

        ensure_result = ensure(
            servers, document, ["access_mode", "service_name"], state
        )
        accumulate_result_dicts(result, ensure_result)

    module.exit_json(**result)


if __name__ == "__main__":
    run_module()
