find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_eas gnuradio-eas)

FIND_PATH(
    GR_eas_INCLUDE_DIRS
    NAMES gnuradio/eas/api.h
    HINTS $ENV{eas_DIR}/include
        ${PC_eas_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_eas_LIBRARIES
    NAMES gnuradio-eas
    HINTS $ENV{eas_DIR}/lib
        ${PC_eas_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-easTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_eas DEFAULT_MSG GR_eas_LIBRARIES GR_eas_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_eas_LIBRARIES GR_eas_INCLUDE_DIRS)
