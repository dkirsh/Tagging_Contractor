"""Sprint 1 contract tests for the L41-L58 latent extractor stubs.

These tests verify three properties:

1. The dispatch table (``LATENT_EXTRACTORS``) contains exactly 18 entries
   keyed L41..L58.
2. ``get_extractor`` resolves each id to the matching ``detect_L##`` callable.
3. Each stub raises ``NotImplementedError`` whose message contains the
   string ``"Sprint 2"`` (so the deferred work is grep-able).

Sprint 2 will replace the stubs with real implementations; these tests
will at that point be expected to *fail* and will be replaced or relaxed
accordingly.
"""

from __future__ import annotations

import inspect

import pytest

from tagging_pipeline.extractors.latents import LATENT_EXTRACTORS, get_extractor


EXPECTED_IDS = [f"L{n}" for n in range(41, 59)]  # L41 .. L58 inclusive
VLM_IDS = {"L46", "L47"}


def test_dispatch_table_has_eighteen_entries():
    """LATENT_EXTRACTORS must contain exactly 18 entries (L41..L58)."""
    assert len(LATENT_EXTRACTORS) == 18, (
        f"Expected 18 entries, got {len(LATENT_EXTRACTORS)}: "
        f"{sorted(LATENT_EXTRACTORS)}"
    )


def test_dispatch_table_keys_are_l41_through_l58():
    """Dispatch keys must be exactly the canonical L41..L58 set."""
    assert sorted(LATENT_EXTRACTORS) == EXPECTED_IDS


def test_get_extractor_resolves_each_id():
    """``get_extractor`` must return the same callable as the dict lookup."""
    for attribute_id in EXPECTED_IDS:
        assert get_extractor(attribute_id) is LATENT_EXTRACTORS[attribute_id]


def test_get_extractor_raises_keyerror_for_unknown_id():
    """``get_extractor`` must raise ``KeyError`` for unregistered ids."""
    with pytest.raises(KeyError):
        get_extractor("L999")


@pytest.mark.parametrize("attribute_id", EXPECTED_IDS)
def test_stub_raises_not_implemented_with_sprint_2_message(attribute_id: str):
    """Each stub must raise NotImplementedError whose message names Sprint 2."""
    extractor = LATENT_EXTRACTORS[attribute_id]
    sig = inspect.signature(extractor)
    param_names = list(sig.parameters)

    # Build dummy args that match the published signature without invoking
    # any real numpy/VLM machinery — the stub must raise before touching
    # the inputs.
    if attribute_id in VLM_IDS:
        # vlm signature: (image, vlm_client=None)
        assert param_names == ["image", "vlm_client"], (
            f"{attribute_id}: expected (image, vlm_client) signature, "
            f"got {param_names}"
        )
        with pytest.raises(NotImplementedError) as excinfo:
            extractor(image=None, vlm_client=None)
    else:
        # composite/geometry signature: (image, segments, depth=None)
        assert param_names == ["image", "segments", "depth"], (
            f"{attribute_id}: expected (image, segments, depth) signature, "
            f"got {param_names}"
        )
        with pytest.raises(NotImplementedError) as excinfo:
            extractor(image=None, segments={}, depth=None)

    message = str(excinfo.value)
    assert "Sprint 2" in message, (
        f"{attribute_id}: NotImplementedError message must mention 'Sprint 2' "
        f"so it is grep-able; got: {message!r}"
    )
