#python

import modo, lx, util, items
from var import *

def do_preset(preset_path):
    """Drops a material preset, deletes the cruft, and returns the good stuff."""

    lx.eval('preset.do {%s}' % preset_path)

    preset_group = modo.Scene().groups[-1]
    preset_parent_mask = preset_group.itemGraph('itemGroups').forward()[0]
    preset_contents = preset_parent_mask.children()

    modo.Scene().removeItems(preset_parent_mask)
    modo.Scene().removeItems(preset_group)

    if len(preset_contents) == 1 and preset_contents[0].type == 'mask':
        parent_mask = preset_contents[0]
        preset_contents = parent_mask.children()
        modo.Scene().removeItems(parent_mask)

    return preset_contents

def build_material(
        item = None,
        i_POLYTAG = lx.symbol.i_POLYTAG_MATERIAL,
        pTag = None,
        parent = None,
        name = None,
        preset=None,
        shader=False
        ):

    """Builds a material in the shader tree, including a mask, material, and shader with default settings.

    :param item: item for mask to filter (optional)
    :type item: modo.item.Item() object

    :param i_POLYTAG: lx.symbol.i_POLYTAG_* (optional)
    :type i_POLYTAG: int

    :param pTag: pTag string (optional)
    :type pTag: str

    :param parent: parent (optional)
    :type parent: modo.item.Item() object

    :param name: name (optional)
    :type name: str

    :param preset: path to modo preset file (.lxp)
    :type preset: str

    :param shader: include shader in material group
    :type shader: bool
    """

    scene = modo.Scene()

    color = util.random_color()

    mask = add_mask(
        item,
        i_POLYTAG,
        pTag,
        parent,
        name
    )

    if parent:
        parent = get_masks(names = parent)[0]
        if parent:
            mask.setParent(parent,parent.childCount())

    if preset:
        preset_contents = do_preset(preset)
        for i in preset_contents:
            i.setParent(mask)

    elif not preset:
        if(shader):
            sname = ' '.join([name,SHADERNAME]) if name else None
            shdr = add_shader(sname)
            shdr.setParent(mask)

        mname = ' '.join([name,MATNAME]) if name else None
        channels = {lx.symbol.sICHAN_ADVANCEDMATERIAL_DIFFCOL:color}
        mat = add_material(mname,channels)
        mat.setParent(mask)

    if [i for i in mask.children() if i.type == 'defaultShader']:
        move_to_base_shader(mask, True)
    else:
        move_to_base_shader(mask, False)

    return mask



def add_mask(
    item = None,
    i_POLYTAG = lx.symbol.i_POLYTAG_MATERIAL,
    pTag = None,
    parent = None,
    name = None
    ):

    """Add a Mask to the Shader Tree.

    :param item: item for mask to filter (optional)
    :type item: modo.item.Item() object

    :param i_POLYTAG: lx.symbol.i_POLYTAG_* (optional)
    :type i_POLYTAG: int

    :param pTag: pTag string (optional)
    :type pTag: str

    :param parent: parent (optional)
    :type parent: modo.item.Item() object

    :param name: name (optional)
    :type name: str
    """

    scene = modo.Scene()
    mask = scene.addItem(lx.symbol.sITYPE_MASK)

    if item:
        sg = scene.GraphLookup('shadeLoc')
        ig = lx.object.ItemGraph(sg)
        ig.AddLink(mask,item)

    if i_POLYTAG:
        mask.channel(lx.symbol.sICHAN_MASK_PTYP).set(sICHAN_MASK_PTYP(i_POLYTAG))

    if pTag:
        mask.channel(lx.symbol.sICHAN_MASK_PTAG).set(pTag)

    if not parent:
        parent = scene.renderItem
    elif get_masks(names=parent):
        mask.setParent(parent)

    mask.name = name if name else None

    return mask




def add_material(name=None,channels={}):
    """Adds a material item to the Shader Tree and sets channel values based on an optional dict."""

    scene = modo.scene.current()
    m = scene.addItem(lx.symbol.sITYPE_ADVANCEDMATERIAL, name)
    for k,v in channels.iteritems():
        m.channel(k).set(v)
    return m



def add_shader(name=None,channels={}):
    """Adds a shader item to the Shader Tree and sets channel values based on an optional dict."""

    scene = modo.scene.current()
    m = scene.addItem(lx.symbol.sITYPE_DEFAULTSHADER, name)
    for k,v in channels.iteritems():
        m.channel(k).set(v)
    return m



