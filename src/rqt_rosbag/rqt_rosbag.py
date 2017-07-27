#!/usr/bin/env python
# coding: utf-8

import rospy
import rospkg

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget

from os.path import join, relpath
from glob import glob

class RosbagPlugin(Plugin):

    def __init__(self, context):
        super(RosbagPlugin, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('RosbagPlugin')

        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file which should be in the "resource" folder of this package
        pkg_path = rospkg.RosPack().get_path('rqt_rosbag')
        ui_file = join(pkg_path, 'resource', 'RosbagPlugin.ui')
        # Extend the widget with all atrributes and children from UI File
        loadUi(ui_file, self._widget)
        # Give QObjects reasonable names
        self._widget.setObjectName('RosbagPluginUi')
        # Show _widget.windowTitle on left-top of each plugin(when it's set in _widget).
        # This is useful when you open multiple plugins aat once. Also if you open multiple
        # instances of your plugin at once, these lines add number to make it easy to
        # tell from pane to pane.
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' %d' % context.serial_number()))
        # Add widget to the user interface
        context.add_widget(self._widget)

        # initialize comboBox
        files = self.get_files(join(pkg_path, 'scripts/'), '*.yaml')
        self._widget.TopicListComboBox.addItems(files)

        # callback
        self._widget.RecordPushButton.clicked.connect(self._record_clicked)
        self._widget.StopPushButton.clicked.connect(self._stop_clicked)

    def _record_clicked(self):
        print(self._widget.FileNameLineEdit.text())
        print(self._widget.DulationSpinBox.text())
        print(self._widget.CompressCheckBox.isChecked())
        print(self._widget.TopicListComboBox.currentText())
        self.widget_enabled(False)

    def _stop_clicked(self):
        print("stop clicked")
        self.widget_enabled(True)

    # path以下のformat指定のファイルを返す
    def get_files(self, path, format):
        return [relpath(x, path) for x in glob(join(path, format))]

    # widgetのenable/disableを切り替え
    def widget_enabled(self, enabled):
        self._widget.FileNameLineEdit.setEnabled(enabled)
        self._widget.DulationSpinBox.setEnabled(enabled)
        self._widget.CompressCheckBox.setEnabled(enabled)
        self._widget.TopicListComboBox.setEnabled(enabled)

    def shutdown_plugin(self):
        # TODO unregister all publishers here
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.get_value(k, v)
        pass

    def restore_settings(self, pluign_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass
