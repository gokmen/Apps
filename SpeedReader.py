#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Speed Reader """

import time

from PyQt4.QtCore import QSize
from PyQt4.QtCore import QChar
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QPoint

from PyQt4.QtGui import qApp
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QApplication

__author__    = "Gökmen Göksel"
__email__     = "gokmen@goksel.me"
__copyright__ = "Copyright 2011, Leskog"
__license__   = "GPLv2"
__version__   = "0.1"

# Copyright (C) 2011, Leskog
# 2011 - Gökmen Göksel <gokmen@goksel.me>

# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

class FunnyLabel(QWidget):
    """ FunnyLabel, dynamic label which fits its container. """

    def __init__(self, parent = None):
        """ Init Method

            :param parent: Parent Widget
            :type parent: QWidget

        """
        QWidget.__init__(self, parent)

        # Get the system font
        self.font = qApp.font().toString().split(',')[0]

        # Set default text
        self.setText()

    def setText(self, text = ''):
        """ This function is used to update label text.

        :param text: New text to update label
        :type text: string

        """
        # Store the text
        self.text = text

        # Create a qfont for system font
        # We will use the font to calculate metrics
        font = QFont(self.font, 10, QFont.Normal)
        fm = QFontMetrics(font)

        # Calculate base_width/height over system font
        self.font_base_width = fm.width(self.text)
        self.font_base_height = fm.height()

        # Re-paint the text
        self.update()

    def paintEvent(self, event):
        """ This is reimplemented method from QWidget.paintEvent()

        :param event: Paint Event
        :type event: QPaintEvent

        """
        # Just re-paint if there is a text
        if self.text:

            # Get container boundaries
            wi = self.width()
            he = self.height()

            # Calculate Font Point for Width & Height over base font values
            fpt_w = (wi * 10) / (self.font_base_width)
            fpt_h = (he * 10) / (self.font_base_height)

            # Create a new font which fits to the container
            font = QFont(self.font, min(fpt_w, fpt_h), QFont.Normal)
            fm = QFontMetrics(font)

            # Calculate text boundaries over new font
            rect = fm.boundingRect(self.text)
            leftBearing = fm.leftBearing(QChar('X'))

            # Start to paint
            painter = QPainter()
            painter.begin(self)
            painter.setFont(font)

            # Draw the text at the center of the container
            painter.drawText(QPoint(wi/2 - rect.width()/2 - leftBearing, \
                                    he/2 + rect.height()/3),
                             self.text)

            # Finish paint
            painter.end()

class SpeedReader(QDialog):
    """ SpeedReader is a simple application that provides easy&speed
        reading for plain text files. """

    def __init__(self, parent = None):
        """ Init Method

        :param parent: Parent Widget
        :type parent: QWidget

        """
        QDialog.__init__(self, parent)
        self.setWindowTitle('Speed Reader')

        # Add a FunnyLabel
        self.label = FunnyLabel(self)
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.label)

        # Setup a timer to show next word
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._showNextWord)

    def loadContent(self, content):
        """ This function loads given content and starts the reading timer.

        :param path_to_file: Content of the file, content must be PLAINTEXT
        :type path_to_file: string

        """
        # Stop current timer if its running
        self.timer.stop()

        # Load and split the file
        self.content = unicode(content).split()

        # Set the current word as 0
        self.current = 0

        # Burn it!
        self.timer.start(300)

    def _showNextWord(self):
        """ This function is an internal function to show next word in
            the content. """

        # Get the current word
        self.label.setText(self.content[self.current])

        # Next
        self.current += 1

        # Stop if at EOF
        if self.current == len(self.content):
            self.timer.stop()

if __name__ == '__main__':
    # We need arguments
    import os
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='SpeedReader, read Plain Text files in easy&speed way')
    parser.add_argument('to_read', help='FILE or TEXT to read')

    args = parser.parse_args()
    app = QApplication(sys.argv)

    # Create an instance to run SpeedReader
    widget = SpeedReader()
    widget.resize(QSize(340, 180))
    if os.path.exists(args.to_read):
        widget.loadContent(file(args.to_read).read())
    else:
        widget.loadContent(unicode(args.to_read))
    widget.show()

    # Fire!
    sys.exit(app.exec_())
