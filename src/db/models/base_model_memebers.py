"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

class BaseModelMembers():
    """Class to add common members for models"""

    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        
        return d



