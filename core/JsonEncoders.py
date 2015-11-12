import json
import bson


class JsonEncoders(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bson.objectid.ObjectId):
            return str(obj)

        return json.JSONEncoder.default(self, obj)
