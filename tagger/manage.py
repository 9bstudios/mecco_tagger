# python

import lx, items

def convert_tags(polys, from_i_POLYTAG=lx.symbol.i_POLYTAG_MATERIAL, to_i_POLYTAG=lx.symbol.i_POLYTAG_PICK, replace=False):
    """Converts ptags of one type to another.
    :param polys: polys to convert
    :from_i_POLYTAG: polygon tag type to convert from (e.g. lx.symbol.i_POLYTAG_MATERIAL)
    :to_i_POLYTAG: polygon tag type to convert to (e.g. lx.symbol.i_POLYTAG_PART)
    :param replace: if to_i_POLYTAG is lx.symbol.i_POLYTAG_PICK and this parameter is True,
    the entire pick tag will be overwritten (thus removing all previously-existing selection sets)
    """
    for p in polys:
        tag = "-".join(p.getTag(from_i_POLYTAG).split(";")) if p.getTag(from_i_POLYTAG) else None
        tag_polys([p], tag, False, to_i_POLYTAG, replace)
        tag_polys([p], None, False, from_i_POLYTAG, True)

    mm = items.get_active_layers()
    for m in mm:
        m.geometry.setMeshEdits()

def tag_polys(polys,ptag,connected=False,i_POLYTAG=lx.symbol.i_POLYTAG_MATERIAL,replace=False):
    """Assigns a pTag of type ptyp to all selected polys in all active layers.

    :param polys: polys to tag
    :param ptag: tag to apply (str)
    :param connected: extend selection to all connected polys (bool)
    :param ptyp: type of tag to apply (str) - e.g. lx.symbol.i_POLYTAG_MATERIAL
    :param replace: replace existing tag (as opposed to appending, pick tags only)
    """

    if not polys:
        return False

    for p in polys:
        if i_POLYTAG == lx.symbol.i_POLYTAG_PICK and not replace:
            tags = p.getTag(i_POLYTAG).split(";")
            if not ptag in tags:
                tags.append(ptag)
            p.setTag(i_POLYTAG,";".join(tags))
        else:
            p.setTag(i_POLYTAG,ptag)

    mm = items.get_active_layers()
    for m in mm:
        m.geometry.setMeshEdits()

    return True
