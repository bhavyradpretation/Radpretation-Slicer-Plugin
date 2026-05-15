import ctk
import qt
import slicer

from UI.ViewerWidget import ViewerWidget
from UI.ToolbarWidget import ToolbarWidget
from UI.SettingsWidget import SettingsWidget
from Utils.logger import logger

class MainWidget:
    """The main entry point for the Radpretation Slicer UI."""
    def __init__(self, parent_widget, layout):
        self.parent = parent_widget
        self.layout = layout
        self.setup_ui()

    def setup_ui(self):
        logger.info("Setting up Modern MainWidget UI")
        
        # --- PACS Settings ---
        self.settings_box = ctk.ctkCollapsibleButton()
        self.settings_box.text = "PACS Settings"
        self.settings_box.collapsed = True
        self.layout.addWidget(self.settings_box)
        settings_layout = qt.QVBoxLayout(self.settings_box)
        self.settings_widget = SettingsWidget()
        settings_layout.addWidget(self.settings_widget)
        
        # --- Toolbar Section ---
        self.toolbar_box = ctk.ctkCollapsibleButton()
        self.toolbar_box.text = "Radiology Tools"
        self.layout.addWidget(self.toolbar_box)
        tb_layout = qt.QVBoxLayout(self.toolbar_box)
        self.toolbar_widget = ToolbarWidget()
        tb_layout.addWidget(self.toolbar_widget)



        # --- Viewer Settings ---
        self.viewer_box = ctk.ctkCollapsibleButton()
        self.viewer_box.text = "Viewport Settings"
        self.layout.addWidget(self.viewer_box)
        viewer_layout = qt.QVBoxLayout(self.viewer_box)
        self.viewer_widget = ViewerWidget()
        viewer_layout.addWidget(self.viewer_widget)
        
        # --- Segmentation Actions (to be populated by services) ---
        self.seg_box = ctk.ctkCollapsibleButton()
        self.seg_box.text = "Segmentation Workflow"
        self.layout.addWidget(self.seg_box)
        self.seg_layout = qt.QVBoxLayout(self.seg_box)

        self.create_seg_btn = qt.QPushButton("Create New Segmentation")
        self.seg_layout.addWidget(self.create_seg_btn)

        self.export_seg_btn = qt.QPushButton("Export & Upload to Orthanc")
        self.seg_layout.addWidget(self.export_seg_btn)

        self.seg_status_label = qt.QLabel("Unsaved Changes: False")
        self.seg_layout.addWidget(self.seg_status_label)

        self.layout.addStretch(1)
