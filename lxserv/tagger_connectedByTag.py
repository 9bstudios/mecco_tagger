#!/usr/bin/env python

# Adapted from James O'Hare's excellent ffr_expandByMat.py code:
# https://gist.github.com/Farfarer/c42ebd249602542a7369b4fd205f4fb5

import lx
import lxu.command
import lxifc
import modo
import traceback
import tagger

CMD_NAME = 'tagger.selectConnectedByTag'

lookup = {
    'material': lx.symbol.i_POLYTAG_MATERIAL,
    'part': lx.symbol.i_POLYTAG_PART,
    'pick': lx.symbol.i_POLYTAG_PICK
}

class sPresetText(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._items)

    def uiv_PopUserName (self, index):
        return self._items[index]

    def uiv_PopInternalName (self, index):
        return self._items[index][0]

class ExpandByMaterial_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__ (self)

        self.dyna_Add ('i_POLYTAG', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Interact(self):
        # Stop modo complaining.
        pass

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def arg_UIValueHints(self, index):
        if index == 0:
            return sPresetText(('material', 'part', 'pick'))

    def arg_UIHints (self, index, hints):
        if index == 0:
            hints.Class ("sPresetText")

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def CMD_EXE(self, msg, flags):
        i_POLYTAG = lookup[self.dyna_String(0)] if self.dyna_IsSet(0) else 'material'

        layer_svc = lx.service.Layer ()
        layer_scan = lx.object.LayerScan (layer_svc.ScanAllocate (lx.symbol.f_LAYERSCAN_ACTIVE | lx.symbol.f_LAYERSCAN_MARKPOLYS))
        if not layer_scan.test ():
            return

        sel_svc = lx.service.Selection ()
        polygon_pkts = []

        mesh_svc = lx.service.Mesh()
        mark_mode_selected = mesh_svc.ModeCompose (lx.symbol.sMARK_SELECT, None)
        mark_mode_valid = mesh_svc.ModeCompose (None, 'hide lock')

        for n in xrange (layer_scan.Count ()):
            mesh = lx.object.Mesh (layer_scan.MeshBase (n))
            if not mesh.test ():
                continue

            polygon_count = mesh.PolygonCount ()
            if polygon_count == 0:
                continue

            polygon = lx.object.Polygon (mesh.PolygonAccessor ())
            if not polygon.test ():
                continue

            edge = lx.object.Edge (mesh.EdgeAccessor ())
            if not edge.test ():
                continue

            visitor = tagger.PolysConnectedByTag (polygon, edge, mark_mode_valid, i_POLYTAG)
            polygon.Enumerate (mark_mode_selected, visitor, 0)

            sel_type_polygon = sel_svc.LookupType (lx.symbol.sSELTYP_POLYGON)
            sel_svc.Drop (sel_type_polygon)
            poly_pkt_trans = lx.object.PolygonPacketTranslation (sel_svc.Allocate (lx.symbol.sSELTYP_POLYGON))
            sel_svc.StartBatch ()
            for polygonID in visitor.getPolyIDs ():
                sel_svc.Select (sel_type_polygon, poly_pkt_trans.Packet (polygonID, mesh))
            sel_svc.EndBatch ()

        layer_scan.Apply ()

lx.bless(ExpandByMaterial_Cmd, CMD_NAME)
