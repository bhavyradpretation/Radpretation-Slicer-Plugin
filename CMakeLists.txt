cmake_minimum_required(VERSION 3.20.6...3.22.6 FATAL_ERROR)

project(RadpretationExtension)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/RadpretationExtension")
set(EXTENSION_CONTRIBUTORS "Bhavy Raheja (Radpretation)")
set(EXTENSION_DESCRIPTION "Advanced workstation integration between OHIF, Orthanc, and 3D Slicer for Radpretation.")
set(EXTENSION_ICONURL "https://www.example.com/Slicer/Extensions/RadpretationExtension.png")
set(EXTENSION_SCREENSHOTURLS "https://www.example.com/Slicer/Extensions/RadpretationExtension/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(RadpretationTools)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
