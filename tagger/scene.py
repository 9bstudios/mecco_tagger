import modo, lx

def all_tags_by_type(i_POLYTAG):
    tags = set()
    for m in modo.Scene().meshes:
        n = m.geometry.internalMesh.PTagCount(i_POLYTAG)
        for i in range(n):
            tags.add(m.geometry.internalMesh.PTagByIndex(i_POLYTAG, i))
    return list(tags)

def all_tags():
    tags = set()
    for i_POLYTAG in (lx.symbol.i_POLYTAG_MATERIAL, lx.symbol.i_POLYTAG_PICK, lx.symbol.i_POLYTAG_PART):
        for m in modo.Scene().meshes:
            n = m.geometry.internalMesh.PTagCount(i_POLYTAG)
            for i in range(n):
                tags.add(m.geometry.internalMesh.PTagByIndex(i_POLYTAG, i))
    return list(tags)

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
