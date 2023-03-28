find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_SERIALIZER gnuradio-serializer)

FIND_PATH(
    GR_SERIALIZER_INCLUDE_DIRS
    NAMES gnuradio/serializer/api.h
    HINTS $ENV{SERIALIZER_DIR}/include
        ${PC_SERIALIZER_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_SERIALIZER_LIBRARIES
    NAMES gnuradio-serializer
    HINTS $ENV{SERIALIZER_DIR}/lib
        ${PC_SERIALIZER_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-serializerTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_SERIALIZER DEFAULT_MSG GR_SERIALIZER_LIBRARIES GR_SERIALIZER_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_SERIALIZER_LIBRARIES GR_SERIALIZER_INCLUDE_DIRS)
