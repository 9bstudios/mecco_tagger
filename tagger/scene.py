import modo, lx
import util
from var import *

def all_tags_by_type(i_POLYTAG):
    tags = set()
    for m in modo.Scene().meshes:
        n = m.geometry.internalMesh.PTagCount(i_POLYTAG)
        for i in range(n):
            tags.add(m.geometry.internalMesh.PTagByIndex(i_POLYTAG, i))
    return sorted(list(tags))

def all_tags():
    tags = set()
    for i_POLYTAG in (lx.symbol.i_POLYTAG_MATERIAL, lx.symbol.i_POLYTAG_PICK, lx.symbol.i_POLYTAG_PART):
        for m in modo.Scene().meshes:
            n = m.geometry.internalMesh.PTagCount(i_POLYTAG)
            for i in range(n):
                tags.add(m.geometry.internalMesh.PTagByIndex(i_POLYTAG, i))
    return sorted(list(tags))

def meshes_with_pTag(pTag, i_POLYTAG):
    meshes = set()

    for m in modo.Scene().meshes:
        tags = set()
        n = m.geometry.internalMesh.PTagCount(i_POLYTAG)
        for i in range(n):
            tags.add(m.geometry.internalMesh.PTagByIndex(i_POLYTAG, i))
        if pTag in tags:
            meshes.add(m)

    return list(meshes)

def replace_tag(tagType, replaceTag, withTag):
    i_POLYTAG = util.string_to_i_POLYTAG(tagType)
    meshes = meshes_with_pTag(replaceTag, i_POLYTAG)

    hitcount = 0
    for mesh in meshes:
        with mesh.geometry as geo:
            hitlist = set()
            for poly in geo.polygons:

                if tagType in [MATERIAL, PART]:
                    if poly.getTag(i_POLYTAG) == replaceTag:
                        hitlist.add(poly)
                        hitcount += 1

                elif tagType == PICK:
                    if not poly.getTag(i_POLYTAG):
                        continue

                    pickTags = set(poly.getTag(i_POLYTAG).split(";"))
                    if replaceTag in pickTags:
                        hitlist.add(poly)
                        hitcount += 1


        with mesh.geometry as geo:
            for poly in hitlist:

                if tagType in [MATERIAL, PART]:
                    poly.setTag(i_POLYTAG, withTag)

                elif tagType == PICK:
                    pickTags = set(poly.getTag(i_POLYTAG).split(";"))
                    pickTags.discard(replaceTag)
                    if withTag:
                        pickTags.add(withTag)
                    poly.setTag(i_POLYTAG, ";".join(pickTags))

    return hitcount
