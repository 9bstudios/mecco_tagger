#python

import tagger

errors = 0

lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')

def open_scene(slug):
    scenesFolder = lx.eval("query platformservice alias ? {kit_mecco_tagger:testing}")

    lx.eval("pref.value application.defaultScene {%s/%s.lxo}" % (scenesFolder,slug))
    lx.eval("scene.new")
    lx.eval("pref.value application.defaultScene {}")

lx.eval('scene.closeAll')
open_scene('testScene')

lx.eval('select.drop item')
lx.eval('select.drop channel')
lx.eval('select.subItem Cube set')

lx.eval('select.polygon add material face m1')
polys = tagger.selection.get_polys()

# Set Material

lx.eval('tagger.setMaterial test1')
for p in polys:
    if p.tags()['material'] != 'test1':
        lx.out('tagger.setMaterial - failed')
        errors += 1
        break

lx.eval('tagger.setMaterial {} auto remove')
for p in polys:
    if p.tags()['material']:
        lx.out('tagger.setMaterial {} auto remove - failed')
        errors += 1
        break

# Convert Tags

lx.eval('tagger.pTagConvert part material')
for p in polys:
    if p.tags()['part'] or p.tags()['material'] != 'p3':
        lx.out('tagger.pTagConvert part material - failed')
        errors += 1
        break

lx.eval('tagger.pTagConvert material part')
for p in polys:
    if p.tags()['material'] or p.tags()['part'] != 'p3':
        lx.out('tagger.pTagConvert material part - failed')
        errors += 1
        break

lx.eval('tagger.pTagConvert part pick')
for p in polys:
    if p.tags()['part'] or 'p3' not in p.tags()['pick'].split(";"):
        lx.out('tagger.pTagConvert part pick - failed')
        errors += 1
        break

lx.eval('tagger.pTagConvert pick part')
for p in polys:
    if p.tags()['pick'] or 'p3' not in p.tags()['part'].split('-'):
        lx.out("Got " + str(p.tags()['part']) + ", expected p3")
        lx.out('tagger.pTagConvert pick part - failed')
        errors += 1
        break

# pTag Set

lx.eval('tagger.pTagSet part')
for p in polys:
    if p.tags()['part'] != None:
        lx.out('tagger.pTagSet part - failed')
        errors += 1
        break

lx.eval('tagger.pTagSet pick')
for p in polys:
    if p.tags()['pick'] != None:
        lx.out('tagger.pTagSet pick - failed')
        errors += 1
        break

lx.eval('tagger.setMaterial test1')
lx.eval('tagger.pTagSet material')
for p in polys:
    if p.tags()['material'] != None:
        lx.out('tagger.pTagSet material - failed')
        errors += 1
        break


# pTag Clipboard
# Copy and paste material tags using connected:0, 1, and 2.
# Test to ensure that all of the proper tags were applied.


# pTag Replace
# Replace a tag globally in the file.
# Test to ensure that the tag is gone from the scene.


# pTag Select All By Tag
# Run the command to make sure no errors are thrown. Do not test.


# pTag Tag With Masked
# Tag a polygon selection with a mask selection.
# Test to ensure that the proper tag was applied.


# pTag Connected By Tag
# Run the command to make sure no errors are thrown. Do not test.


# pTag Remove All
# Remove a given tag type from the scene entirely. (e.g. remove all part tags)
# Test to ensure that all polys in scene are tagged "None" for the given tag type.



if not errors:
    lx.out("Found zero errors. Well done, you. Be sure to check the UI buttons.")

else:
    lx.out("Found %s errors. Get to work." % errors)
