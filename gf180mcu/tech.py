"""Technology definitions."""

from collections.abc import Callable
from functools import partial, wraps
from typing import Any

import gdsfactory as gf
from gdsfactory.cross_section import CrossSection
from gdsfactory.typings import LayerSpec

from gf180mcu.layers import LAYER, LAYER_STACK, LAYER_VIEWS  # noqa: F401

############################
# Cross-sections functions
############################

cross_sections: dict[str, Callable[..., CrossSection]] = {}
_cross_section_default_names: dict[str, str] = {}
# Registered functions whose default cross-section has not been built yet. They are built on the
# first call of any registered function, not at import: building a cross-section looks its layer
# up in the active PDK, and from gdsfactory 10 that lookup activates $PDK, which is this package,
# still half-imported (a circular import).
_pending_default_names: list[Callable[..., CrossSection]] = []


def _register_default_names() -> None:
    """Build the default cross-section of every pending function, in registration order."""
    while _pending_default_names:
        func = _pending_default_names.pop(0)
        _cross_section_default_names[func().name] = func.__name__


def xsection(func: Callable[..., CrossSection]) -> Callable[..., CrossSection]:
    """Returns decorated to register a cross section function.

    Ensures that the cross-section name matches the name of the function that generated it when created using default parameters

    ```python
        @xsection
        def strip(width=TECH.width_strip, radius=TECH.radius_strip):
            return gf.cross_section.cross_section(width=width, radius=radius)
    ```
    """
    _pending_default_names.append(func)

    @wraps(func)
    def newfunc(**kwargs: Any) -> CrossSection:
        _register_default_names()
        xs = func(**kwargs)
        if xs.name in _cross_section_default_names:
            xs._name = _cross_section_default_names[xs.name]
        return xs

    cross_sections[func.__name__] = newfunc
    return newfunc


@xsection
def metal1(
    width: float = 0.2,
    layer: LayerSpec = "metal1",
    radius: float | None = None,
) -> CrossSection:
    """Return Metal Strip cross_section."""
    return gf.cross_section.metal1(
        width=width,
        layer=layer,
        radius=radius,
        radius_min=None,
    )


@xsection
def metal2(
    width: float = 0.2,
    layer: LayerSpec = "metal2",
    radius: float | None = None,
) -> CrossSection:
    """Return Metal Strip cross_section."""
    return gf.cross_section.metal1(
        width=width,
        layer=layer,
        radius=radius,
        radius_min=None,
    )


@xsection
def metal3(
    width: float = 0.2,
    layer: LayerSpec = "metal3",
    radius: float | None = None,
) -> CrossSection:
    """Return Metal Strip cross_section."""
    return gf.cross_section.metal1(
        width=width,
        layer=layer,
        radius=radius,
        radius_min=None,
    )


@xsection
def metal4(
    width: float = 0.2,
    layer: LayerSpec = "metal4",
    radius: float | None = None,
) -> CrossSection:
    """Return Metal Strip cross_section."""
    return gf.cross_section.metal1(
        width=width,
        layer=layer,
        radius=radius,
        radius_min=None,
    )


@xsection
def metal5(
    width: float = 0.2,
    layer: LayerSpec = "metal5",
    radius: float | None = None,
) -> CrossSection:
    """Return Metal Strip cross_section."""
    return gf.cross_section.metal1(
        width=width,
        layer=layer,
        radius=radius,
        radius_min=None,
    )


route_bundle = partial(
    gf.routing.route_bundle_electrical, cross_section="metal1", auto_taper=False
)
route_bundle_metal1 = partial(route_bundle, cross_section="metal1")
route_bundle_metal2 = partial(route_bundle, cross_section="metal2")
route_bundle_metal3 = partial(route_bundle, cross_section="metal3")
route_bundle_metal4 = partial(route_bundle, cross_section="metal4")
route_bundle_metal5 = partial(route_bundle, cross_section="metal5")

routing_strategies = dict(
    route_bundle=route_bundle,
    route_bundle_metal1=route_bundle_metal1,
    route_bundle_metal2=route_bundle_metal2,
    route_bundle_metal3=route_bundle_metal3,
    route_bundle_metal4=route_bundle_metal4,
    route_bundle_metal5=route_bundle_metal5,
)


if __name__ == "__main__":
    print(cross_sections.keys())
