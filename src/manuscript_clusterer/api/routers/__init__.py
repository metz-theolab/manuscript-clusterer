"""Initializes the database for use across the different endpoints.
"""

from manuscript_clusterer.api.database.db_manipulator import ManuscriptDB
from manuscript_clusterer.api.models.settings import Settings

STUDIED_CHAPTER = "10"
# A bit too hardcoded but will eventually be configurable


settings = Settings()

db_manipulator = ManuscriptDB(host=settings.db_host,
                              port=settings.db_port,
                              db_name=settings.db_name)