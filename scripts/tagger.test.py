#python

lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true')
lx.eval('layout.createOrClose passify_testify "passify_testify" title:Test width:800 height:400 persistent:true')

def open_scene(slug):
    scenesFolder = lx.eval("query platformservice alias ? {kit_mecco_tagger:testing}")

    lx.eval("pref.value application.defaultScene {%s/%s.lxo}" % (scenesFolder,slug))
    lx.eval("scene.new")
    lx.eval("pref.value application.defaultScene {}")

open_scene('testScene')

lx.eval('select.drop item')
lx.eval('select.drop channel')
lx.eval('select.subItem mesh021 set mesh')

lx.eval('select.polygon add material face m1')
polys = tagger.selection.get_polys()

lx.eval('tagger.setMaterial test1')
for p in polys:
    if p.tags()['material'] != 'test1':
        lx.out('tagger.setMaterial - failed')

lx.eval('tagger.setMaterial {} auto remove')
for p in polys:
    if p.tags()['material'] != None:
        lx.out('tagger.setMaterial {} auto remove - failed')

lx.eval('tagger.convertTags part material')
for p in polys:
    if p.tags()['part'] != None or p.tags()['material'] != p3:
        lx.out('tagger.convertTags part material - failed')

lx.eval('tagger.removeTag part')
lx.eval('tagger.removeTag pick')
lx.eval('tagger.removeTag material')
