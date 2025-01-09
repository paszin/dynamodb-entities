
DATASTORE_DESCRIPTION = {
    "AttributeDefinitions": [
        {
            "AttributeName": "pk",
            "AttributeType": "S"
        },
        {
            "AttributeName": "sk",
            "AttributeType": "S"
        }
    ],
    "BillingMode": "PAY_PER_REQUEST",
    "KeySchema": [
        {
            "AttributeName": "pk",
            "KeyType": "HASH"
        },
        {
            "AttributeName": "sk",
            "KeyType": "RANGE"
        }
    ],
    "GlobalSecondaryIndexes": [
        {
            "IndexName": "gsi_1",
            "KeySchema": [
                {
                    "AttributeName": "gsi_1",
                    "KeyType": "HASH"
                }
            ],
            "Projection": {
                "ProjectionType": "ALL"
            }
        }
    ]
}

