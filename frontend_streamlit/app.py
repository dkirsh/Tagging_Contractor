"""
TRS Streamlit UI with Proposal Workflow

Pages:
- Public Tag Explorer: Read-only discovery surface
- Dashboard: Overview and stats
- Registry Browser: Browse all tags
- Tag Inspector: View tag details
- Search: Resolve terms to tags
- ---
- Propose Tag: Submit new proposals
- Review Queue: Review pending proposals
- ---
- Releases: Release dashboard
- Contracts: View contracts
- Audit Log: View all actions
"""

import os
from pathlib import Path
from typing import Any

import pandas as pd
import requests
import streamlit as st

def _read_text(path: str, default: str = "unknown") -> str:
    try:
        return Path(path).read_text(encoding="utf-8").strip()
    except Exception:
        return default

SYSTEM_VERSION = _read_text("/app/VERSION.txt")
CORE_VERSION = os.getenv("TRS_CORE_VER", "unknown")

def render_version_sidebar():
    st.sidebar.markdown("### Tagging_Contractor")
    st.sidebar.markdown(f"**System:** {SYSTEM_VERSION}")
    st.sidebar.markdown(f"**Core:** {CORE_VERSION}")

API_URL = os.getenv("TRS_API_URL", "http://localhost:8401")

st.set_page_config(
    page_title="Tag Registry Service",
    page_icon="🏷️",
    layout="wide",
)

