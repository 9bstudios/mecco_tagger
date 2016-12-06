#python

import modo, lx, lxu, defaults, selection

def group_selected_and_maskable(name):
    scene = modo.Scene()

    group = scene.addItem(lx.symbol.sITYPE_GROUP)
    group.name = name
    group.addItems(get_selected_and_maskable())

    return group



def get_groups(items=[]):
    """Returns a list of items of type lx.symbol.sITYPE_GROUP. If a list of items is supplied,
    resulting list will only return groups containing any of the supplied items."""

    scene = modo.Scene()
    groups = set()

    if len(items) == 0:
        return scene.iterItems(lx.symbol.sITYPE_GROUP)

    for group in scene.iterItems(lx.symbol.sITYPE_GROUP):
        if [i for i in items if i in group.items]:
            groups.add(group)

    return list(groups)


def ptag_replace(layers,pTags,default = defaults.get('ptag'),i_POLYTAG = lx.symbol.i_POLYTAG_MATERIAL):
    """Replaces all instances of supplied pTag(s) in suplied layer(s) with a default tag.

    :param layers: modo.item.Item() object or list of objects to search
    :param pTags: string or list of strings for which to search
    :param default: string with which to replace matching pTags (optional)
    """

    if not isinstance(layers,list):
        layers = [layers]

    if not isinstance(pTags,list):
        pTags = [pTags]

    for layer in layers:
        for p in layer.geometry.polygons:
            if i_POLYTAG == lx.symbol.i_POLYTAG_PICK:
                tags = p.getTag(i_POLYTAG).split(";")
                if not ptag in tags:
                    tags.append(ptag)
                p.setTag(i_POLYTAG,";".join(tags))
            else:
                p.setTag(i_POLYTAG,ptag)


def get_layers_by_pTag(pTags,i_POLYTAG=lx.symbol.i_POLYTAG_MATERIAL):
    """Returns a list of all mesh layers containing any of the provided pTag(s)
    of type i_POLYTAG, e.g. lx.symbol.i_POLYTAG_MATERIAL.
    """

    if not isinstance(pTags,list):
        pTags = [pTags]

    scene = modo.Scene()

    mm = set()
    for m in scene.meshes:
        for i in range(m.geometry.internalMesh.PTagCount(i_POLYTAG)):
            tag = m.geometry.internalMesh.PTagByIndex(i_POLYTAG,i)
            if i_POLYTAG == lx.symbol.i_POLYTAG_PICK:
                if [i for i in tag.split(";") if i in pTags]:
                    mm.add(m)
            else:
                if tag in pTags:
                    mm.add(m)

    return list(mm)


def get_active_layers():
    """Returns a list of all currently active mesh layers (regardless of selection state)."""

    lyr_svc = lx.service.Layer ()
    scan = lx.object.LayerScan (lyr_svc.ScanAllocate (lx.symbol.f_LAYERSCAN_ACTIVE))
    itemCount = scan.Count ()
    if itemCount > 0:
            items = [modo.Mesh( scan.MeshItem(i) ) for i in range(itemCount)]
    scan.Apply ()

    return items



def get_all_masked_tags():
    """see https://gist.github.com/mattcox/6147502"""
    ptags = set()

    lookup = {
        'Material': 'material',
        'Part': 'part',
        'Selection Set': 'pick'
    }

    scn_svc = lx.service.Scene()
    scene = lxu.select.SceneSelection().current()

    chan_read = scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, 0.0)
    mask_type = scn_svc.ItemTypeLookup(lx.symbol.sITYPE_MASK)

    for i in range (scene.ItemCount(mask_type)):
        mask = scene.ItemByIndex(mask_type, i)

        tagType = lookup[chan_read.String(mask, mask.ChannelLookup(lx.symbol.sICHAN_MASK_PTYP))]
        tag = chan_read.String(mask, mask.ChannelLookup(lx.symbol.sICHAN_MASK_PTAG))
        ptags.add((tagType, tag))

    return list(ptags)



def get_selected_and_maskable():
    """Returns a list of object(s) that can be masked."""

    items = modo.Scene().selected

    r = set()
    for item in items:
        if test_maskable(item):
            r.add(item)

    r = list(r)

    return r


def test_maskable(items):

    """Returns True if an item or items can be masked by shader tree masks.
    e.g. Mesh items return True, Camera items return False

    :param items: item(s) to test for maskability
    :type items: object or list of objects
    """

    if not isinstance(items,list):
        items = [items]

    hst_svc = lx.service.Host ()
    scn_svc = lx.service.Scene ()
    hst_svc.SpawnForTagsOnly ()

    r = list()
    for item in items:
        if item.isLocatorSuperType():
            item = item.internalItem

            type = scn_svc.ItemTypeName (item.Type ())

            factory = hst_svc.LookupServer (lx.symbol.u_PACKAGE, type, 1)

            for i in range (factory.TagCount ()):
                if (factory.TagByIndex (i)[0]== lx.symbol.sPKG_IS_MASK):
                    r.append(True)
                else:
                    r.append(False)
        else:
            r.append(False)

    if len(r) == 1:
        return r[0]
    return r
