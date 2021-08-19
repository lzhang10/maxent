cmake_minimum_required(VERSION 3.10)

# set the project name
project(maxent)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_FLAGS "-Wall")
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

include(CheckLanguage)
check_language(Fortran)
if(CMAKE_Fortran_COMPILER)
  enable_language(Fortran)
else()
  message(FATAL_ERROR "Can not detect Fortran compiler required for building lbfgs optimizer. Please install a Fortran compiler like gfortran to proceed.")
endif()

set(CMAKE_FIND_LIBRARY_SUFFIXES ".a")
#set(BUILD_SHARED_LIBS OFF)
set(Boost_USE_STATIC_LIBS ON)
find_package(Boost 1.48.0 REQUIRED COMPONENTS timer)
include_directories(SYSTEM ${Boost_INCLUDE_DIR})

# zlib1g-dev on debian
find_package( ZLIB REQUIRED )
include_directories( ${ZLIB_INCLUDE_DIRS})
link_libraries(${ZLIB_LIBRARIES})

add_subdirectory(src)
add_subdirectory(test)