st.markdown(
    """
    <style>
      .trs-intro {
        padding: 1rem 1.2rem;
        background: linear-gradient(135deg, #eff7f4 0%, #f7f5ef 100%);
        border: 1px solid #d8e5df;
        border-radius: 0.9rem;
        margin-bottom: 1rem;
      }
      .trs-intro h3 {
        margin: 0 0 0.35rem 0;
        color: #1c3d3a;
      }
      .trs-badge-row {
        margin: 0.35rem 0 0.75rem 0;
      }
      .trs-badge {
        display: inline-block;
        padding: 0.18rem 0.5rem;
        border-radius: 999px;
        margin: 0 0.35rem 0.35rem 0;
        font-size: 0.78rem;
        border: 1px solid #d6d6d6;
        background: #f7f7f7;
        color: #2d2010;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


render_version_sidebar()
# Session state for API key
if "api_key" not in st.session_state:
    st.session_state.api_key = ""


def get_headers():
    """Get headers with API key if set."""
    headers = {}
    if st.session_state.api_key:
        headers["X-API-Key"] = st.session_state.api_key
    return headers


def get_json(path, params=None):
    """GET request to API."""
    try:
        r = requests.get(f"{API_URL}{path}", params=params, headers=get_headers(), timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None


def post_json(path, data):
    """POST request to API."""
    try:
        r = requests.post(f"{API_URL}{path}", json=data, headers=get_headers(), timeout=30)
        if r.status_code == 401:
            st.error("Authentication required. Enter your API key in the sidebar.")
            return None
        if r.status_code == 403:
            st.error("Permission denied. You don't have the required role.")
            return None
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None


def load_registry_tags() -> tuple[dict[str, dict[str, Any]], dict[str, Any] | None]:
    """Load registry and return (tags, registry)."""
    registry = get_json("/registry")
    if not registry:
        return {}, None
    tags = registry.get("tags", {})
    if not isinstance(tags, dict):
        st.error("Registry payload did not contain a tag dictionary.")
        return {}, registry
    return tags, registry


def normalized_extractability(tag: dict[str, Any]) -> dict[str, Any]:
    extract = tag.get("extractability", {})
    if not isinstance(extract, dict):
        extract = {}
    return {
        "from_2d": extract.get("from_2d") or "unknown",
        "from_3d_vr": extract.get("from_3d_vr") or "unknown",
        "monocular_3d_approx": extract.get("monocular_3d_approx") or "unknown",
        "region_support": bool(extract.get("region_support")),
    }


def registry_rows(tags: dict[str, dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for tag_id, tag in tags.items():
        if not isinstance(tag, dict):
            continue
        extract = normalized_extractability(tag)
        semantics = tag.get("semantics", {})
        if not isinstance(semantics, dict):
            semantics = {}
        rows.append(
            {
                "tag_id": tag_id,
                "canonical_name": tag.get("canonical_name") or tag.get("name") or tag_id,
                "definition": semantics.get("definition_short") or tag.get("definition") or "",
                "status": tag.get("status") or "unknown",
                "value_type": tag.get("value_type") or "unknown",
                "domain": tag.get("domain") or "unknown",
                "subdomain": tag.get("subdomain") or "",
                "from_2d": extract["from_2d"],
                "from_3d_vr": extract["from_3d_vr"],
                "monocular_3d_approx": extract["monocular_3d_approx"],
                "region_support": extract["region_support"],
                "alias_count": len(semantics.get("aliases", []) if isinstance(semantics.get("aliases"), list) else []),
            }
        )
    return pd.DataFrame(rows)


def filter_rows(df: pd.DataFrame, domain: str, status: str, evidence: str) -> pd.DataFrame:
    filtered = df.copy()
    if domain != "(all)":
        filtered = filtered[filtered["domain"] == domain]
    if status != "(all)":
        filtered = filtered[filtered["status"] == status]
    if evidence == "2D-ready":
        filtered = filtered[filtered["from_2d"] == "yes"]
    elif evidence == "3D/VR involved":
        filtered = filtered[filtered["from_3d_vr"].isin(["yes", "partial"])]
    elif evidence == "Monocular 3D approximation":
        filtered = filtered[filtered["monocular_3d_approx"].isin(["yes", "partial"])]
    elif evidence == "Regional support":
        filtered = filtered[filtered["region_support"] == True]
    return filtered


def explorer_badges(tag: dict[str, Any]) -> str:
    extract = normalized_extractability(tag)
    badges = [
        f"2D: {extract['from_2d']}",
        f"3D/VR: {extract['from_3d_vr']}",
        f"Monocular 3D: {extract['monocular_3d_approx']}",
        "Regional" if extract["region_support"] else "Global/default",
    ]
    return "".join(f"<span class='trs-badge'>{label}</span>" for label in badges)


def render_tag_detail(tag_id: str, tag: dict[str, Any]) -> None:
    semantics = tag.get("semantics", {})
    if not isinstance(semantics, dict):
        semantics = {}

    st.subheader(f"{tag.get('canonical_name') or tag_id}")
    st.caption(tag_id)
    st.markdown(f"<div class='trs-badge-row'>{explorer_badges(tag)}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.4, 1])
    with col1:
        st.write(semantics.get("definition_long") or tag.get("definition") or "No definition supplied.")
        if semantics.get("extraction_notes_2d"):
            st.markdown("**2D extraction notes**")
            st.write(semantics.get("extraction_notes_2d"))
        if semantics.get("extraction_notes_3d"):
            st.markdown("**3D / VR extraction notes**")
            st.write(semantics.get("extraction_notes_3d"))
    with col2:
        st.markdown("**Tag profile**")
        st.write(f"Status: `{tag.get('status') or 'unknown'}`")
        st.write(f"Value type: `{tag.get('value_type') or 'unknown'}`")
        st.write(f"Domain: `{tag.get('domain') or 'unknown'}`")
        if tag.get("subdomain"):
            st.write(f"Subdomain: `{tag.get('subdomain')}`")
        if tag.get("unit"):
            st.write(f"Unit: `{tag.get('unit')}`")

    aliases = semantics.get("aliases")
    if isinstance(aliases, list) and aliases:
        st.markdown("**Aliases**")
        st.write(", ".join(str(a) for a in aliases[:20]))

    col3, col4 = st.columns(2)
    with col3:
        if semantics.get("examples_positive"):
            st.markdown("**Positive examples**")
            for item in semantics["examples_positive"][:6]:
                st.write(f"- {item}")
        if semantics.get("scope_includes"):
            st.markdown("**Scope includes**")
            for item in semantics["scope_includes"][:6]:
                st.write(f"- {item}")
    with col4:
        if semantics.get("examples_negative"):
            st.markdown("**Negative examples**")
            for item in semantics["examples_negative"][:6]:
                st.write(f"- {item}")
        if semantics.get("scope_excludes"):
            st.markdown("**Scope excludes**")
            for item in semantics["scope_excludes"][:6]:
                st.write(f"- {item}")

    related_tags = semantics.get("related_tags")
    if isinstance(related_tags, list) and related_tags:
        st.markdown("**Related tags**")
        st.write(", ".join(str(t) for t in related_tags[:20]))

    with st.expander("Full tag JSON"):
        st.json(tag)


# Sidebar
st.sidebar.title("🏷️ Tag Registry")

# API Key input
with st.sidebar.expander("🔑 Authentication", expanded=not st.session_state.api_key):
    api_key = st.text_input(
        "API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your TRS API key for write access",
    )
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        st.rerun()
    
    if st.session_state.api_key:
        st.success("🔓 Authenticated")
    else:
        st.info("Read-only mode. Enter API key for write access.")

st.sidebar.divider()

# Navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "🧭 Public Tag Explorer",
        "📊 Dashboard",
        "📚 Registry Browser",
        "🔍 Tag Inspector",
        "🔎 Search",
        "📈 Registry Stats",
        "---",
        "➕ Propose Tag",
        "📝 Review Queue",
        "---",
        "🚀 Releases",
        "📄 Contracts",
        "📋 Audit Log",
        "⚡ System Metrics",
    ],
)

# Handle dividers
if page.startswith("---"):
    page = "📊 Dashboard"

# ============================================================================
# Public Tag Explorer
# ============================================================================
if page == "🧭 Public Tag Explorer":
    st.title("🧭 Public Tag Explorer")
    st.markdown(
        """
        <div class="trs-intro">
          <h3>Read-only discovery surface</h3>
          <p>
            This view is for researchers, students, contributors, and ordinary visitors who
            simply want to understand what a CNFA tag means, what kind of evidence it needs,
            and how it relates to the rest of the registry. It is intentionally read-only.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tags, _registry = load_registry_tags()
    if not tags:
        st.stop()

    df = registry_rows(tags)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tags", len(df))
    col2.metric("Domains", df["domain"].nunique())
    col3.metric("2D-ready", int((df["from_2d"] == "yes").sum()))
    col4.metric("Regional", int(df["region_support"].sum()))

    search_col, domain_col, status_col, evidence_col = st.columns([1.4, 1, 1, 1])
    with search_col:
        search_query = st.text_input("Search", placeholder="lighting, cozy, biophilic, openness...")
    with domain_col:
        domain = st.selectbox("Domain", ["(all)"] + sorted(d for d in df["domain"].dropna().unique() if str(d).strip()))
    with status_col:
        status = st.selectbox("Status", ["(all)"] + sorted(s for s in df["status"].dropna().unique() if str(s).strip()))
    with evidence_col:
        evidence = st.selectbox(
            "Evidence profile",
            ["(all)", "2D-ready", "3D/VR involved", "Monocular 3D approximation", "Regional support"],
        )

    filtered = filter_rows(df, domain, status, evidence)

    score_map: dict[str, float] = {}
    if search_query.strip():
        params: dict[str, Any] = {"q": search_query.strip(), "limit": 100}
        if domain != "(all)":
            params["domain"] = domain
        if status != "(all)":
            params["status"] = status
        search_results = get_json("/api/search", params=params) or {}
        ids = [row["tag_id"] for row in search_results.get("results", []) if row["tag_id"] in set(filtered["tag_id"])]
        score_map = {row["tag_id"]: row.get("score", 0.0) for row in search_results.get("results", [])}
        filtered = filtered[filtered["tag_id"].isin(ids)].copy()
        filtered["score"] = filtered["tag_id"].map(score_map).fillna(0.0)
        filtered = filtered.sort_values(["score", "tag_id"], ascending=[False, True])
    else:
        filtered = filtered.sort_values(["domain", "canonical_name", "tag_id"])

    st.write(f"Showing {len(filtered)} tags.")
    preview_cols = ["tag_id", "canonical_name", "domain", "status", "value_type", "from_2d", "from_3d_vr"]
    if "score" in filtered.columns:
        preview_cols = ["score"] + preview_cols
    st.dataframe(filtered[preview_cols], use_container_width=True, hide_index=True, height=280)

    if filtered.empty:
        st.info("No tags matched the current filters.")
        st.stop()

    selection_ids = filtered["tag_id"].tolist()
    selected_id = st.selectbox(
        "Inspect a tag",
        selection_ids,
        format_func=lambda tag_id: f"{tag_id} — {tags[tag_id].get('canonical_name') or tag_id}",
    )
    render_tag_detail(selected_id, tags[selected_id])

# ============================================================================
# Dashboard
# ============================================================================
elif page == "📊 Dashboard":
    st.title("📊 Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Registry Status")
        status = get_json("/status")
        if status:
            st.metric("Tags", status.get("counts", {}).get("tag_count", 0))
            st.metric("Version", status.get("core_version", "unknown"))
            st.metric("Contracts", status.get("counts", {}).get("contracts_files", 0))
    
    with col2:
        st.subheader("Proposal Queue")
        stats = get_json("/api/proposals/stats")
        if stats:
            col2a, col2b, col2c = st.columns(3)
            col2a.metric("Pending", stats.get("pending", 0))
            col2b.metric("Approved", stats.get("approved", 0))
            col2c.metric("Total", stats.get("total", 0))
    
    st.divider()
    
    # Recent proposals
    st.subheader("Recent Proposals")
    proposals = get_json("/api/proposals", params={"limit": 10})
    if proposals:
        for p in proposals[:5]:
            status_emoji = {"pending": "⏳", "approved": "✅", "rejected": "❌", "merged": "🔄"}.get(p["status"], "❓")
            st.write(f"{status_emoji} **{p['tag_id']}** — {p['proposal_type']} by {p['submitter']} ({p['status']})")
    else:
        st.info("No proposals yet.")

# ============================================================================
# Registry Browser
# ============================================================================
elif page == "📚 Registry Browser":
    st.title("📚 Registry Browser")
    
    reg = get_json("/registry")
    if not reg:
        st.stop()
    
    tags = reg.get("tags", {})
    rows = []
    
    if isinstance(tags, dict):
        for k, v in tags.items():
            if isinstance(v, dict):
                rows.append({
                    "tag_id": k,
                    "canonical_name": v.get("canonical_name") or v.get("name"),
                    "status": v.get("status"),
                    "value_type": v.get("value_type"),
                    "domain": v.get("domain"),
                    "subdomain": v.get("subdomain"),
                })
    
    df = pd.DataFrame(rows)
    if df.empty:
        st.warning("No tags found.")
        st.stop()
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        domains = ["(all)"] + sorted([d for d in df["domain"].dropna().unique() if str(d).strip()])
        domain = st.selectbox("Domain", domains)
    
    with col2:
        statuses = ["(all)"] + sorted([s for s in df["status"].dropna().unique() if str(s).strip()])
        status = st.selectbox("Status", statuses)
    
    with col3:
        search = st.text_input("Filter by name/ID")
    
    # Apply filters
    if domain != "(all)":
        df = df[df["domain"] == domain]
    if status != "(all)":
        df = df[df["status"] == status]
    if search:
        mask = df["tag_id"].str.contains(search, case=False, na=False) | \
               df["canonical_name"].str.contains(search, case=False, na=False)
        df = df[mask]
    
    st.write(f"Showing {len(df)} of {len(rows)} tags")
    st.dataframe(df, use_container_width=True, height=500)

# ============================================================================
# Tag Inspector
# ============================================================================
elif page == "🔍 Tag Inspector":
    st.title("🔍 Tag Inspector")
    
    reg = get_json("/registry")
    if not reg:
        st.stop()
    
    tags = reg.get("tags", {})
    if not isinstance(tags, dict) or not tags:
        st.warning("No tags found.")
        st.stop()
    
    tag_id = st.selectbox("Select Tag", sorted(tags.keys()))
    
    if tag_id:
        tag = tags[tag_id]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Basic Info")
            st.write(f"**Canonical Name:** {tag.get('canonical_name')}")
            st.write(f"**Status:** {tag.get('status')}")
            st.write(f"**Value Type:** {tag.get('value_type')}")
            st.write(f"**Domain:** {tag.get('domain')}")
            st.write(f"**Definition:** {tag.get('definition', 'N/A')}")
        
        with col2:
            st.subheader("Extractability")
            extract = tag.get("extractability", {})
            st.write(f"**From 2D:** {extract.get('from_2d', 'N/A')}")
            st.write(f"**From 3D/VR:** {extract.get('from_3d_vr', 'N/A')}")
            st.write(f"**Monocular 3D:** {extract.get('monocular_3d_approx', 'N/A')}")
        
        with st.expander("Full JSON"):
            st.json(tag)

# ============================================================================
# Search
# ============================================================================
elif page == "🔎 Search":
    st.title("🔎 Search Tags")
    
    term = st.text_input("Search term (alias, name, or tag ID)", "")
    
    if term.strip():
        results = get_json("/resolve", params={"term": term, "limit": 25})
        if results:
            matches = results.get("matches", [])
            st.write(f"Found {len(matches)} matches for '{term}'")
            
            for m in matches:
                with st.expander(f"**{m['tag_id']}** — {m.get('canonical_name', '')}"):
                    st.write(f"Status: {m.get('status')}")
                    st.write(f"Value Type: {m.get('value_type')}")
                    st.write(f"Domain: {m.get('domain')}")

# ============================================================================
# Registry Stats
# ============================================================================
elif page == "📈 Registry Stats":
    st.title("📈 Registry Statistics")
    
    stats = get_json("/api/stats")
    
    if stats:
        st.metric("Total Tags", stats.get("total_tags", 0))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("By Status")
            for status, count in sorted(stats.get("by_status", {}).items()):
                st.write(f"**{status}**: {count}")
        
        with col2:
            st.subheader("By Value Type")
            for vtype, count in sorted(stats.get("by_value_type", {}).items()):
                st.write(f"**{vtype}**: {count}")
        
        with col3:
            st.subheader("By Domain")
            for domain, count in sorted(stats.get("by_domain", {}).items(), key=lambda x: -x[1]):
                domain_short = domain[:30] + "..." if len(domain) > 30 else domain
                st.write(f"**{domain_short}**: {count}")
        
        st.divider()
        
        # Fuzzy search
        st.subheader("🔍 Smart Search")
        search_query = st.text_input("Search (fuzzy matching)", placeholder="e.g., 'warm light' or 'ceiling'")
        
        col1, col2 = st.columns(2)
        with col1:
            domains = get_json("/api/domains")
            domain_filter = st.selectbox("Filter by Domain", ["(all)"] + (domains.get("domains", []) if domains else []))
        with col2:
            status_filter = st.selectbox("Filter by Status", ["(all)", "active", "deprecated", "experimental"])
        
        if search_query:
            params = {"q": search_query, "limit": 25}
            if domain_filter != "(all)":
                params["domain"] = domain_filter
            if status_filter != "(all)":
                params["status"] = status_filter
            
            search_results = get_json("/api/search", params=params)
            
            if search_results:
                st.write(f"Found {search_results.get('count', 0)} results")
                
                for r in search_results.get("results", []):
                    score = r.get("score", 0)
                    score_color = "🟢" if score > 0.8 else "🟡" if score > 0.6 else "🔴"
                    
                    with st.expander(f"{score_color} **{r['tag_id']}** ({score:.0%})"):
                        st.write(f"**Name:** {r.get('canonical_name', 'N/A')}")
                        st.write(f"**Definition:** {r.get('definition', 'N/A')}")
                        st.write(f"**Status:** {r.get('status')} | **Type:** {r.get('value_type')}")
                        if r.get("match_field"):
                            st.caption(f"Matched: {r['match_field']}")

# ============================================================================
# Propose Tag
# ============================================================================
elif page == "➕ Propose Tag":
    st.title("➕ Propose New Tag")
    
    if not st.session_state.api_key:
        st.warning("⚠️ Authentication required to submit proposals. Enter your API key in the sidebar.")
        st.stop()
    
    with st.form("proposal_form"):
        st.subheader("Tag Details")
        
        proposal_type = st.selectbox(
            "Proposal Type",
            ["new_tag", "modify_tag", "deprecate_tag"],
            help="new_tag: Add a new tag, modify_tag: Change existing tag, deprecate_tag: Mark tag as deprecated"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            canonical_name = st.text_input("Canonical Name*", help="Human-readable name")
            tag_id = st.text_input(
                "Tag ID*",
                help="Format: category.domain.attribute (e.g., env.lighting.warmth)"
            )
        
        with col2:
            domain = st.selectbox("Domain", [
                "A. Luminous Environment",
                "B. Chromatic Environment",
                "C. Material and Texture",
                "D. Geometric Pattern and Form",
                "E. Spatial Configuration",
                "F. Order and Maintenance",
                "G. Nature and Biophilia",
                "H. Furnishing and Function",
                "I. Social and Cultural",
                "J. Safety and Security",
                "K. Acoustic Environment",
                "L. Thermal Environment",
                "M. Olfactory Environment",
                "N. Signs and Symbols",
            ])
            value_type = st.selectbox("Value Type", ["ordinal", "binary", "continuous", "categorical"])
        
        definition = st.text_area("Definition*", help="Clear description of what this tag measures")
        
        st.subheader("Evidence")
        evidence_doi = st.text_input("Evidence DOI", placeholder="https://doi.org/10.xxxx/...")
        reason = st.text_area("Reason for Proposal", help="Why is this tag needed?")
        
        st.subheader("Aliases")
        aliases_text = st.text_input("Aliases (comma-separated)", help="Alternative names for this tag")
        
        submitted = st.form_submit_button("Submit Proposal", type="primary")
        
        if submitted:
            if not all([canonical_name, tag_id, definition]):
                st.error("Please fill in all required fields (marked with *)")
            else:
                # Build payload
                payload = {
                    "canonical_name": canonical_name,
                    "category": "environmental",
                    "value_type": value_type,
                    "status": "proposed",
                    "domain": domain,
                    "definition": definition,
                    "semantics": {
                        "aliases": [a.strip() for a in aliases_text.split(",") if a.strip()]
                    }
                }
                
                result = post_json("/api/proposals", {
                    "proposal_type": proposal_type,
                    "tag_id": tag_id,
                    "canonical_name": canonical_name,
                    "payload": payload,
                    "evidence_doi": evidence_doi or None,
                    "reason": reason or None,
                })
                
                if result:
                    st.success(f"✅ Proposal #{result['id']} submitted successfully!")
                    st.balloons()

# ============================================================================
# Review Queue
# ============================================================================
elif page == "📝 Review Queue":
    st.title("📝 Review Queue")
    
    # Status filter
    status_filter = st.selectbox("Filter by Status", ["pending", "approved", "rejected", "all"])
    
    params = {"limit": 50}
    if status_filter != "all":
        params["status"] = status_filter
    
    proposals = get_json("/api/proposals", params=params)
    
    if not proposals:
        st.info("No proposals found.")
        st.stop()
    
    st.write(f"Showing {len(proposals)} proposals")
    
    for p in proposals:
        status_emoji = {
            "pending": "⏳",
            "approved": "✅",
            "rejected": "❌",
            "merged": "🔄",
            "withdrawn": "🚫",
        }.get(p["status"], "❓")
        
        with st.expander(f"{status_emoji} **{p['tag_id']}** — {p['canonical_name'] or p['proposal_type']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Type:** {p['proposal_type']}")
                st.write(f"**Submitter:** {p['submitter']}")
                st.write(f"**Submitted:** {p['created_at']}")
                if p.get("reason"):
                    st.write(f"**Reason:** {p['reason']}")
                if p.get("evidence_doi"):
                    st.write(f"**Evidence:** {p['evidence_doi']}")
            
            with col2:
                st.write(f"**Status:** {p['status']}")
                st.write(f"**ID:** #{p['id']}")
            
            with st.expander("View Payload"):
                st.json(p.get("payload", {}))
            
            # Review actions (only for pending)
            if p["status"] == "pending" and st.session_state.api_key:
                st.divider()
                st.write("**Review Actions**")
                
                comment = st.text_input(f"Comment for #{p['id']}", key=f"comment_{p['id']}")
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("✅ Approve", key=f"approve_{p['id']}", type="primary"):
                        result = post_json(f"/api/proposals/{p['id']}/review", {
                            "decision": "approve",
                            "comment": comment or None,
                        })
                        if result:
                            st.success("Approved!")
                            st.rerun()
                
                with col_b:
                    if st.button("❌ Reject", key=f"reject_{p['id']}"):
                        result = post_json(f"/api/proposals/{p['id']}/review", {
                            "decision": "reject",
                            "comment": comment or "Rejected",
                        })
                        if result:
                            st.warning("Rejected.")
                            st.rerun()
                
                with col_c:
                    if st.button("📝 Request Changes", key=f"changes_{p['id']}"):
                        if not comment:
                            st.error("Please provide a comment explaining requested changes.")
                        else:
                            result = post_json(f"/api/proposals/{p['id']}/review", {
                                "decision": "request_changes",
                                "comment": comment,
                            })
                            if result:
                                st.info("Changes requested.")
                                st.rerun()

# ============================================================================
# Releases
# ============================================================================
elif page == "🚀 Releases":
    st.title("🚀 Release Dashboard")
    
    # Stats
    col1, col2, col3 = st.columns(3)
    
    stats = get_json("/api/proposals/stats")
    status = get_json("/status")
    latest = get_json("/api/releases/latest")
    
    with col1:
        st.metric("Current Version", status.get("core_version", "unknown") if status else "?")
    
    with col2:
        st.metric("Pending Proposals", stats.get("pending", 0) if stats else 0)
    
    with col3:
        st.metric("Approved (Ready)", stats.get("approved", 0) if stats else 0)
    
    st.divider()
    
    # Release form
    if st.session_state.api_key:
        with st.expander("🚀 Create New Release"):
            with st.form("release_form"):
                version = st.text_input("Version", placeholder="v0.2.9")
                release_notes = st.text_area("Release Notes")
                
                if st.form_submit_button("Create Release", type="primary"):
                    if not version or not version.startswith("v"):
                        st.error("Version must start with 'v' (e.g., v0.2.9)")
                    else:
                        result = post_json("/api/releases", {
                            "version": version,
                            "release_notes": release_notes or None,
                        })
                        if result:
                            st.success(f"Release {version} created!")
                            st.rerun()
    
    st.divider()
    
    # Release history
    st.subheader("Release History")
    releases = get_json("/api/releases", params={"limit": 20})
    
    if releases:
        for r in releases:
            with st.expander(f"**{r['version']}** — {r['created_at'][:10]}"):
                st.write(f"**Released by:** {r['released_by']}")
                st.write(f"**Previous:** {r.get('previous_version') or 'N/A'}")
                st.write(f"**Changes:** +{r['tags_added']} / ~{r['tags_modified']} / -{r['tags_removed']}")
                if r.get("release_notes"):
                    st.write(f"**Notes:** {r['release_notes']}")
    else:
        st.info("No releases recorded yet.")

# ============================================================================
# Contracts
# ============================================================================
elif page == "📄 Contracts":
    st.title("📄 Contracts")
    
    consumer = st.selectbox(
        "Consumer",
        ["image_tagger", "article_eater", "bn", "preference_testing"],
    )
    
    contract = get_json("/contracts/latest", params={"consumer": consumer})
    
    if contract:
        meta = contract.get("meta", {})
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Version", meta.get("contract_version", "?"))
        col2.metric("Tags", len(contract.get("tags", [])))
        col3.metric("SHA256", meta.get("registry_sha256", "?")[:12] + "...")
        
        with st.expander("View Full Contract"):
            st.json(contract)

# ============================================================================
# Audit Log
# ============================================================================
elif page == "📋 Audit Log":
    st.title("📋 Audit Log")
    
    if not st.session_state.api_key:
        st.warning("⚠️ Authentication required to view audit log.")
        st.stop()
    
    col1, col2 = st.columns(2)
    
    with col1:
        action_filter = st.selectbox("Filter by Action", ["(all)", "proposal_created", "proposal_reviewed", "release_created", "api_access"])
    
    with col2:
        limit = st.number_input("Limit", min_value=10, max_value=500, value=100)
    
    params = {"limit": limit}
    if action_filter != "(all)":
        params["action"] = action_filter
    
    entries = get_json("/api/audit", params=params)
    
    if entries:
        for e in entries:
            timestamp = e.get("timestamp", "")[:19]
            action = e.get("action", "")
            user = e.get("user_id", "")
            target = f"{e.get('target_type', '')}/{e.get('target_id', '')}" if e.get("target_type") else ""
            
            st.write(f"`{timestamp}` | **{action}** | {user} | {target}")
    else:
        st.info("No audit entries found.")

# ============================================================================
# System Metrics
# ============================================================================
elif page == "⚡ System Metrics":
    st.title("⚡ System Metrics")
    
    # Health status
    st.subheader("🏥 System Health")
    health = get_json("/dashboard/health")
    
    if health:
        status = "🟢 Healthy" if health.get("healthy") else "🔴 Unhealthy"
        st.markdown(f"**Status:** {status}")
        
        deps = health.get("dependencies", [])
        
        cols = st.columns(len(deps))
        for i, dep in enumerate(deps):
            with cols[i]:
                name = dep.get("name", "Unknown")
                is_healthy = dep.get("healthy", False)
                icon = "✅" if is_healthy else "❌"
                st.metric(name.capitalize(), icon)
                
                if "latency_ms" in dep:
                    st.caption(f"{dep['latency_ms']:.1f}ms")
                
                if "error" in dep:
                    st.error(dep["error"])
    
    st.divider()
    
    # Metrics
    st.subheader("📊 Performance Metrics")
    metrics_data = get_json("/dashboard/metrics")
    
    if metrics_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            uptime = metrics_data.get("uptime_seconds", 0)
            hours = int(uptime // 3600)
            mins = int((uptime % 3600) // 60)
            st.metric("Uptime", f"{hours}h {mins}m")
        
        with col2:
            active = metrics_data.get("requests", {}).get("active", 0)
            st.metric("Active Requests", active)
        
        with col3:
            cache = metrics_data.get("cache", {})
            hit_rate = cache.get("hit_rate", 0)
            st.metric("Cache Hit Rate", f"{hit_rate:.0%}")
        
        with col4:
            db = metrics_data.get("database", {})
            queries = db.get("query_count", 0)
            st.metric("DB Queries", queries)
        
        # Business metrics
        st.subheader("📈 Business Metrics")
        biz = metrics_data.get("business", {})
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Proposals Created", biz.get("proposals_created", 0))
        with col2:
            st.metric("Proposals Approved", biz.get("proposals_approved", 0))
        with col3:
            st.metric("Releases", biz.get("releases_created", 0))
        with col4:
            st.metric("Searches", biz.get("searches_performed", 0))
        
        # Errors
        errors = metrics_data.get("errors", {})
        if errors:
            st.subheader("⚠️ Errors")
            for error_type, count in errors.items():
                st.write(f"**{error_type}**: {count}")
    
    st.divider()
    
    # Database stats
    st.subheader("🗄️ Database")
    db_stats = get_json("/dashboard/database")
    
    if db_stats and "tables" in db_stats:
        col1, col2 = st.columns(2)
        
        with col1:
            size_mb = db_stats.get("size_bytes", 0) / (1024 * 1024)
            st.metric("Database Size", f"{size_mb:.2f} MB")
        
        with col2:
            tables = db_stats.get("tables", {})
            total_rows = sum(tables.values())
            st.metric("Total Rows", total_rows)
        
        with st.expander("Table Details"):
            for table, count in sorted(tables.items()):
                st.write(f"**{table}**: {count:,} rows")
    
    # System info
    st.divider()
    st.subheader("💻 System Info")
    sys_info = get_json("/dashboard/system")
    
    if sys_info:
        st.json(sys_info)
