import modo, lx
import util
import re
from debug import *
from var import *

def add_pTag_to_recent(pTag, tagType):
    old_tag = modo.Scene().sceneItem.getTags().get(SCENE_TAG_RECENT)
    if old_tag:
        tags_list = old_tag.split(TAG_SEP)
    else:
        tags_list = []

    tags_list = [TAGTYPE_SEP.join((tagType, pTag))] + tags_list

    # removes duplicates while maintainint list order
    tags_list = [ii for n,ii in enumerate(tags_list) if ii not in tags_list[:n]]

    if len(tags_list) > SCENE_TAG_RECENT_MAX:
        tags_list = tags_list[:SCENE_TAG_RECENT_MAX]

    modo.Scene().sceneItem.setTag(SCENE_TAG_RECENT, TAG_SEP.join(tags_list))

def get_recent_pTags():
    tags = modo.Scene().sceneItem.getTags().get(SCENE_TAG_RECENT)
    if tags:
        tags = tags.split(TAG_SEP)
        tags = [tuple(i.split(TAGTYPE_SEP)) for i in tags]
    return tags

def all_tags_by_type(i_POLYTAG):
    timer = DebugTimer()

    tags = set()
    for m in modo.Scene().meshes:
        n = m.geometry.internalMesh.PTagCount(i_POLYTAG)
        for i in xrange(n):
            tags.add(m.geometry.internalMesh.PTagByIndex(i_POLYTAG, i))

    timer.end()
    return sorted(list(tags))

def all_tags():
    timer = DebugTimer()

    tags = set()

    for m in modo.Scene().meshes:
        for i_POLYTAG in (lx.symbol.i_POLYTAG_MATERIAL, lx.symbol.i_POLYTAG_PICK, lx.symbol.i_POLYTAG_PART):
            n = m.geometry.internalMesh.PTagCount(i_POLYTAG)
            for i in range(n):
                tags.add(m.geometry.internalMesh.PTagByIndex(i_POLYTAG, i))

    timer.end()
    return sorted(list(tags))
def compareRegexp(pattern, str, ignoreCase, regexp):
    if ignoreCase:
        if regexp:
            return re.match(pattern, str, re.IGNORECASE) is not None
        else:
            return pattern.lower() == str.lower()
    else:
        if regexp:
            return re.match(pattern, str) is not None
        else:
            return pattern == str
            
# Replace all leftmost occurrences of 'search' by 'replace'. Function is case sensitive
def replaceStringCase(string, search, replace):
    return string.replace(search, replace)

# Replace all leftmost occurrences of regexp pattern 'search' by 'replace'. Function is case sensitive
def replaceRegexpCase(string, search, replace):
    pattern = re.compile(search)
    return pattern.sub(replace, string)

# Replace all leftmost occurrences of 'search' by 'replace'. Function ignores case
def replaceStringIgnoreCase(string, search, replace):
    # There is no standard Python function for this. Have to implement it.
    idx = 0
    while idx < len(string):
        pos = string.lower().find(search.lower(), idx)
        if pos == -1:
            break
        string = string[:pos] + replace + string[pos + len(search):]
  	idx = pos + len(replace)
    return string

# Replace all leftmost occurrences of regexp pattern 'search' by 'replace'. Function ignores case
def replaceRegexpIgnoreCase(string, search, replace):
    pattern = re.compile(search, re.IGNORECASE)
    return pattern.sub(replace, string)

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

def meshes_with_pTag_Regexp(pTag, i_POLYTAG, ignoreCase, regexp):
    meshes = set()

    for m in modo.Scene().meshes:
        tags = set()
        n = m.geometry.internalMesh.PTagCount(i_POLYTAG)
        for i in range(n):
            tags.add(m.geometry.internalMesh.PTagByIndex(i_POLYTAG, i))
        for tag in tags:
            if compareRegexp(pTag, tag, ignoreCase, regexp):
                meshes.add(m)
                break

    return list(meshes)

def replace_tag(tagType, replaceTag, withTag, ignoreCase, regexp):
    i_POLYTAG = util.convert_to_iPOLYTAG(tagType)
    meshes = meshes_with_pTag_Regexp(replaceTag, i_POLYTAG, ignoreCase, regexp)

    hitcount = 0
    for mesh in meshes:
        with mesh.geometry as geo:
            hitlist = set()
            for poly in geo.polygons:

                if tagType in [MATERIAL, PART]:
                    if compareRegexp(replaceTag, poly.getTag(i_POLYTAG), ignoreCase, regexp):
                        hitlist.add(poly)
                        hitcount += 1

                elif tagType == PICK:
                    if not poly.getTag(i_POLYTAG):
                        continue

                    pickTags = set(poly.getTag(i_POLYTAG).split(";"))
                    for tag in pickTags:
                        if compareRegexp(replaceTag, tag, ignoreCase, regexp):
                            hitlist.add(poly)
                            hitcount += 1
                            break

        # Building replace function based of ignoreCase and regexp flags
        if ignoreCase:
            if regexp:
                replace = replaceRegexpIgnoreCase
            else:
                replace = replaceStringIgnoreCase
        else:
            if regexp:
                replace = replaceRegexpCase
            else:
                replace = replaceStringCase


        with mesh.geometry as geo:
            for poly in hitlist:

                if tagType in [MATERIAL, PART]:
                    poly.setTag(i_POLYTAG, replace(poly.getTag(i_POLYTAG), replaceTag, withTag))

                elif tagType == PICK:
                    pickTags = set(poly.getTag(i_POLYTAG).split(";"))
                    if withTag:
                        newTags = map(lambda tag: replace(tag, replaceTag, withTag) if compare(replaceTag, tag) else tag, pickTags)
                    else:
                        newTags = list()
                        for tag in pickTags:
                            if not compareRegexp(replaceTag, tag):
                                newTags.append(tag)

                    poly.setTag(i_POLYTAG, ";".join(newTags))

    return hitcount
