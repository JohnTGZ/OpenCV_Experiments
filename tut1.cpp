#include "opencv2/imgproc.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"
#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char** argv){
  CommandLineParser parser(argc, argv, "{@input | lena.png | input image}" );
  Mat src = imread( parser.get<String>("@input"));
  if (src.empty()){
    std::cout << "unable to load image" << std::endl;
    return -1;
  }

  cvtColor( src, src, COLOR_BGR2GRAY);

  Mat dst;
  equalizeHist(src, dst);
  imshow("original", src);
  imshow("equalized", dst);
  moveWindow("equalized", 500, 0);

  waitKey(0);
  return 0;
}