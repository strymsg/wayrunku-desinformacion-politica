"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

import datetime


class DataField():
    """Class to manage data fields with some utilities"""

    field_type: str
    field_type_name: str
    name: str
    bd_field: str
    nullable: bool


    def __init_(self, name: str, field_type: str, bd_field: str, nullable: bool) -> dict:
        possible_fields = [
            'str', 
            'int',
            'float',
            'date',
            'datetime',
            'bool',
        ]

        if field_type not in possible_fields:
            raise Exception(f'{field_type} not allowed type.')

        self.name = name
        self.field_type_name = field_type
        if field_type == 'date':
            self.field_type = datetime.date
        elif field_type == 'datetime':
            self.field_type = datetime.datetime
        else:
            self.field_type = field_type
        
        self.bd_field = bd_field
        self.nullable = nullable

        return vars(self)
    
    
