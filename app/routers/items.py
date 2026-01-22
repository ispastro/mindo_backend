from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from datetime import datetime
from ..database import get_session
from ..models.models import Item, User
from ..schemas.item import ItemCreate, ItemResponse, ItemUpdate
from ..dependencies.auth import get_current_user
from ..utils.ai import extract_search_terms


router = APIRouter(prefix="/api/items", tags=["Items"])

@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item_data: ItemCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new item for the current user"""
    new_item = Item(
        name=item_data.name,
        location=item_data.location,
        user_id=current_user.id
    )
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item

@router.get("", response_model=dict)
def list_items(
    page: int = 1,
    page_size: int = 10,
    query: str | None = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all items for the current user with pagination and search"""
    # Validate pagination parameters
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")
    if page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Page size must be between 1 and 100")
    
    # Base query
    statement = select(Item).where(Item.user_id == current_user.id)
    
    # Add search filter if query provided
    if query:
        search_pattern = f"%{query}%"
        statement = statement.where(
            (Item.name.ilike(search_pattern)) | (Item.location.ilike(search_pattern))
        )
    
    # Get total count
    total_items = len(session.exec(statement).all())
    
    # Apply pagination
    offset = (page - 1) * page_size
    statement = statement.offset(offset).limit(page_size)
    
    items = session.exec(statement).all()
    
    # Calculate pagination metadata
    total_pages = (total_items + page_size - 1) // page_size
    
    return {
        "data": [ItemResponse.model_validate(item) for item in items],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next_page": page < total_pages,
            "has_previous_page": page > 1
        }
    }


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a single item by ID"""
    item = session.get(Item, UUID(item_id))
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    if item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this item"
        )
    
    return item

@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: str,
    item_data: ItemUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update an item"""
    item = session.get(Item, UUID(item_id))
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    if item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this item"
        )
    
    if item_data.name is not None:
        item.name = item_data.name
    if item_data.location is not None:
        item.location = item_data.location
    
    item.updated_at = datetime.utcnow()
    session.add(item)
    session.commit()
    session.refresh(item)
    
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete an item"""
    item = session.get(Item, UUID(item_id))
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    if item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this item"
        )
    
    session.delete(item)
    session.commit()
    
    return None

@router.get("/search/ai", response_model=dict)
def ai_search_items(
    query: str,
    page: int = 1,
    page_size: int = 10,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """AI-powered natural language search for items"""
    print(f"\n🔍 AI SEARCH REQUEST:")
    print(f"   Query: '{query}'")
    print(f"   User: {current_user.email}")
    print(f"   Page: {page}, Size: {page_size}")
    
    # Validate pagination
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")
    if page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="Page size must be between 1 and 100")
    
    # Extract search terms using AI
    search_terms = extract_search_terms(query)
    print(f"   Extracted terms: '{search_terms}'")
    
    # Base query
    statement = select(Item).where(Item.user_id == current_user.id)
    
    # Add search filter
    if search_terms:
        search_pattern = f"%{search_terms}%"
        statement = statement.where(
            (Item.name.ilike(search_pattern)) | (Item.location.ilike(search_pattern))
        )
    
    # Get total count
    total_items = len(session.exec(statement).all())
    
    # Apply pagination
    offset = (page - 1) * page_size
    statement = statement.offset(offset).limit(page_size)
    
    items = session.exec(statement).all()
    
    # Calculate pagination metadata
    total_pages = (total_items + page_size - 1) // page_size
    
    return {
        "data": [ItemResponse.model_validate(item) for item in items],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next_page": page < total_pages,
            "has_previous_page": page > 1
        },
        "ai_metadata": {
            "original_query": query,
            "extracted_terms": search_terms
        }
    }
