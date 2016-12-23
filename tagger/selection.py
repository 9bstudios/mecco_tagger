#python

import modo, lx, items, manage
from PolysConnectedByTag import *
from var import *


def get_mode():
    """Returns the current selection mode as any of the following strings:
    vertex;edge;polygon;item;pivot;center;ptag
    """

    modes = 'vertex;edge;polygon;item;pivot;center;ptag'
    for mode in modes.split(';'):
        if lx.eval('select.typeFrom %s;%s ?' % (mode, modes)):
            return mode
    return False


def get_polys(connected=SCOPE_SELECTED):
    """Returns a list of all implicitly selected polys in all active layers.
    If in poly mode, returns selected polys. If in edge or vertex mode,
    returns all polys adjacent to all selected components.

    :param connected: If True, returns all polys connected to the selection."""

    result = set()
    scene = modo.scene.current()

    for layer in items.get_active_layers():

        if get_mode() == 'polygon':
            if layer.geometry.polygons.selected:
                for p in layer.geometry.polygons.selected:
                    result.add(p)
            else:
                for p in layer.geometry.polygons:
                    result.add(p)
        elif get_mode() == 'edge':
            if layer.geometry.edges.selected:
                for e in layer.geometry.edges.selected:
                    for p in e.polygons:
                        result.add(p)
            else:
                for p in layer.geometry.polygons:
                    result.add(p)
        elif get_mode() == 'vertex':
            if layer.geometry.edges.selected:
                for v in layer.geometry.vertices.selected:
                    for p in v.polygons:
                        result.add(p)
            else:
                for p in layer.geometry.polygons:
                    result.add(p)

        elif get_mode() == 'ptag':
            return []
        else:
            return []

        if connected == SCOPE_CONNECTED:
            result = island(result)
        elif connected == SCOPE_FLOOD:
            result = flood(result)

    return list(result)

def get_ptags(i_POLYTAG = lx.symbol.i_POLYTAG_MATERIAL,connected=SCOPE_SELECTED):
    """Returns a list of all pTags for currently selected polys in all active layers.

    :param i_POLYTAG: type of tag to return (str), e.g. lx.symbol.i_POLYTAG_MATERIAL
    :param connected: extend selection to connected polys (bool)
    """

    r = set()
    pp = get_polys(connected)
    if pp:
        for p in pp:
            tags = set(p.getTag(i_POLYTAG).split(";"))
            r.update(tags)
    return list(r)



def convert_tags(from_i_POLYTAG=lx.symbol.i_POLYTAG_MATERIAL, to_i_POLYTAG=lx.symbol.i_POLYTAG_PICK, connected=SCOPE_SELECTED):
    """Converts ptags of one type to another.
    :param from_i_POLYTAG: polygon tag type to convert from (e.g. lx.symbol.i_POLYTAG_MATERIAL)
    :param to_i_POLYTAG: polygon tag type to convert to (e.g. lx.symbol.i_POLYTAG_PART)
    :param connected: extend selections to convert poly islands
    """

    for layer in items.get_active_layers():
        with layer.geometry as geo:
            polys = geo.polygons.selected

            if connected == SCOPE_CONNECTED:
                polys = island(polys)
            if connected == SCOPE_FLOOD:
                polys = flood(polys)

            for p in polys:
                if p.getTag(from_i_POLYTAG):
                    tag = "-".join(p.getTag(from_i_POLYTAG).split(";")) if p.getTag(from_i_POLYTAG) else ''
                else:
                    tag = ''

                manage.tag_polys([p], tag, to_i_POLYTAG)

        with layer.geometry as geo:
            polys = geo.polygons.selected
            if connected:
                polys = island(polys)

            for p in polys:
                manage.tag_polys([p], '', from_i_POLYTAG)



def island(seed_polys):
    polyIsland = set()
    checked = set()
    toCheck = set()

    for poly in seed_polys:

        if poly in polyIsland:
            continue

        polyIsland.add( poly )
        checked.add( poly )
        toCheck.add( poly )

        while toCheck:
            poly = toCheck.pop()
            for polyN in poly.neighbours:
                if not polyN in checked:
                    checked.add( polyN )
                    if not polyN in polyIsland:
                        polyIsland.add( polyN )
                        toCheck.add( polyN )

    return polyIsland


def flood(seed_polys, i_POLYTAG):
    seed_polys = set(seed_polys)

    polyIsland = set()
    checked = set()
    toCheck = set()

    for poly in seed_polys:
        tag = poly.getTag(i_POLYTAG)
        if not tag:
            return island(seed_polys)

        tags = set(tag.split(";"))
        if not tags:
            return island(seed_polys)

        if poly in polyIsland:
            continue

        polyIsland.add( poly )
        checked.add( poly )
        toCheck.add( poly )

        while toCheck:
            poly = toCheck.pop()

            for polyN in poly.neighbours:
                if not tags.intersection(set(polyN.getTag(i_POLYTAG).split(";"))):
                    continue
                if not polyN in checked:
                    checked.add( polyN )
                    if not polyN in polyIsland:
                        polyIsland.add( polyN )
                        toCheck.add( polyN )

    return polyIsland



def expand_by_pTag(polys=set(), pTagKey='material', pTags=set(), ignore=set()):
    """Expands current poly selection to include all contiguous polys with a given
    set of pTags. Returns set() of selected polys. If no pTags are provided, uses
    tags of the provided pTagKey on the provided polys.

    :param polys: set of TD polygons to expand
    :param pTagKey: "material", "part", or "pick"
    :param pTags: (optional) set of tags for which to search
    :param ignore: (for recursion) set of polygons that have already been ruled out
    """

    polys = set([i for i in polys if pTagKey in i.tags()])
    polys = set([i for i in polys if i.tags()[pTagKey] is not None])

    if not pTags:
        for p in polys:
            pTags = pTags.union(p.tags()[pTagKey].split(";"))

    to_check = set()

    for p in polys:
        to_check = to_check.union(set(p.neighbours))

    to_check = to_check.difference(ignore)
    to_check = set([i for i in to_check if pTagKey in i.tags()])
    to_check = set([i for i in to_check if i.tags()[pTagKey] is not None])
    to_check = set([i for i in to_check if [t for t in pTags if t in i.tags()[pTagKey].split(";")]])

    if not to_check:
        return False

    for p in to_check:
        p.select()

    ignore = ignore.union(to_check)
    expand_by_pTag(to_check, pTagKey, pTags, ignore)

    return True
