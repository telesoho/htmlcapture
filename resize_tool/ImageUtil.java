package jp.co.uclgroup.util;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import javax.imageio.ImageIO;
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfRect;
import org.opencv.core.Rect;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;

public class ImageUtil
{
  public static void convert2Jpeg(String srcPath, String outPath)
    throws IOException
  {
    File inFile = new File(srcPath);
    BufferedImage im = ImageIO.read(inFile);
    convert2Jpeg(im, outPath);
  }
  
  public static void convert2Jpeg(BufferedImage im, String outPath)
    throws IOException
  {
    BufferedImage om = convert2Jpeg(im);
    File outFile = new File(outPath);
    ImageIO.write(om, "jpeg", outFile);
  }
  
  public static BufferedImage convert2Jpeg(BufferedImage im)
    throws IOException
  {
    BufferedImage om = new BufferedImage(im.getWidth(), im.getHeight(), 1);
    Graphics2D off = om.createGraphics();
    off.drawImage(im, 0, 0, Color.WHITE, null);
    return om;
  }
  
  public static List<File> fileList(String folderPath, boolean isSub)
  {
    File folder = new File(folderPath);
    List<File> fileList = new ArrayList();
    _getFileList(folder, fileList, isSub);
    return fileList;
  }
  
  private static void _getFileList(File folder, List<File> fileList, boolean isSub)
  {
    if ((folder.exists()) && (folder.isDirectory()))
    {
      File[] temp = folder.listFiles();
      if ((temp != null) && (temp.length > 0))
      {
        File[] arrayOfFile1;
        int j = (arrayOfFile1 = temp).length;
        for (int i = 0; i < j; i++)
        {
          File f = arrayOfFile1[i];
          if ((f.isFile()) && (
            (f.getName().toLowerCase().endsWith("jpg")) || 
            
            (f.getName().toLowerCase().endsWith("png")) || 
            (f.getName().toLowerCase().endsWith("jpeg")))) {
            fileList.add(f);
          } else if ((f.isDirectory()) && (isSub)) {
            _getFileList(f, fileList, isSub);
          }
        }
      }
    }
  }
  
  public static void trimmingOne(String inPath, String outPath, String type, int x, int y, int width, int height)
    throws IOException
  {
    BufferedImage im = ImageIO.read(new File(inPath));
    BufferedImage om = im.getSubimage(x, y, width, height);
    ImageIO.write(om, type, new File(outPath));
  }
  
  public static void trimmingAll(String inPath, String outFolder, String fnPrefix, String type, int width, int height)
    throws IOException
  {
    File out = new File(outFolder);
    if (!out.exists()) {
      out.mkdirs();
    }
    BufferedImage im = ImageIO.read(new File(inPath));
    _trimmingAll(im, outFolder, fnPrefix, type, width, height, 0, 1);
  }
  
  private static void _trimmingAll(BufferedImage im, String outFolder, String fnPrefix, String type, int width, int height, int y, int n)
    throws IOException
  {
    String outPath = outFolder + "\\" + fnPrefix + "_" + n + "." + type;
    boolean continueFlg = true;
    int h = height;
    if (im.getHeight() - y <= height + 20)
    {
      h = im.getHeight() - y - 20;
      continueFlg = false;
    }
    BufferedImage om = im.getSubimage(0, y, width, h);
    ImageIO.write(om, type, new File(outPath));
    if (continueFlg)
    {
      y += height;
      n++;
      _trimmingAll(im, outFolder, fnPrefix, type, width, height, y, n);
    }
  }
  
  public static double findFaceY(String filePath, String detectorXml)
  {
    System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    CascadeClassifier faceDetector = new CascadeClassifier(detectorXml);
    double rst = 99999.0D;
    Mat im = Imgcodecs.imread(filePath);
    Mat gray = new Mat();
    Imgproc.cvtColor(im, gray, 7);
    MatOfRect faceDetections = new MatOfRect();
    faceDetector.detectMultiScale(gray, faceDetections);
    if (faceDetections.elemSize() > 0L)
    {
      Rect[] arrayOfRect;
      int j = (arrayOfRect = faceDetections.toArray()).length;
      for (int i = 0; i < j; i++)
      {
        Rect rect = arrayOfRect[i];
        if (rst > rect.y + rect.height - rect.height * 0.4D) {
          rst = rect.y + rect.height - rect.height * 0.4D;
        }
      }
    }
    if (rst == 99999.0D) {
      rst = 0.0D;
    }
    if (rst > im.size().height / 2.0D) {
      rst = 0.0D;
    }
    return rst;
  }
  
  public static void resize(String inPath, String outPath, String type, int width, int height)
    throws IOException
  {
    BufferedImage im = ImageIO.read(new File(inPath));
    BufferedImage om = new BufferedImage(width, height, im.getType());
    om.getGraphics()
      .drawImage(
      im.getScaledInstance(width, height, 
      16), 0, 0, width, 
      height, null);
    if ((!"jpg".equals(type)) && (!"jpeg".equals(type))) {
      om = convert2Jpeg(om);
    }
    ImageIO.write(om, "jpeg", new File(outPath));
  }
  
  public static String getType(String path)
  {
    if ((path != null) && (path.length() > 0)) {
      return path.replaceAll("^.+\\.([^\\.]+)$", "$1").toLowerCase();
    }
    return "";
  }
}