
"""
This cli script creates a folder structure based on the defined NoSQL export
"""

import json
import argparse

from pathlib import Path


# Templates

entity_template = """
from dynamodbEntities import Entity

class {entity_name}(Entity):

    def __init__(self, {init_params}, **kwargs):
        super().__init__({init_params_assignment}, **kwargs)
    
    @property
    def {pk}(self):
        # TODO: Implement the partition key
        return ""
    
    @property
    def {sk}(self):
        # TODO: Implement the sort key
        return ""

"""

init_template = """
{imports}

__all__ = {all_statement}
"""

factory_template = """
\"\"\"
This factory file is used to create a customized Entity class.
Import this new Entity.
\"\"\"


from dynamodbEntities.entity import get_entity_class

Entity = get_entity_class(
    # name of the partition key
    __pk_name="{pk}",
    # type of the partition key in the DynamoDB format, use "S" for string, "N" for number
    __pk_type="{pk_type}",
    # name of the sort key
    __sk_name="{sk}",
    # type of the sort key in the DynamoDB format, use "S" for string, "N" for number
    __sk_type="{sk_type}",
     # name of the entity property,
    __et_name = "_et",
)


# Use the code below to further overwrite the Entity class
'''
class Entity(Entity):

    __reserved_names = ["modified_date", "entity"]

    @property
    def modified_date(self):
        \"\"\"
        a custom last modified date
        \"\"\"
        # Implement a custom last modified date here, or return the default
        return self.__md

    @property
    def entity(self):
        \"\"\"
        a custom entity property
        \"\"\"
        return self.__et
 
'''
"""

tablespec_template = """
DATASTORE_DESCRIPTION = {json_data}

"""

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", help="path to input")
parser.add_argument("--dest", "-d", help="path to output")
args = parser.parse_args()

outdir = Path(args.dest, "entities")
# outdir = Path("./example/testrun/entities")
outdir.mkdir(exist_ok=True, parents=True)

importFile = args.input
# importFile = "/home/paszin/Documents/personal/dynamodb-entities/example/webshob/Webshop.json"

with open(importFile) as f:
    data = json.load(f)


partitionKey = data["DataModel"][0]["KeyAttributes"]["PartitionKey"]["AttributeName"]
partitionKeyType = data["DataModel"][0]["KeyAttributes"]["PartitionKey"]["AttributeType"]
try:
    sortKey = data["DataModel"][0]["KeyAttributes"]["SortKey"]["AttributeName"]
    sortKeyType = data["DataModel"][0]["KeyAttributes"]["SortKey"]["AttributeType"]
except:
    sortKey = None
    sortKeyType = None
facets = data["DataModel"][0]["TableFacets"]


facet_names = []

for facet in facets:
    facet_name = facet["FacetName"]
    facet_pk = facet["KeyAttributeAlias"]["PartitionKeyAlias"]
    facet_sk = facet["KeyAttributeAlias"].get("SortKeyAlias")
    facet_properties = facet["NonKeyAttributes"]
    facet_names.append(facet_name)

    filecontent = entity_template.format(
        pk=facet_pk,
        sk=facet_sk,
        entity_name=facet_name,
        init_params=", ".join(facet_properties),
        init_params_assignment=", ".join(
            [f"{p}={p}" for p in facet_properties])
    )

    filename = f"{facet_name}.py"

    with open(outdir / filename, "w") as f:
        f.write(filecontent)


init_file = init_template.format(
    imports="\n".join([f"from .{name} import {name}" for name in facet_names]),
    all_statement=str(facet_names)
)

with open(outdir / "__init__.py", "w") as f:
    f.write(init_file)




factory_file = factory_template.format(
    pk=partitionKey,
    pk_type=partitionKeyType,
    sk=sortKey,
    sk_type=sortKeyType
)

with open(outdir / "_factory.py", "w") as f:
    f.write(factory_file)


tablespec_data = {
    "AttributeDefinitions": [
        {"AttributeName": partitionKey, "AttributeType": partitionKeyType},
        # {"AttributeName": "sk", "AttributeType": "S"},
        # {"AttributeName": "gsi_1", "AttributeType": "S"},
    ],
    "BillingMode": "PAY_PER_REQUEST",
    "KeySchema": [
        {"AttributeName": partitionKey, "KeyType": "HASH"},
        # {"AttributeName": "sk", "KeyType": "RANGE"},
    ],
    "GlobalSecondaryIndexes": [],
}

if sortKey:
    tablespec_data["AttributeDefinitions"].append(
        {"AttributeName": sortKey, "AttributeType": sortKeyType}
    )
    tablespec_data["KeySchema"].append(
        {"AttributeName": sortKey, "KeyType": "RANGE"}
    )

for gsi in data["DataModel"][0]["GlobalSecondaryIndexes"]:

    tablespec_data["GlobalSecondaryIndexes"].append(
        {
            "IndexName": gsi["IndexName"],
            "KeySchema": [
                {"AttributeName": gsi["KeyAttributes"]["PartitionKey"]
                    ["AttributeName"], "KeyType": "HASH"},
                # TODO: extend for sort key
                # {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "ALL"},
        }
    )


tablespec_file = tablespec_template.format(
    json_data=json.dumps(tablespec_data, indent=4)
)

with open(outdir / ".." / "tablespec.py", "w") as f:
    f.write(tablespec_file)
