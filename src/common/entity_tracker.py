"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

import src.common.data_field as DataField

class EntityTracker():
    """Class to manage an entity tracker, an entity is an abstraction of
    Subjects that can generate data like Profiles, Groups (FB and tiktok), Lists (X), etc.
    """

    entity_type: str
    created_at: DataField
    country_creation: str
    owner: str # change this to Account
    data_fields: []
    

    def __init__(self, entity_type: str, created_at: DataField, country_creation: str,
                 owner: str, data_fields: []) -> dict:
        valid_entities = [
            'fb_profile',
            'fb_group',
            'x_profile',
            'x_list',
            'tiktok_profile',
            'tiktok_group'
        ]

        valid_platforms = [
            'facebook',
            'tiktok'
            'x'
        ]

        if entity_type not in valid_entities:
            raise Exception(f'{entity_type} not an allowed entity.')

        self.entity_type = entity_type
        self.created_at = created_at
        self.country_creation = country_creation
        self.owner = owner
        self.data_fields = data_fields

        return vars(self)
    

    def get_data_fields(self):
        pass


    def sate_tocsv(filename: str):
        pass
