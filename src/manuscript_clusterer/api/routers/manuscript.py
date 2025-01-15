"""Router for the API endpoints to get manuscript related data.
"""
from fastapi import APIRouter, HTTPException
from manuscript_clusterer.api.routers import db_manipulator
from . import STUDIED_CHAPTER

router = APIRouter(prefix="/manuscript", tags=["manuscript"])


@router.get("/")
async def get_manuscripts():
    """Get all manuscripts from the database.
    """
    manuscripts = db_manipulator.get_manuscripts()
    if not manuscripts:
        raise HTTPException(status_code=404, detail="No manuscripts found")
    return manuscripts


@router.get("/{manuscript_id}")
async def get_manuscript(manuscript_id: str):
    """Get a manuscript from the database.
    """
    manuscript = db_manipulator.get_manuscript(manuscript_id=manuscript_id)
    if not manuscript:
        raise HTTPException(status_code=404, detail="Manuscript not found")
    return manuscript


@router.get("/{manuscript_id}/content")
async def get_manuscript_content(manuscript_id: str):
    """Get the content of a manuscript from the database.
    """
    manuscript_content = db_manipulator.get_manuscript_content(
        manuscript_id=manuscript_id)
    if not manuscript_content:
        raise HTTPException(
            status_code=404, detail="Manuscript content not found")
    return manuscript_content

@router.get("/{manuscript_id}/content/{chapter}/{verse}")
async def get_manuscript_verse(manuscript_id: str, verse: str, chapter: str = STUDIED_CHAPTER):
    """Get the content of a verse of a manuscript from the database.
    """
    manuscript_content = db_manipulator.get_manuscript_content(
        manuscript_id=manuscript_id)
    if not manuscript_content:
        raise HTTPException(
            status_code=404, detail="Manuscript content not found")
    return manuscript_content["content"][chapter][verse]


@router.get("/{manuscript_id}/profile")
async def get_manuscript_profile(manuscript_id: str):
    """Get the profile of a manuscript from the database.
    """
    manuscript_profile = db_manipulator.get_manuscript_profile(
        manuscript_id=manuscript_id)
    if not manuscript_profile:
        raise HTTPException(
            status_code=404, detail="Manuscript profile not found")
    return manuscript_profile


@router.get("/{manuscript_id}/info")
async def get_manuscript_info(manuscript_id: str):
    """Get the profile and content of a manuscript from the database.
    """
    manuscript_info = db_manipulator.get_manuscript_info(
        manuscript_id=manuscript_id)
    if not manuscript_info:
        raise HTTPException(
            status_code=404, detail="Manuscript info not found")
    return manuscript_info


@router.get("/{manuscript_id}/verses")
async def get_manuscript_verses(manuscript_id: str,
                                chapter: str = STUDIED_CHAPTER):
    """Get the list of available verses of a manuscript from the database.
    """
    manuscript_verses = db_manipulator.get_manuscript_content(
        manuscript_id=manuscript_id)["content"][chapter]
    if not manuscript_verses:
        raise HTTPException(
            status_code=404, detail="Manuscript verses not found")
    return list(manuscript_verses.keys())