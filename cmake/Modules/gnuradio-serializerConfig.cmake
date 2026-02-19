find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_serializer gnuradio-serializer)

FIND_PATH(
    GR_serializer_INCLUDE_DIRS
    NAMES gnuradio/serializer/api.h
    HINTS $ENV{serializer_DIR}/include
        ${PC_serializer_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_serializer_LIBRARIES
    NAMES gnuradio-serializer
    HINTS $ENV{serializer_DIR}/lib
        ${PC_serializer_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-serializerTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_serializer DEFAULT_MSG GR_serializer_LIBRARIES GR_serializer_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_serializer_LIBRARIES GR_serializer_INCLUDE_DIRS)
