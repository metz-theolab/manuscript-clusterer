"""Model representing a manuscript.
"""
from typing import Optional
from pydantic import BaseModel



class Manuscript(BaseModel):
    """Model representing a manuscript.
    """
    id: int
    name: str
    type: str
    location: Optional[str]
    text_type: Optional[str]
    von_soden_group: Optional[str]
    wisse_group: Optional[str]
    auto: Optional[str]


class ManuscriptContent(BaseModel):
    """Model representing the text of a manuscript.
    """
    id: int
    name: str
    content: dict[str, dict[str, str]]
    

class ManuscriptsProjection(BaseModel):
    """
    Model representing a projection of manuscripts.
    """