import json

import detection_pb2


def read_database():
    """Reads the route guide database.

  Returns:
    The full contents of the route guide database as a sequence of
      route_guide_pb2.Features.
  """
    block_list = []
    with open("blocklist_db.json") as db_file:
        for item in json.load(db_file):
            block_list.append(item["ip"])
    return block_list
