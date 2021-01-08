#include <iostream>
#include <opencv2/aruco.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>

int main(int argc, char** argv){
  cv::CommandLineParser parser(argc, argv, "{@input | aruco_sample.jpg | input image}");
  cv::Mat src = cv::imread( parser.get<cv::String>("@input"));
  if (src.empty()){
    std::cout << "unable to load image" << std::endl;
    return -1;
  }

  cv::Mat inputImage = src;

  std::vector<int> markerIds;
  std::vector<std::vector<cv::Point2f>> markerCorners, rejectedCandidates;
  cv::Ptr<cv::aruco::DetectorParameters> parameters = cv::aruco::DetectorParameters::create();
  cv::Ptr<cv::aruco::Dictionary> dictionary = cv::aruco::getPredefinedDictionary(cv::aruco::DICT_6X6_250);
  cv::aruco::detectMarkers(inputImage, dictionary, markerCorners, markerIds, parameters, rejectedCandidates);

  cv::Mat outputImage = inputImage.clone();
  cv::aruco::drawDetectedMarkers(outputImage, markerCorners, markerIds);

  cv::imshow("detected Markers", outputImage);
  cv::waitKey(0);

  return 0;
}