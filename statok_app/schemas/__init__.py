from datetime import datetime
from statok_app.models.category import CategoryType

OPERATION_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
OPERATION_MAX_VALUE = 999999999.9999           # Corresponds to NUMERIC(13,4) operation database model

# JSON encoders for schemas
json_encoders = {
    datetime: lambda v: v.strftime(OPERATION_DATE_FORMAT),
    CategoryType: lambda v: v.name
}
