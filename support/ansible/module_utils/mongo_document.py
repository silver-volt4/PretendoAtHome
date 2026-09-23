from typing import Any
from pymongo.collection import Collection


def ensure(
    collection: Collection,
    document: dict[str, Any],
    discriminator: str | list[str],
    state: str,
):
    if discriminator is str:
        discriminator = [discriminator]

    discriminator_dict = {k: v for k, v in document.items() if k in discriminator}
    existing = collection.find_one(discriminator_dict)

    if state == "absent":
        if existing:
            collection.delete_one({"_id": existing["_id"]})
            return dict(
                changed=True,
                message="Deleted Mongo document " + str(discriminator_dict),
            )
        return dict(ok=True)

    if not existing:
        collection.insert_one(document)
        return dict(
            changed=True, message="Created Mongo document " + str(discriminator_dict)
        )
    else:
        collection.update_one({"_id": existing["_id"]}, {"$set": document})
        new = collection.find_one(discriminator_dict)
        if new != existing:
            return dict(
                changed=True,
                message="Updated Mongo document " + str(discriminator_dict),
            )
        else:
            return dict(ok=True)


def accumulate_result_dicts(collector, new):
    if new.get("changed"):
        if collector.get("ok"):
            del collector["ok"]
        collector["changed"] = True
    elif new.get("ok"):
        collector["ok"] = True

    added_message = new.get("message")
    if added_message:
        added_message += "\n"
    else:
        added_message = ""

    collector["message"] = collector.get("message", "") + added_message
