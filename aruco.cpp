#include <iostream>
#include <opencv2/aruco.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>

#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API
#include <opencv2/opencv.hpp> // Include OpenCV API

void readCameraParams(cv::Mat& cameraMatrix, cv::Mat& distCoeffs, std::string filename);

int main(int argc, char** argv){
  // cv::CommandLineParser parser(argc, argv, "{@input | aruco_sample.jpg | input image}");
  // cv::Mat src = cv::imread( parser.get<cv::String>("@input"));
  // if (src.empty()){
  //   std::cout << "unable to load image" << std::endl;
  //   return -1;
  // }
 
  float marker_width = 0.093; //Marker Width (in meters)
  float axis_disp_length = 0.1; //Display of axis length (in meters)

  cv::Ptr<cv::aruco::Dictionary> dictionary = cv::aruco::getPredefinedDictionary(cv::aruco::DICT_4X4_50);
  cv::Ptr<cv::aruco::DetectorParameters> detectorParams = cv::aruco::DetectorParameters::create(
    
  );
  int waitTime = 10; //in milliseconds

  cv::VideoCapture inputVideo;
  inputVideo.open(0);

  //init image holders
  cv::Mat image, imageCopy;
  //init calib matrices
  cv::Mat cameraMatrix, distCoeffs;
  readCameraParams(cameraMatrix, distCoeffs, "realsense_calib.json");

  while(inputVideo.grab()){
    // std::cout << "grab frame " << frame_no << std::endl;
    
    inputVideo.retrieve(image);
    image.copyTo(imageCopy);

    //Obtain corner and ids of markers
    std::vector<int> markerIds;
    std::vector<std::vector<cv::Point2f>> markerCorners;
    cv::aruco::detectMarkers(image, dictionary, markerCorners, markerIds, detectorParams);

    //if at least one marker detected
    if (markerIds.size() > 0){
      cv::aruco::drawDetectedMarkers(imageCopy, markerCorners, markerIds);

      //Estimate pose of markers
      std::vector<cv::Vec3d> rvecs, tvecs; //rotation and translation vectors respectively
      cv::aruco::estimatePoseSingleMarkers(markerCorners, marker_width, cameraMatrix, distCoeffs, rvecs, tvecs);

      //draw axis for each marker
      for (int i=0; i < markerIds.size(); i++){
        cv::aruco::drawAxis(imageCopy, cameraMatrix, distCoeffs, rvecs[i], tvecs[i], axis_disp_length);
      }
    }

    cv::imshow("out", imageCopy);
    char key = (char) cv::waitKey(waitTime);
    if (key == 27)
      break;

  }
  
  return 0;
}



void readCameraParams(cv::Mat& cameraMatrix, cv::Mat& distCoeffs, std::string filename){
  //cameraMatrix: 3x3 floating point camera matrix A
  //distCoeffs: vector of distortion coefficients 

}