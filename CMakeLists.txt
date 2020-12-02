cmake_minimum_required(VERSION 2.8)
SET(CMAKE_CXX_FLAGS "-std=c++11")
project( tut1 )

find_package( OpenMP)
if (OpenMP_C11_FOUND)
    target_link_libraries(tut1 PUBLIC OpenMP::OpenMP_C11)
endif()

###############
#FIND PACKAGES
###############
find_package( OpenCV REQUIRED)
find_package( Ceres REQUIRED COMPONENTS SuiteSparse)
find_package( Eigen3 REQUIRED)

###############
#INCLUDE DIR
###############
include_directories( 
  include
  ${OpenCV_INCLUDE_DIRS} 
  ${CERES_INCLUDES}
  ${Eigen3_INCLUDE_DIRS}
)

#############################################
#ADD EXECUTABLE AND TARGET LINK LIBRARIES
#############################################
add_executable( tut1 tut1.cpp )
target_link_libraries( tut1 ${OpenCV_LIBS} )