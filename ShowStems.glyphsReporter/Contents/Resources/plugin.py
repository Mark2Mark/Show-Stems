# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

## ToDo: display the matched stem? e.g. `oH` / `nH` / ...

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

from math import tan, radians
import traceback
# import numpy as np

class ShowVerticalStems(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Stems',
			'de': 'Stämme',
			'fr': 'les traits',
			'es': 'astas',
		})
		self.keyboardShortcut = 's'
		self.keyboardShortcutModifier = NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask

	@objc.python_method
	def foreground(self, layer):
		self.verticalStems(layer)

	@objc.python_method
	def BoundsRect(self, NSRect):
		x = NSRect[0][0]
		y = NSRect[0][1]
		width = NSRect[1][0]
		height = NSRect[1][1]
		return x, y, width, height

	@objc.python_method
	def drawLine(self, color, x1, y1, x2, y2, w=1):
		myPath = NSBezierPath.bezierPath()
		myPath.moveToPoint_((x1, y1))
		myPath.lineToPoint_((x2, y2))
		myPath.setLineWidth_(w/self.getScale())
		if self.dashed:
			myPath.setLineDash_count_phase_((2, 2), 2, 0.0)
		NSColor.colorWithCalibratedRed_green_blue_alpha_( *color ).set()
		myPath.stroke()

	@objc.python_method
	def italo(self, yPos):
		'''	ITALIC OFFSET '''
		offset = tan(radians(self.angle)) * self.xHeight/2
		shift = tan(radians(self.angle)) * yPos - offset
		return shift

	@objc.python_method
	def drawBadge(self, x, y, width, color):
		height = width
		myRect = NSRect( ( x - width/2, y - height/2 ), ( width, height ) )
		myPath = NSBezierPath.bezierPathWithOvalInRect_( myRect )
		NSColor.colorWithCalibratedRed_green_blue_alpha_( *color ).set()
		myPath.fill()

	@objc.python_method
	def drawRoundedRectangleForStringAtPosition(self, thisString, center, fontsize, color=(0, .3, .8, .65) ):
		x, y = center
		scaledSize = fontsize / self.getScale()
		width = len(thisString) * scaledSize * 0.7
		rim = scaledSize * 0.3
		panel = NSRect()
		panel.origin = NSPoint( x-width/2, y-scaledSize/2-rim )
		panel.size = NSSize( width, scaledSize + rim*2 )
		NSColor.colorWithCalibratedRed_green_blue_alpha_( *color ).set()
		NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_( panel, scaledSize*0.5, scaledSize*0.5 ).fill()
		self.drawTextAtPoint(thisString, center, fontsize, align="center", fontColor=NSColor.whiteColor() )

	@objc.python_method
	def drawTriangle(self, x, y, size):
		myPath = NSBezierPath.bezierPath()
		size = size / self.getScale()
		a, b, c = 0, size, size * 2
		myPath.moveToPoint_( (a + x, a + y - size / 2) )
		myPath.lineToPoint_( (a + x, c + y - size / 2) )
		myPath.lineToPoint_( (b + x, b + y - size / 2) )
		myPath.closePath()

		### FILL
		NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.8, 0.8, 0.8, 0.8 ).set()
		myPath.fill()

	@objc.python_method
	def verticalStems(self, layer):
		try:
			letterCase = layer.parent.subCategory
		except:
			letterCase = None

		MeasurementPositionMeasurementLine = NSUserDefaults.standardUserDefaults().floatForKey_("MeasurementPositionMeasurementLine")
		Dimensions = {}
		savedMeasurements = {}
		thisFont = layer.parent.parent
		thisMasterID = thisFont.selectedFontMaster.id
		try:
			Dimensions = thisFont.userData["GSDimensionPlugin.Dimensions"]
			savedMeasurements = Dimensions[thisMasterID]
		except:
			# print(traceback.format_exc())
			pass

		###### IMPORTANT: convert to int, because the input fields could return objc.unicode or objc.integers.
		## LC
		try:
			savedMeasurements_nV = int(savedMeasurements["nV"])
		except:
			savedMeasurements_nV = None
		try:
			savedMeasurements_oV = int(savedMeasurements["oV"])
		except:
			savedMeasurements_oV = None
		## UC
		try:
			savedMeasurements_HV = int(savedMeasurements["HV"])
		except:
			savedMeasurements_HV = None
		try:
			savedMeasurements_OV = int(savedMeasurements["OV"])
		except:
			savedMeasurements_OV = None


		try:
			lineColor = 0, 0, 0.3, 0.1
			backlineColor = 1, 1, 1, 0.45
			intersectionColor = 0, 0, 0.3, 0.15
			onPathColor = 0, 0.75, 0.2, 0.8
			offPathColor = 0.8, 0, 0.1, 0.1

			'''	PATH '''
			self.dashed = False
			self.xHeight = layer.master.xHeight
			self.capHeight = layer.master.capHeight
			self.angle = layer.master.italicAngle

			if letterCase == "Uppercase":
				verticalCenter = self.capHeight
			else:
				verticalCenter = self.xHeight

			### LAYER/METRIC DIMENSIONS
			xLayerLeft = 0
			xLayerRight = layer.width
			yAscender = layer.master.ascender
			yDescender = layer.master.descender

			### Line from (0, 0) to (xHeight, LayerWidth)
			# self.drawLine( 0 + self.italo(0) , 0, xLayerRight + self.italo(verticalCenter), verticalCenter)

			MeasurementPosition = True ### OPTION LATER
			if MeasurementPosition:
				linePosY = MeasurementPositionMeasurementLine
			else:
				linePosY = verticalCenter / 2

			centerLine = 0 + self.italo(linePosY) , linePosY, xLayerRight + self.italo(linePosY), linePosY
			centerLinePointA, centerLinePointB = (0 + self.italo(linePosY) , linePosY), (xLayerRight + self.italo(linePosY), linePosY) ## same as above, just formatted differently
			self.drawLine( backlineColor, *centerLine, w=2.5 )
			self.drawLine( lineColor, *centerLine )


			# A) ignoring components
			# intersectionsBetweenPoints = layer.intersectionsBetweenPoints( centerLinePointA, centerLinePointB )
			# B) including components
			intersectionsBetweenPoints = layer.copyDecomposedLayer().intersectionsBetweenPoints( centerLinePointA, centerLinePointB )

			try:
				NSLayerPath = layer.bezierPath()
				# NSLayerPath = layer.copyDecomposedLayer().bezierPath()
			except:
				NSLayerPath = layer.bezierPath
				# NSLayerPath = layer.copyDecomposedLayer().bezierPath
				# NSLayerPath.fill()
			badgeSize = 5 / self.getScale()

			for i, point in enumerate(intersectionsBetweenPoints):
				'''
				1)
				cycle through all distances A-B, B-C, C-D, ...
				'''

				if i < len(intersectionsBetweenPoints) - 1:
					pointA = intersectionsBetweenPoints[i]
					pointB = intersectionsBetweenPoints[i+1]

				try:
					thisDistance = pointB.x - pointA.x
					thisDistanceRounded = int(round(thisDistance))
					thisDistanceCenterX = pointA.x + (pointB.x - pointA.x) / 2
					shiftY = 10 / self.getScale()
					if i < len(intersectionsBetweenPoints) - 1: ## avoid last segment to draw text twice
						self.drawRoundedRectangleForStringAtPosition(" %s " % thisDistanceRounded, (thisDistanceCenterX, linePosY + shiftY), 10 )
						# self.drawTextAtPoint(" %s " % thisDistanceRounded, (thisDistanceCenterX, linePosY + shiftY), 9 )

					try:
						text = int( savedMeasurements.keys()[savedMeasurements.values().index( thisDistanceRounded )] )
					except:
						text = ""




					if letterCase == "Lowercase":
						if thisDistanceRounded == savedMeasurements_nV and thisDistanceRounded == savedMeasurements_oV:
							self.drawLine( onPathColor, pointA.x, linePosY, pointB.x, linePosY )
							### A) two badges below each other
							# self.drawRoundedRectangleForStringAtPosition( " n ", (thisDistanceCenterX, linePosY - shiftY), 10, color=onPathColor )
							# self.drawRoundedRectangleForStringAtPosition( " o ", (thisDistanceCenterX, linePosY - shiftY*2.8), 10, color=onPathColor )
							### B) one badges, comma separated
							self.drawRoundedRectangleForStringAtPosition( " n, o ", (thisDistanceCenterX, linePosY - shiftY), 10, color=onPathColor )
						elif thisDistanceRounded == savedMeasurements_nV:
							self.drawLine( onPathColor, pointA.x, linePosY, pointB.x, linePosY )
							self.drawRoundedRectangleForStringAtPosition( " n ", (thisDistanceCenterX, linePosY - shiftY), 10, color=onPathColor )
						elif thisDistanceRounded == savedMeasurements_oV:
							self.drawLine( onPathColor, pointA.x, linePosY, pointB.x, linePosY )
							self.drawRoundedRectangleForStringAtPosition( " o ", (thisDistanceCenterX, linePosY - shiftY), 10, color=onPathColor )

					elif letterCase == "Uppercase": # or `if`
						if thisDistanceRounded == savedMeasurements_HV and thisDistanceRounded == savedMeasurements_OV:
							self.drawLine( onPathColor, pointA.x, linePosY, pointB.x, linePosY )
							### A) two badges below each other
							# self.drawRoundedRectangleForStringAtPosition( " H ", (thisDistanceCenterX, linePosY - shiftY), 10, color=onPathColor )
							# self.drawRoundedRectangleForStringAtPosition( " O ", (thisDistanceCenterX, linePosY - shiftY*2.8), 10, color=onPathColor )
							### B) one badges, comma separated
							self.drawRoundedRectangleForStringAtPosition( " H, O ", (thisDistanceCenterX, linePosY - shiftY), 10, color=onPathColor )
						elif thisDistanceRounded == savedMeasurements_HV:
							self.drawLine( onPathColor, pointA.x, linePosY, pointB.x, linePosY )
							self.drawRoundedRectangleForStringAtPosition( " H ", (thisDistanceCenterX, linePosY - shiftY), 10, color=onPathColor )
						elif thisDistanceRounded == savedMeasurements_OV:
							self.drawLine( onPathColor, pointA.x, linePosY, pointB.x, linePosY )
							self.drawRoundedRectangleForStringAtPosition( " O ", (thisDistanceCenterX, linePosY - shiftY), 10, color=onPathColor )



					else:
						allStems = []
						for val in savedMeasurements.items():
							key, value = val
							if key[:-1] == "V": # pass only vertical dimensions
								if int(value) == thisDistanceRounded:
									allStems.append(key[0])
						text = ", ".join(allStems)


						if len(allStems) > 0:
							if len(allStems) == 1:
								t = " %s " % text
							else:
								t = "%s" % text
							self.drawLine( onPathColor, pointA.x, linePosY, pointB.x, linePosY )
							self.drawRoundedRectangleForStringAtPosition( t, (thisDistanceCenterX, linePosY - shiftY), 10, color=onPathColor )



					# self.logToConsole( str(thisDistanceCenterX) )

					'''
					check if each distance (e.g. center of distance onPath) is on path, if so:
					'''
					if NSLayerPath:
						if NSLayerPath.containsPoint_( (thisDistanceCenterX, linePosY) ):
							# self.drawTextAtPoint("1", (thisDistanceCenterX, linePosY), 0 )
							self.drawBadge( thisDistanceCenterX, linePosY, badgeSize, onPathColor )
							# if thisDistance = :
					else:
						# self.drawTextAtPoint("o", (thisDistanceCenterX, linePosY), 0 )
						self.drawBadge( thisDistanceCenterX, linePosY, badgeSize, offPathColor )

					# self.drawTextAtPoint("x", (point.x, linePosY), 0 )
					self.drawBadge( point.x, linePosY, badgeSize, intersectionColor )

					'''
					DRAW VERTICAL CENTER
					'''
					self.drawTriangle( 0, verticalCenter / 2, 6 )

				except:
					print(traceback.format_exc())

				'''
				draw a vertical line with italic angle in the center of this distance
				2)
				also if so: check the distance with the defaults for stemWidth and display green if match
				Make the same as here, but with each path for the layer (so that e.g the crossbar of an H does not bother)
				3)
				Draw /n at second stem
				'''

		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_: %s" % str(e) )

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