def seek_and_destroy(
    maskedItems = [],
    pTags = {},
    names = []
    ):

    """Remove all Shader Tree masks and eliminate pTags matching any of the provided criteria.

    :param maskedItems: remove item masks filtering any of the listed items
    :type maskedItems: list of modo.item.Item() objects

    :param pTags: remove masks filtering any of the "pTag":"i_POLYTAG" pairs
    :type pTags: dict of "pTag":lx.symbol.i_POLYTAG_* pairs
    """

    if not isinstance(maskedItems,list):
        maskedItems = [maskedItems]

    if not isinstance(names,list):
        names = [names]

    scene = modo.scene.current()

    if len(pTags) > 0:
        for m in scene.meshes:
            for p in m.geometry.polygons:
                for pTag, i_POLYTAG in pTags.iteritems():
                    if i_POLYTAG == lx.symbol.i_POLYTAG_PICK:
                        tags = p.getTag(i_POLYTAG).split(";")
                        tags.remove(pTag)
                        p.setTag(i_POLYTAG,";".join(tags))
                    else:
                        if p.getTag(i_POLYTAG) == pTag:
                            p.setTag(i_POLYTAG, DEFAULT_PTAG)

    for i in get_masks(maskedItems,pTags,names):
        scene.removeItems(i,True)







def get_masks(
    maskedItems = [],
    pTags = {},
    names = []
    ):

    """Returns a list of all lx.symbol.sITYPE_MASK items given any of the provided criteria.

    :param maskedItems: items for which to find masks
    :type maskedItems: list of modo.item.Item() objects

    :param pTags: ptags for which to find masks
    :type pTags: dict of "pTag":lx.symbol.i_POLYTAG_* pairs

    :param names: UniqueNames for which to find masks
    :type names: list of strings to match with modo.item.Item().UniqueName()
    """

    if not isinstance(maskedItems,list):
        maskedItems = [maskedItems]

    if not isinstance(names,list):
        names = [names]

    scene = modo.Scene()

    r = set()
    for m in scene.iterItems(lx.symbol.sITYPE_MASK):
        maskedItem = get_masked_items(m)
        if maskedItem:
            if maskedItem in maskedItems:
                r.add(m)

        for pTag, pTyp in pTags.iteritems():
            if (
                m.channel(lx.symbol.sICHAN_MASK_PTYP).get() == sICHAN_MASK_PTYP(pTyp)
                and m.channel(lx.symbol.sICHAN_MASK_PTAG).get() == pTag
                ):

                r.add(m)

        if m.UniqueName() in names:
            r.add(m)

    return list(r)







def get_masked_items(
    masks=[]
    ):
    """Returns modo.item.Item() object(s) masked by the provided lx.symbol.sITYPE_MASK object(s).

    :param masks: mask objects for whom to list masked objects
    :type masks: object or list of objects
    """

    if not isinstance(masks,list):
        masks = [masks]

    sg = modo.Scene().GraphLookup('shadeLoc')
    ig = lx.object.ItemGraph(sg)

    r = set()
    for mask in masks:
        if ig.FwdCount(mask) > 0:
            r.add (modo.item.Item(ig.FwdByIndex(mask,0)))

    r = list(r)

    if len(r) == 1:
        return r[0]

    return r






def move_to_top(items):
    """Moves the supplied items to the top slot in their respective parents."""

    if not isinstance(items,list):
        items = [items]

    for item in items:
        item.setParent(item.parent,item.parent.childCount())




def get_shaders(mask):
    """Return a list of all shaders anywhere inside the supplied mask item."""

    shaders = set()
    for i in mask.children(True):
        if i.type == lx.symbol.sITYPE_DEFAULTSHADER:
            shaders.add(i)

    return list(shaders)

def move_to_base_shader(items, above_base_shader=False):
    """Places supplied item(s) above or below Base Shader as appropriate.

    :param items: Item(s) to re-order
    :type items: modo.item.Item() object or list of the same

    :param above_base_shader: True if index should be above Base Shader (default: False)
    :type above_base_shader: bool"""

    if not isinstance(items,list):
        items = [items]

    for n, i in enumerate(modo.Scene().renderItem.children()):
    	if i.type == 'defaultShader':
    		target_index = n - 1

    if above_base_shader:
    	for n, i in enumerate(modo.Scene().renderItem.children()):
    		print n, i.name
    		if i.type == 'mask':
    			target_index = n if n > target_index else target_index + 1

    for item in items:
        item.setParent(modo.Scene().renderItem, target_index)
        return target_index
