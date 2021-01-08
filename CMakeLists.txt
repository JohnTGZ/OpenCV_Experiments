cmake_minimum_required(VERSION 2.8)
SET(CMAKE_CXX_FLAGS "-std=c++11")
project( aruco )

find_package( OpenMP)
if (OpenMP_C11_FOUND)
    target_link_libraries(aruco PUBLIC OpenMP::OpenMP_C11)
endif()

###############
#FIND PACKAGES
###############
find_package( OpenCV REQUIRED)
#find_package( Ceres REQUIRED COMPONENTS SuiteSparse)
find_package( Eigen3 REQUIRED)
find_package(realsense2)
if(NOT realsense2_FOUND)
    message(FATAL_ERROR "\n\n Intel RealSense SDK 2.0 is missing, please install it from https://github.com/IntelRealSense/librealsense/releases\n\n")
endif()

###############
#INCLUDE DIR
###############
include_directories( 
  include
  ${OpenCV_INCLUDE_DIRS} 
  ${Eigen3_INCLUDE_DIRS}
  ${realsense2_INCLUDE_DIR}
#  ${CERES_INCLUDES}
)

#############################################
#ADD EXECUTABLE AND TARGET LINK LIBRARIES
#############################################
add_executable( aruco aruco.cpp )
target_link_libraries( aruco ${OpenCV_LIBS} ${realsense2_LIBRARY})

add_executable( rs_tut rs_tut.cpp )
target_link_libraries( rs_tut ${OpenCV_LIBS} ${realsense2_LIBRARY})
