"""
SYNTX Formats API - CRUD für Format-Definitionen
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime
import json

from .format_loader import (
    load_format, list_formats, get_format_summary,
    get_field_definitions, get_scoring_config, 
    get_parser_config, validate_format, clear_cache,
    FORMATS_DIR
)

router = APIRouter(prefix="/formats", tags=["formats"])

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class FieldValidation(BaseModel):
    min_length: int = 30
    max_length: int = 5000
    required: bool = True

class FieldDefinition(BaseModel):
    name: str
    weight: int
    description: Dict[str, str]  # {"de": "...", "en": "..."}
    keywords: Dict[str, List[str]]  # {"de": [...], "en": [...]}
    headers: Optional[Dict[str, List[str]]] = None
    validation: Optional[FieldValidation] = None

class ScoringConfig(BaseModel):
    presence_weight: int = 20
    similarity_weight: int = 35
    coherence_weight: int = 25
    depth_weight: int = 15
    structure_weight: int = 5
    pass_threshold: int = 60
    excellent_threshold: int = 85

class ParserConfig(BaseModel):
    header_pattern: str = "###"
    field_separator: str = "\n\n"
    case_sensitive: bool = False

class FormatCreate(BaseModel):
    name: str
    version: str = "1.0"
    description: Dict[str, str]
    author: Optional[str] = None
    tags: Optional[List[str]] = []
    languages: List[str] = ["de"]
    primary_language: str = "de"
    wrapper: Optional[str] = None
    scoring: Optional[ScoringConfig] = None
    parser: Optional[ParserConfig] = None
    fields: List[FieldDefinition]

class FormatUpdate(BaseModel):
    version: Optional[str] = None
    description: Optional[Dict[str, str]] = None
    author: Optional[str] = None
    tags: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    primary_language: Optional[str] = None
    wrapper: Optional[str] = None
    scoring: Optional[ScoringConfig] = None
    parser: Optional[ParserConfig] = None
    fields: Optional[List[FieldDefinition]] = None

# ============================================================================
# GET ENDPOINTS
# ============================================================================

@router.get("/")
async def get_all_formats():
    """
    🌊 Liste aller verfügbaren Formate
    """
    formats = list_formats()
    summaries = []
    
    for fmt_name in formats:
        try:
            summary = get_format_summary(fmt_name)
            summaries.append(summary)
        except Exception as e:
            summaries.append({"name": fmt_name, "error": str(e)})
    
    return {
        "status": "FORMATS_LOADED",
        "count": len(formats),
        "formats": summaries
    }

@router.get("/{name}")
async def get_format(name: str, language: str = Query("de")):
    """
    📄 Ein Format vollständig laden
    """
    try:
        fmt = load_format(name)
        field_defs = get_field_definitions(name, language)
        
        return {
            "status": "FORMAT_LOADED",
            "format": fmt,
            "field_definitions": field_defs
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{name}/fields")
async def get_format_fields(name: str, language: str = Query("de")):
    """
    🔧 Nur die Feld-Definitionen eines Formats (für Scorer)
    """
    try:
        field_defs = get_field_definitions(name, language)
        scoring = get_scoring_config(name)
        parser = get_parser_config(name)
        
        return {
            "status": "FIELDS_LOADED",
            "format": name,
            "language": language,
            "fields": field_defs,
            "scoring": scoring,
            "parser": parser
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{name}/summary")
async def get_format_summary_endpoint(name: str):
    """
    📊 Kurze Zusammenfassung eines Formats
    """
    try:
        summary = get_format_summary(name)
        return {
            "status": "SUMMARY_LOADED",
            "summary": summary
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ============================================================================
# POST ENDPOINT - CREATE
# ============================================================================

@router.post("/")
async def create_format(format_data: FormatCreate):
    """
    🌟 Neues Format erstellen
    """
    # Check ob existiert
    path = FORMATS_DIR / f"{format_data.name}.json"
    if path.exists():
        raise HTTPException(
            status_code=409, 
            detail=f"Format '{format_data.name}' existiert bereits! Nutze PUT zum Updaten."
        )
    
    # Build JSON
    now = datetime.now().strftime("%Y-%m-%d")
    fmt_dict = {
        "name": format_data.name,
        "version": format_data.version,
        "description": format_data.description,
        "author": format_data.author,
        "created": now,
        "updated": now,
        "tags": format_data.tags or [],
        "languages": format_data.languages,
        "primary_language": format_data.primary_language,
        "wrapper": format_data.wrapper,
        "scoring": format_data.scoring.dict() if format_data.scoring else {
            "presence_weight": 20,
            "similarity_weight": 35,
            "coherence_weight": 25,
            "depth_weight": 15,
            "structure_weight": 5,
            "pass_threshold": 60,
            "excellent_threshold": 85
        },
        "parser": format_data.parser.dict() if format_data.parser else {
            "header_pattern": "###",
            "field_separator": "\n\n",
            "case_sensitive": False
        },
        "fields": [f.dict() for f in format_data.fields],
        "expected_structure": {
            "format": "markdown",
            "has_headers": True,
            "min_fields": len(format_data.fields),
            "max_fields": len(format_data.fields)
        },
        "examples": {"good": [], "bad": []}
    }
    
    # Validate
    errors = validate_format(fmt_dict)
    if errors:
        raise HTTPException(status_code=400, detail={"validation_errors": errors})
    
    # Save
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(fmt_dict, f, indent=2, ensure_ascii=False)
    
    # Clear cache
    clear_cache()
    
    return {
        "status": "FORMAT_CREATED",
        "message": f"Format '{format_data.name}' wurde geboren! 🌟",
        "format": {
            "name": format_data.name,
            "path": str(path),
            "fields_count": len(format_data.fields)
        }
    }

# ============================================================================
# PUT ENDPOINT - UPDATE
# ============================================================================

@router.put("/{name}")
async def update_format(name: str, format_data: FormatUpdate):
    """
    🔄 Format aktualisieren
    """
    path = FORMATS_DIR / f"{name}.json"
    if not path.exists():
        raise HTTPException(
            status_code=404, 
            detail=f"Format '{name}' nicht gefunden! Nutze POST zum Erstellen."
        )
    
    # Load existing
    with open(path, 'r', encoding='utf-8') as f:
        existing = json.load(f)
    
    # Update nur was übergeben wurde
    if format_data.version:
        existing["version"] = format_data.version
    if format_data.description:
        existing["description"] = format_data.description
    if format_data.author:
        existing["author"] = format_data.author
    if format_data.tags is not None:
        existing["tags"] = format_data.tags
    if format_data.languages:
        existing["languages"] = format_data.languages
    if format_data.primary_language:
        existing["primary_language"] = format_data.primary_language
    if format_data.wrapper:
        existing["wrapper"] = format_data.wrapper
    if format_data.scoring:
        existing["scoring"] = format_data.scoring.dict()
    if format_data.parser:
        existing["parser"] = format_data.parser.dict()
    if format_data.fields:
        existing["fields"] = [f.dict() for f in format_data.fields]
        existing["expected_structure"]["min_fields"] = len(format_data.fields)
        existing["expected_structure"]["max_fields"] = len(format_data.fields)
    
    # Update timestamp
    existing["updated"] = datetime.now().strftime("%Y-%m-%d")
    
    # Validate
    errors = validate_format(existing)
    if errors:
        raise HTTPException(status_code=400, detail={"validation_errors": errors})
    
    # Save
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    
    # Clear cache
    clear_cache()
    
    return {
        "status": "FORMAT_UPDATED",
        "message": f"Format '{name}' wurde moduliert! 🔄",
        "format": {
            "name": name,
            "version": existing.get("version"),
            "fields_count": len(existing.get("fields", []))
        }
    }

# ============================================================================
# DELETE ENDPOINT
# ============================================================================

@router.delete("/{name}")
async def delete_format(name: str):
    """
    💀 Format löschen
    """
    path = FORMATS_DIR / f"{name}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Format '{name}' nicht gefunden")
    
    # Load for response
    with open(path, 'r', encoding='utf-8') as f:
        existing = json.load(f)
    
    # Delete
    path.unlink()
    
    # Clear cache
    clear_cache()
    
    return {
        "status": "FORMAT_DELETED",
        "message": f"Format '{name}' wurde freigegeben! 💀",
        "deleted": {
            "name": name,
            "had_fields": len(existing.get("fields", []))
        }
    }

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@router.post("/validate")
async def validate_format_endpoint(format_data: dict):
    """
    ✅ Format validieren ohne zu speichern
    """
    errors = validate_format(format_data)
    
    if errors:
        return {
            "status": "VALIDATION_FAILED",
            "valid": False,
            "errors": errors
        }
    
    return {
        "status": "VALIDATION_PASSED",
        "valid": True,
        "errors": []
    }

@router.post("/clear-cache")
async def clear_format_cache():
    """
    🧹 Format-Cache leeren
    """
    clear_cache()
    return {
        "status": "CACHE_CLEARED",
        "message": "Format-Cache wurde geleert!"
    }
