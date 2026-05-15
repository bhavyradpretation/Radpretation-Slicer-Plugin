import qt
import slicer

class ViewerWidget(qt.QWidget):
    """Placeholder for OHIF-like Viewer controls within Slicer."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = qt.QVBoxLayout(self)
        
        lbl = qt.QLabel("Slicer 3D Viewer is active. Use the toolbar for navigation.")
        lbl.setWordWrap(True)
        layout.addWidget(lbl)
        
        self.reset_views_btn = qt.QPushButton("Reset Viewports to Axial/Sagittal/Coronal")
        self.reset_views_btn.clicked.connect(self.reset_views)
        layout.addWidget(self.reset_views_btn)
        
        layout.addStretch()

    def reset_views(self):
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)
