#python

from lx import symbol

DEFAULT_PTAG = symbol.i_POLYTAG_MATERIAL
DEFAULT_RANDOM_COLOR_SATURATION = .7
DEFAULT_RANDOM_COLOR_VALUE = .95
DEFAULT_MATERIAL_NAME = 'material'
DEFAULT_GROUP_NAME = 'tagger_group'

CMD_SET_MATERIAL = 'tagger.setMaterial_auto'
CMD_REMOVE_MATERIAL = 'tagger.removeMaterial_auto'
CMD_SET_PTAG = 'tagger.setMaterial_pTag'
CMD_REMOVE_PTAG = 'tagger.removeMaterial_pTag'
CMD_SET_ITEM = 'tagger.setMaterial_item'
CMD_SET_GROUP = 'tagger.setMaterial_group'
CMD_SELECT_CONNECTED_BY_TAG = 'tagger.selectConnectedByTag'
CMD_PTAG_SET = 'tagger.pTagSet'
CMD_PTAG_CLIPBOARD = 'tagger.pTagClipboard'
CMD_PTAG_INSPECT = 'tagger.pTagInspect'
CMD_PTAG_REMOVEALL = 'tagger.pTagRemoveAll'
CMD_PTAG_REPLACE = 'tagger.pTagReplace'
CMD_PTAG_SELECTION_FCL = 'tagger.pTagSelectionFCL'
CMD_SELECT_ALL_BY_TAG = 'tagger.selectAllByTag'
CMD_TAG_WITH_MASKED = 'tagger.tagWithMasked'

GROUPNAME = "group"
MATNAME = "material"
SHADERNAME = "shader"

GTYP = "GTYP"

GROUP_TYPES_STANDARD = ''
GROUP_TYPES_ASSEMBLY = 'assembly'

NAME = 'name'
MODE = 'mode'
OPERATION = 'operation'
CONNECTED = 'connected'
REMOVE_SCOPE = 'scope'
PRESET = 'preset'
TAGTYPE = 'tagType'
COPY = 'copy'
PASTE = 'paste'
MATERIAL = 'material'
PICK = 'pick'
PART = 'part'
TAG = 'tag'
i_POLYTAG = 'i_POLYTAG'
MASK = 'mask'
COPYMASK = 'copyMask'
REPLACETAG = 'replaceTag'
WITHTAG = 'withTag'
QUERY = 'query'
RANDOM = 'random'
DELETE_UNUSED_MASKS = 'delete_unused'
WITH_EXISTING = 'withExisting'
GET_MORE_PRESETS = 'getMorePresets'
GET_MORE_PRESETS_URL = 'http://www.mechanicalcolor.com/coming-soon'
OPERATION = 'operation'
REMOVE = 'remove'
ADD = 'add'
USE = 'use'
KEEP = 'keep'
REMOVE = 'remove'
CONSOLIDATE = 'consolidate'
SCOPE_SELECTED = 0
SCOPE_CONNECTED = 1
SCOPE_FLOOD = 2
SCOPE_SCENE = 3

# These should probably be pulled from message tables
LABEL_MODE = "Mode"
LABEL_TAGTYPE = "Tag Type"
LABEL_TAG = "Tag"
LABEL_TAGS = "Tags"
LABEL_PRESET = "Preset"
LABEL_CONNECTED = "Connected"
LABEL_REMOVE_SCOPE = "Remove From"
LABEL_NONE = "(none)"
LABEL_REPLACE_TAG = "Replace Tag"
LABEL_WITH_TAG = "With Tag"
LABEL_RANDOM_COLOR = "Random Color"
LABEL_GET_MORE_PRESETS = "Get more presets..."
LABEL_WITH_EXISTING = "With Existing"
LABEL_DELETE_UNUSED_MASKS = "Cleanup unused masks"
LABEL_OPERATION = "Operation"
LABEL_GROUP_NAME = "Group Name"
LABEL_TAG_WITH_MASKED = "Tag With Masked"
LABEL_MATERIAL = "Material"
LABEL_PART = "Part"
LABEL_PICK = "Selection Set"
LABEL_SCOPE_SELECTED = 'Selected Polys'
LABEL_SCOPE_CONNECTED = 'Connected Polys'
LABEL_SCOPE_FLOOD = 'Flood Polys'
LABEL_SCOPE_SCENE = 'Entire Scene'
LABEL_USE = 'Use'
LABEL_KEEP = 'Keep and add'
LABEL_REMOVE = 'Remove and add'
LABEL_CONSOLIDATE = 'Consolidate and add'
LABEL_FROM_TAGTYPE = 'From Tag Type'
LABEL_TO_TAGTYPE = 'To Tag Type'
LABEL_COPY = 'Copy'
LABEL_PASTE = 'Paste'
DIALOGS_NO_MASK_SELECTED = ("No Mask Selected", "Select a mask to apply.")
DIALOGS_TOO_MANY_MASKS = ("Too Many Masks", "Select only one mask to apply.")
DIALOGS_NO_PTAG_FILTER = ("No pTag Filter", "The selected mask applies to all polygons. No tag to apply.")
DIALOGS_NONE_PTAG_FILTER = ("(none) pTag Filter", "The selected mask applies to nothing. No tag to apply.")

POPUPS_CLIPBOARD = [
        (COPY, LABEL_COPY),
        (PASTE, LABEL_PASTE)
    ]

POPUPS_CONNECTED = [
        (SCOPE_SELECTED, LABEL_SCOPE_SELECTED),
        (SCOPE_CONNECTED, LABEL_SCOPE_CONNECTED),
        (SCOPE_FLOOD, LABEL_SCOPE_FLOOD)
    ]

POPUPS_REMOVE_SCOPE = [
        (SCOPE_SELECTED, LABEL_SCOPE_SELECTED),
        (SCOPE_CONNECTED, LABEL_SCOPE_CONNECTED),
        (SCOPE_FLOOD, LABEL_SCOPE_FLOOD),
        (SCOPE_SCENE, LABEL_SCOPE_SCENE)
    ]

POPUPS_TAGTYPES = [
        (MATERIAL, LABEL_MATERIAL),
        (PART, LABEL_PART),
        (PICK, LABEL_PICK)
    ]

POPUPS_WITH_EXISTING = [
        (USE, LABEL_USE),
        (KEEP, LABEL_KEEP),
        (REMOVE, LABEL_REMOVE),
        (CONSOLIDATE, LABEL_CONSOLIDATE)
    ]

POPUPS_ADD_REMOVE = [(ADD, ADD.title()), (REMOVE, REMOVE.title())]

OPERATIONS_ADD = ADD
OPERATIONS_REMOVE = REMOVE
