import base64
import collections
import json
from flask import Response


######## General Constants #########
DATA_MODEL_PATH   = "model/Regression.pkl"  # File path for the model used by the semantic labeling
INDEX_NAME        = "index_name"            # The index_name for use when saving attributes
NOT_ALLOWED_CHARS = '[\\/*?"<>|\s\t]'       # Characters not allowed by elastic search
ID_DIVIDER        = "-"                     # The divider that is used to separate the different parts of ID's, like class and property
CONFIDENCE        = 0.2                     # Semantic types which have a confidence of lower than this number on predict will not be returned

######## Mongodb Names ########
ID                      = "_id"          # ID for any entry in the db
DATA_TYPE               = "dataType"     # Name for the type of data the entry in the db is, should be used with one of the constants here like DATA_TYPE_SEMANTIC_TYPE
DATA_TYPE_SEMANTIC_TYPE = "type"         # Name for the Semantic Type, should be used with DATA_TYPE
DATA_TYPE_COLUMN        = "column"       # Name for the Semantic Type's column, should be used with DATA_TYPE
DATA_TYPE_MODEL         = "model"        # Name for the karma model that is uploaded, should be used with DATA_TYPE
TYPEID                  = "typeId"       # A column's semantic type's id
DATA                    = "data"         # Name for a column's data in the db
NAME                    = "name"         # A column's name
SOURCE                  = "source"       # A column's source
DESC                    = "description"  # Bulk add model description
BULK_ADD_MODEL_DATA     = "bulkAddData"  # The full model that was given to the POST /bulk_add_models

######## Path Parameters ########
COLUMN_ID = "column_id"
TYPE_ID   = "type_id"

######## Query Parameters ########
CLASS              = "class"
PROPERTY           = "property"
NAMESPACE          = "namespace"
NAMESPACES         = "namespaces"
COLUMN_NAME        = "columnName"
COLUMN_NAMES       = "columnNames"
SOURCE_NAME        = "sourceName"
SOURCE_NAMES       = "sourceNames"
COLUMN_IDS         = "columnIds"
MODEL              = "model"
MODELS             = "models"
COLUMNS            = "columns"
DELETE_ALL         = "deleteAll"
RETURN_COLUMNS     = "returnColumns"
RETURN_COLUMN_DATA = "returnColumnData"
#### Query parameters and return values for bulk add ####
SHOW_ALL    = "showAllData"
MODEL_NAMES = "modelNames"
MODEL_DESC  = "modelDesc"
MODEL_IDS   = "modelIds"
MODEL_ID    = "modelId"

######## Other return names ########
SCORE = "score"


def json_response(json_body, code):
    return Response(response=str(json.dumps(json_body, ensure_ascii=False, indent=4)), status=code, mimetype="application/json")


def get_type_id(class_, property_):
    return base64.b64encode(class_) + ID_DIVIDER + base64.b64encode(property_)


def get_column_id(type_id, column_name, source_name, model):
    return type_id + ID_DIVIDER + base64.b64encode(column_name) + ID_DIVIDER + base64.b64encode(source_name) + ID_DIVIDER + base64.b64encode(model)


def clean_column_output(column, show_data=True):
    o = collections.OrderedDict()
    o[COLUMN_ID] = column[ID]
    o[NAME] = column[COLUMN_NAME]
    o[SOURCE] = column[SOURCE_NAME]
    o[MODEL] = column[MODEL]
    if show_data:
        o[DATA] = column[DATA]
    return o


def clean_columns_output(column_input, show_data):
    return map(lambda t: clean_column_output(t, show_data), column_input)


def get_column_create_db_body(column_id, type_id, column_name, source_name, model):
    return {ID: column_id, DATA_TYPE: DATA_TYPE_COLUMN, TYPEID: type_id, COLUMN_NAME: column_name, SOURCE_NAME: source_name, MODEL: model}


def get_type_from_column_id(type_id):
    split_type_id = type_id.split(ID_DIVIDER)
    return split_type_id[0] + ID_DIVIDER + split_type_id[1]