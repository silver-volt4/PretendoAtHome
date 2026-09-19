from pymongo import MongoClient
from ansible.module_utils.basic import AnsibleModule

module_args = {
    "mongo_connection_string": {
        "type": "str",
        "required": True,
    },
    "service_name": {
        "type": "str",
        "required": True,
    },
    "game_server_id": {
        "type": "str",
        "required": True,
    },
    "title_ids": {
        "type": "list",
        "required": True,
        "options": {"sub_param": {"type": "str"}},
    },
    "ip": {
        "type": "str",
        "required": True,
    },
    "port": {
        "type": "int",
        "required": True,
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


def copy_and_diff(obj: dict, key: str, new_value: any):
    pass


def run_module():
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    mongo_connection_string = module.params["mongo_connection_string"]
    service_name = module.params["service_name"]
    game_server_id = module.params["game_server_id"]
    title_ids = module.params["title_ids"]
    ip = module.params["ip"]
    port = module.params["port"]
    device = module.params["device"]
    aes_key = module.params["aes_key"]
    access_levels = module.params["access_levels"]
    state = module.params["state"]

    mongo = MongoClient(mongo_connection_string)
    db = mongo.get_default_database()
    servers = db.get_collection("servers")

    # Assuming unique service names
    # TODO: maybe use some kind of unique ID in the future?

    for level in access_levels:
        old = servers.find_one(
            {
                "service_name": service_name,
                "access_mode": level,
            }
        )

        if state == "absent":
            if old:
                servers.delete_one({"_id": old._id})
            continue

        if not old:
            new = {}
        else:
            new = old.copy()
            del new["_id"]

        new["service_name"] = service_name
        new["game_server_id"] = game_server_id
        new["title_ids"] = title_ids
        new["ip"] = ip
        new["port"] = port
        new["device"] = device
        new["aes_key"] = aes_key
        new["access_mode"] = level

        if not old:
            servers.insert_one(new)
        else:
            servers.update_one({"_id": old._id}, {"$set": new})

    result = dict(changed=True, original_message="", message="")

    module.exit_json(**result)


if __name__ == "__main__":
    run_module()
