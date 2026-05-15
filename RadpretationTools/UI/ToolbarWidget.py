import qt
import slicer

class ToolbarWidget(qt.QWidget):
    """Toolbar for OHIF-like tools (W/L, Pan, Zoom)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = qt.QHBoxLayout(self)
        
        self.wl_btn = qt.QPushButton("Window/Level")
        self.wl_btn.clicked.connect(lambda: self.switch_mode("WindowLevel"))
        
        self.pan_btn = qt.QPushButton("Pan")
        self.pan_btn.clicked.connect(lambda: self.switch_mode("Pan"))
        
        self.zoom_btn = qt.QPushButton("Zoom")
        self.zoom_btn.clicked.connect(lambda: self.switch_mode("Zoom"))

        layout.addWidget(self.wl_btn)
        layout.addWidget(self.pan_btn)
        layout.addWidget(self.zoom_btn)
        layout.addStretch()

    def switch_mode(self, mode):
        # Interacts with Slicer's crosshair/mouse modes
        interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
        if mode == "WindowLevel":
            interactionNode.SetCurrentInteractionMode(slicer.vtkMRMLInteractionNode.WindowLevel)
        elif mode == "Pan":
            interactionNode.SetCurrentInteractionMode(slicer.vtkMRMLInteractionNode.Pan)
        elif mode == "Zoom":
            interactionNode.SetCurrentInteractionMode(slicer.vtkMRMLInteractionNode.Zoom)
