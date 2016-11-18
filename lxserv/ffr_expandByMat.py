# Run with `ffr.expandByMat`, it will expand the current polygon selection by the material ID of the current polygon selection.
#
# An optional argument, `materialID` will expand only by a given material ID, e.g.
# `ffr.expandByMat "Default"`

#!/usr/bin/env python

import lx
import lxu.command
import lxifc
import time

class PolysConnectedByMat (lxifc.Visitor):
	def __init__ (self, polygon, edge, mark_mode_valid, materialID=None):
		self.polygon = polygon
		self.edge = edge
		self.mark_mode_valid = mark_mode_valid

		self.polygonIDs = set ()

		self.tag = lx.object.StringTag ()
		self.tag.set (self.polygon)

		self.materialID = materialID

	def reset (self):
		self.polygonIDs = set ()

	def getPolyIDs (self):
		return self.polygonIDs

	def vis_Evaluate (self):
		inner_list = set ()
		outer_list = set ()

		this_polygon_ID = self.polygon.ID ()

		if self.materialID is None:
			materialID = self.tag.Get (lx.symbol.i_PTAG_MATR)
		else:
			materialID = self.materialID

		if this_polygon_ID not in outer_list:

			outer_list.add (this_polygon_ID)

			while len(outer_list) > 0:
				polygon_ID = outer_list.pop ()

				self.polygon.Select (polygon_ID)

				inner_list.add (polygon_ID)

				num_points = self.polygon.VertexCount ()

				polygon_points = [self.polygon.VertexByIndex (p) for p in xrange (num_points)]

				for p in xrange (num_points):
					self.edge.SelectEndpoints (polygon_points[p], polygon_points[(p+1)%num_points])
					if self.edge.test ():
						for e in xrange (self.edge.PolygonCount ()):
							edge_polygon_ID = self.edge.PolygonByIndex (e)
							if edge_polygon_ID != polygon_ID:
								if edge_polygon_ID not in outer_list and edge_polygon_ID not in inner_list:
									self.polygon.Select (edge_polygon_ID)
									if self.polygon.TestMarks (self.mark_mode_valid) and (self.tag.Get (lx.symbol.i_PTAG_MATR) == materialID):
										outer_list.add (edge_polygon_ID)
		self.polygonIDs.update (inner_list)

class ExpandByMaterial_Cmd(lxu.command.BasicCommand):
	def __init__(self):
		lxu.command.BasicCommand.__init__ (self)

		self.dyna_Add ('materialID', lx.symbol.sTYPE_STRING)
		self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)

	def cmd_Interact(self):
		# Stop modo complaining.
		pass

	def cmd_UserName(self):
		return 'Expand Selection by Material'

	def cmd_Desc(self):
		return 'Expands the current polygon selection to neighbouring polygons sharing the same material tag as the current selection.'

	def cmd_Tooltip(self):
		return 'Expands the current polygon selection to neighbouring polygons sharing the same material tag as the current selection.'

	def cmd_Help(self):
		return 'http://www.farfarer.com/'

	def basic_ButtonName(self):
		return 'Expand Selection by Material'

	def cmd_Flags(self):
		return lx.symbol.fCMD_UNDO

	def basic_Enable(self, msg):
		return True

	def basic_Execute(self, msg, flags):
        timer_start = time.time()

		layer_svc = lx.service.Layer ()
		layer_scan = lx.object.LayerScan (layer_svc.ScanAllocate (lx.symbol.f_LAYERSCAN_ACTIVE | lx.symbol.f_LAYERSCAN_MARKPOLYS))
		if not layer_scan.test ():
			return

		materialID = self.dyna_String (0, None)

		sel_svc = lx.service.Selection ()
		polygon_pkts = []

		# Sort out mark modes we'll need.
		mesh_svc = lx.service.Mesh()
		mark_mode_selected = mesh_svc.ModeCompose (lx.symbol.sMARK_SELECT, None)
		mark_mode_valid = mesh_svc.ModeCompose (None, 'hide lock')

		for n in xrange (layer_scan.Count ()):
			mesh = lx.object.Mesh (layer_scan.MeshBase (n))
			if not mesh.test ():
				continue

			polygon_count = mesh.PolygonCount ()
			if polygon_count == 0:	# Quick out if there are no polys in this layer.
				continue

			polygon = lx.object.Polygon (mesh.PolygonAccessor ())
			if not polygon.test ():
				continue

			edge = lx.object.Edge (mesh.EdgeAccessor ())
			if not edge.test ():
				continue

			visitor = PolysConnectedByMat (polygon, edge, mark_mode_valid, materialID)
			polygon.Enumerate (mark_mode_selected, visitor, 0)

			sel_type_polygon = sel_svc.LookupType (lx.symbol.sSELTYP_POLYGON)
			sel_svc.Drop (sel_type_polygon)
			poly_pkt_trans = lx.object.PolygonPacketTranslation (sel_svc.Allocate (lx.symbol.sSELTYP_POLYGON))
			sel_svc.StartBatch ()
			for polygonID in visitor.getPolyIDs ():
				sel_svc.Select (sel_type_polygon, poly_pkt_trans.Packet (polygonID, mesh))
			sel_svc.EndBatch ()

		layer_scan.Apply ()

        timer_end = time.time()
        lx.out("Time elapsed: %s" % str(timer_end - timer_start))

lx.bless (ExpandByMaterial_Cmd, 'ffr.expandByMat')
