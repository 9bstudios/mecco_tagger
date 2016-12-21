# python

import lx, items, modo, scene, util


def tag_polys(polys, ptag, i_POLYTAG=lx.symbol.i_POLYTAG_MATERIAL):
    """Assigns a pTag of type ptyp. Must be used inside a 'with' statement!
    http://modo.sdk.thefoundry.co.uk/td-sdk/guidelines.html#meshediting102

    :param polys: polys to tag
    :param ptag: tag to apply (str)
    :param connected: extend selection to all connected polys (bool)
    :param ptyp: type of tag to apply (str) - e.g. lx.symbol.i_POLYTAG_MATERIAL
    """
    
    # TODO: should be replaced with pyAPI code

    if not ptag:
        ptag = None

    for p in set(polys):
        if i_POLYTAG == lx.symbol.i_POLYTAG_PICK and ptag:
            new_tags = ptag.split(";")

            if p.getTag(i_POLYTAG):
                all_tags = set(p.getTag(i_POLYTAG).split(";"))
            else:
                all_tags = set()

            all_tags.update(new_tags)
            p.setTag(i_POLYTAG,";".join(all_tags))

        else:
            p.setTag(i_POLYTAG,ptag)

    scene.add_pTag_to_recent(ptag, util.i_POLYTAG_to_string(i_POLYTAG))
