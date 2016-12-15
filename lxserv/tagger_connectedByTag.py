#!/usr/bin/env python

# Adapted from James O'Hare's excellent ffr_expandByMat.py code:
# https://gist.github.com/Farfarer/c42ebd249602542a7369b4fd205f4fb5

import lx, lxu.command, lxifc, modo, traceback, tagger

CMD_NAME = tagger.CMD_SELECT_CONNECTED_BY_TAG

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAGTYPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.MATERIAL,
                    'popup': tagger.POPUPS_TAGTYPES,
                    'flags': ['optional']
                }
            ]

    def basic_ButtonName(self):
        if self.commander_arg_value(0):
            label = []
            label.append(tagger.LABEL_SELECT_CONNECTED_BY)
            label.append(tagger.util.i_POLYTAG_to_label(self.commander_arg_value(0)))
            return " ".join(label)

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0)
        i_POLYTAG = tagger.util.string_to_i_POLYTAG(tagType)

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

lx.bless(CommandClass, CMD_NAME)
