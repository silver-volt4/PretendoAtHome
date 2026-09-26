from pymongo import MongoClient

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.mongo_document import accumulate_result_dicts, ensure

module_args = {
    "mongo_connection_string": {
        "type": "str",
        "required": True,
    },
    "status": {
        "type": "int",
        "required": True,
    },
    "host": {
        "type": "str",
        "required": True,
    },
    "api_host": {
        "type": "str",
        "required": True,
    },
    "portal_host": {
        "type": "str",
        "required": True,
    },
    "n3ds_host": {
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
    status = module.params["status"]
    host = module.params["host"]
    api_host = module.params["api_host"]
    portal_host = module.params["portal_host"]
    n3ds_host = module.params["n3ds_host"]
    access_levels = module.params["access_levels"]
    state = module.params["state"]

    mongo = MongoClient(mongo_connection_string)
    db = mongo.get_default_database()
    servers = db.get_collection("endpoints")

    # Assuming unique host address
    # TODO: maybe use some kind of unique ID in the future? Idk if _id can be specified by the user

    result = {}

    for level in access_levels:
        document = {
            "status": status,
            "server_access_level": level,
            "topics": True,
            "guest_access": True,
            "host": host,
            "api_host": api_host,
            "portal_host": portal_host,
            "n3ds_host": n3ds_host,
        }

        ensure_result = ensure(
            servers, document, ["host", "server_access_level"], state
        )
        accumulate_result_dicts(result, ensure_result)

    module.exit_json(**result)


if __name__ == "__main__":
    run_module()
