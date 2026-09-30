"""Current and historical provenance projections."""

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.domain.review import Origin


class RevisionProvenance(BaseModel):
    """Describe the origin of one retained revision."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    revision_id: str = Field(min_length=1)
    revision_number: int = Field(ge=1)
    origin: Origin


class ProvenanceProjection(BaseModel):
    """Separate current origin from historical approval state."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    field_id: str = Field(min_length=1)
    current: RevisionProvenance
    history: tuple[RevisionProvenance, ...]
    reapproval_required: bool
