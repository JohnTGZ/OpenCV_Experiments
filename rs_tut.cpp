#include <librealsense2/rs.hpp>
#include <opencv2/opencv.hpp>   // Include OpenCV API
#include <opencv2/aruco.hpp>

static cv::Mat depth_frame_to_meters( const rs2::depth_frame & f );
static cv::Mat frame_to_mat(const rs2::frame& f);

int main(int argc, char * argv[]) try
{
  //declare depth colorizer for pretty visualization of depth data
  rs2::colorizer color_map;

  // Declare RealSense pipeline, encapsulating the actual device and sensors
  rs2::pipeline pipe;
  auto config = pipe.start();
  auto profile = config.get_stream(RS2_STREAM_COLOR).as<rs2::video_stream_profile>();
  rs2::align align_to(RS2_STREAM_COLOR);

  const auto window_name = "Display Image";
  cv::namedWindow(window_name, cv::WINDOW_AUTOSIZE);
  while (cv::waitKey(1) < 0 && cv::getWindowProperty(window_name, cv::WND_PROP_AUTOSIZE) >= 0)
  {
      rs2::frameset data = pipe.wait_for_frames(); // Wait for next set of frames from the camera
      data = align_to.process(data);

      auto color_frame = data.get_color_frame();
      auto depth_frame = data.get_depth_frame();

      // Convert RealSense frame to OpenCV matrix:
      auto color_mat = frame_to_mat(color_frame);
      auto depth_mat = depth_frame_to_meters(depth_frame);

      // // Query frame size (width and height)
      // const int w = depth.as<rs2::video_frame>().get_width();
      // const int h = depth.as<rs2::video_frame>().get_height();
      // // Create OpenCV matrix of size (w,h) from the colorized depth data
      // Mat image(Size(w, h), CV_8UC3, (void*)depth.get_data(), Mat::AUTO_STEP);

      // Update the window with new data
      cv::imshow(window_name, color_mat);
  }

  return EXIT_SUCCESS;
}

catch (const rs2::error & e)
{
  std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n    " << e.what() << std::endl;
  return EXIT_FAILURE;
}
catch (const std::exception& e)
{
  std::cerr << e.what() << std::endl;
  return EXIT_FAILURE;
}


// Convert rs2::frame to cv::Mat
static cv::Mat frame_to_mat(const rs2::frame& f)
{
    using namespace cv;
    using namespace rs2;

    auto vf = f.as<video_frame>();
    const int w = vf.get_width();
    const int h = vf.get_height();

    if (f.get_profile().format() == RS2_FORMAT_BGR8)
    {
        return Mat(Size(w, h), CV_8UC3, (void*)f.get_data(), Mat::AUTO_STEP);
    }
    else if (f.get_profile().format() == RS2_FORMAT_RGB8)
    {
        auto r_rgb = Mat(Size(w, h), CV_8UC3, (void*)f.get_data(), Mat::AUTO_STEP);
        Mat r_bgr;
        cvtColor(r_rgb, r_bgr, COLOR_RGB2BGR);
        return r_bgr;
    }
    else if (f.get_profile().format() == RS2_FORMAT_Z16)
    {
        return Mat(Size(w, h), CV_16UC1, (void*)f.get_data(), Mat::AUTO_STEP);
    }
    else if (f.get_profile().format() == RS2_FORMAT_Y8)
    {
        return Mat(Size(w, h), CV_8UC1, (void*)f.get_data(), Mat::AUTO_STEP);
    }
    else if (f.get_profile().format() == RS2_FORMAT_DISPARITY32)
    {
        return Mat(Size(w, h), CV_32FC1, (void*)f.get_data(), Mat::AUTO_STEP);
    }

    throw std::runtime_error("Frame format is not supported yet!");
}

// Converts depth frame to a matrix of doubles with distances in meters
static cv::Mat depth_frame_to_meters( const rs2::depth_frame & f )
{
    cv::Mat dm = frame_to_mat(f);
    dm.convertTo( dm, CV_64F );
    dm = dm * f.get_units();
    return dm;
}