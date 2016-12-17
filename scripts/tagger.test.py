#python

import tagger, traceback

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


try:
    lx.eval('!tagger.setMaterial_pTag test random selected material use')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.setMaterial_auto')
    lx.eval('!tagger.setMaterial_auto')
    lx.eval('!tagger.setMaterial_auto')
except:
    lx.out(traceback.print_exc())
    errors += 1

lx.eval('select.contract')
lx.eval('select.contract')
lx.eval('select.contract')
lx.eval('select.contract')
lx.eval('select.contract')
lx.eval('select.contract')
lx.eval('select.contract')

try:
    lx.eval('!tagger.setMaterial_pTag test2 random flood material consolidate')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.setMaterial_pTag test3 random flood material consolidate')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.setMaterial_pTag test4 random connected material consolidate')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.setMaterial_pTagIslands islands material')
except:
    lx.out(traceback.print_exc())
    errors += 1


lx.eval('select.typeFrom item;pivot;center;edge;polygon;vertex;ptag true')


try:
    lx.eval('!tagger.setMaterial_item')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.setMaterial_group material add random')
except:
    lx.out(traceback.print_exc())
    errors += 1


lx.eval('select.typeFrom polygon;edge;vertex;item;pivot;center;ptag true')


try:
    lx.eval('!tagger.floodSelectMaterial')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.floodSelectPart')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.floodSelectPart')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.floodSelectSelectionSet')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.selectAllByMaterial')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.selectAllByPart')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.selectAllBySelectionSet')
except:
    lx.out(traceback.print_exc())
    errors += 1

lx.eval('select.drop polygon')

try:
    lx.eval('!tagger.pTagCopy')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagPasteMaterial flood')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagPastePart flood')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagPasteSelectionSet flood')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagSet material')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagSet material')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagSet part')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagSet pick')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagConvert material part')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagConvert material pick')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagConvert part material')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagConvert part pick')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagConvert pick material')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagConvert pick part')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagReplace material islands_1 islands_3')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagRemoveUnmasked material')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.shaderTree_cleanup true true')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.shaderTree_maskUnmasked material')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagRemoveAll material')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagRemoveAll part')
except:
    lx.out(traceback.print_exc())
    errors += 1

try:
    lx.eval('!tagger.pTagRemoveAll pick')
except:
    lx.out(traceback.print_exc())
    errors += 1


lx.eval('select.typeFrom item;pivot;center;edge;polygon;vertex;ptag true')


try:
    lx.eval('!tagger.setMaterial_itemRemove')
except:
    lx.out(traceback.print_exc())
    errors += 1



if not errors:
    lx.out("Found zero errors. Well done, you. Be sure to check the UI buttons.")

else:
    lx.out("Found %s errors. Get to work." % errors)
