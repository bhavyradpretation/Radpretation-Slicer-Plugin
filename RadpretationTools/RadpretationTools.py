import os
import qt
import slicer

from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

from UI.MainWidget import MainWidget
from Utils.logger import logger

class RadpretationTools(ScriptedLoadableModule):
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "RadpretationTools"
        self.parent.categories = ["Radpretation"]
        self.parent.dependencies = []
        self.parent.contributors = ["Bhavy Raheja"]
        self.parent.helpText = "Radpretation Advanced Workstation integration for 3D Slicer."
        self.parent.acknowledgementText = "Developed for Radpretation."


class RadpretationToolsWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    def __init__(self, parent=None):
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)
        self.mainWidget = None

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)
        logger.info("Initializing RadpretationToolsWidget setup")

        # Instantiate the UI architecture
        self.mainWidget = MainWidget(self, self.layout)
        
        # Connections will be established below

        # Instantiate Services
        from Services.SegmentationService import SegmentationService
        from Services.ExportService import ExportService
        from Services.LocalBridgeServer import LocalBridgeServer
        from Utils.helpers import MainThreadDispatcher

        # Initialize the dispatcher on the main thread so its QTimer is bound to Slicer's main event loop
        MainThreadDispatcher.get_instance()

        self.segmentation_service = SegmentationService()
        self.export_service = ExportService(self.segmentation_service)
        
        self.local_bridge_server = LocalBridgeServer(self.mainWidget)
        self.local_bridge_server.start()

        # Connect UI Buttons
        self.mainWidget.create_seg_btn.connect("clicked()", self.onCreateSegmentationClicked)
        self.mainWidget.export_seg_btn.connect("clicked()", self.onExportClicked)

    def onCreateSegmentationClicked(self):
        self.segmentation_service.create_segmentation()
        self.mainWidget.seg_status_label.setText("Unsaved Changes: True")

    def onExportClicked(self):
        self.mainWidget.seg_status_label.setText("Exporting...")
        def on_complete(success, message):
            self.mainWidget.seg_status_label.setText(f"Status: {message}")
            if success:
                # Update label since we cleared unsaved changes
                pass
        self.export_service.export_and_upload(on_complete)

    def cleanup(self):
        if hasattr(self, 'local_bridge_server'):
            self.local_bridge_server.stop()
        if hasattr(self, 'segmentation_service'):
            self.segmentation_service.observer_manager.remove_all()
        self.removeObservers()

class RadpretationToolsLogic(ScriptedLoadableModuleLogic):
    def __init__(self):
        ScriptedLoadableModuleLogic.__init__(self)

class RadpretationToolsTest(ScriptedLoadableModuleTest):
    def setUp(self):
        slicer.mrmlScene.Clear()

    def runTest(self):
        self.setUp()
