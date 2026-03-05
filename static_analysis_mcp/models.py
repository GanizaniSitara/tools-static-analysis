"""Pydantic models for MCP tool responses.

Defines type-safe models for all MCP tool return values.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response."""
    isError: bool = True
    message: str


class Finding(BaseModel):
    """A code smell or issue finding."""
    project: str
    repo: str
    file_path: str = Field(alias="path")
    line: int
    smell_type: str
    severity: str
    category: str
    description: str
    context: Optional[str] = None
    source_code: Optional[str] = None

    class Config:
        populate_by_name = True


class ScanSummary(BaseModel):
    """Summary of a scan's results."""
    generated: str
    scan_root: str = Field(alias="scanRoot")
    total_files_scanned: int
    total_files_with_smells: int
    total_smells: int
    top_smell_types: List[Dict[str, Any]]
    severity_counts: Dict[str, int]
    category_counts: Dict[str, int]
    level: str

    class Config:
        populate_by_name = True


class ProjectMetrics(BaseModel):
    """Metrics for a single project."""
    project: str
    repo: str
    category: str
    layer: str
    fan_in: int
    fan_out: int
    has_tests: bool
    total_files: int
    total_lines: int
    complexity_score: int
    smell_count: int
    top_smells: List[str]


class DependencyNode(BaseModel):
    """A node in the dependency graph."""
    id: str
    project: str
    repo: str
    type: str
    path: str
    global_path: str = Field(alias="globalPath")
    description: str

    class Config:
        populate_by_name = True


class DependencyEdge(BaseModel):
    """An edge in the dependency graph."""
    source: str
    target: str
    type: str


class DependencyGraph(BaseModel):
    """Project dependency graph."""
    nodes: List[DependencyNode]
    edges: List[DependencyEdge]


class FixState(BaseModel):
    """State of a fix workflow."""
    fix_id: str
    smell_type: str
    file_path: str
    line: int
    project: str
    status: str
    branch: Optional[str] = None
    editor: str
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    error: Optional[str] = None

    class Config:
        populate_by_name = True


class ScanStatus(BaseModel):
    """Status of a running scan."""
    scan_id: str
    status: str
    output_dir: str
    start_time: str
    end_time: Optional[str] = None
    pid: Optional[int] = None
    error: Optional[str] = None


class TriageDecision(BaseModel):
    """Triage decision for a finding."""
    project: str
    file_path: str
    line: int
    smell_type: str
    status: str  # open, in_progress, resolved, wont_fix, false_positive
    assigned_to: Optional[str] = None
    notes: Optional[str] = None
    updated_at: str


class DataFlow(BaseModel):
    """Data flow information."""
    project: str
    sources: List[str]
    sinks: List[str]
    flow_type: str
    risk_level: Optional[str] = None


class CircularDependency(BaseModel):
    """A circular dependency in the graph."""
    cycle: List[str]
    severity: str
    description: str


class CodeSearchResult(BaseModel):
    """A code search result."""
    file_path: str
    line: int
    content: str
    project: str
    match_context: Optional[str] = None


class PromptTemplate(BaseModel):
    """AI prompt template."""
    name: str
    description: str
    template: str
    variables: List[str]


class ViewerUrl(BaseModel):
    """Viewer URL information."""
    url: str
    output_dir: str
    available: bool
    message: Optional[str] = None
