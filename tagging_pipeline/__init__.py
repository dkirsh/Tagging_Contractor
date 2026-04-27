"""Tagging pipeline package for the Tagging_Contractor project.

This package hosts the runtime extraction code that consumes images (and where
available 3D / floor-plan substrates) and emits registry-conformant tag values.

Sprint 1 (2026-04 / 2026-05) reserves the API surface for the L41-L58
social-interaction latents. The actual extractor implementations land in
Sprint 2; the present package contains only stub functions that raise
NotImplementedError so that downstream consumers can wire against the
agreed-upon function signatures and output dict shapes today.
"""
