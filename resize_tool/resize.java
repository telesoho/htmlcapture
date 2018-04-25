package jp.co.uclgroup;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.math.BigDecimal;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import javax.imageio.ImageIO;
import jp.co.uclgroup.util.ImageUtil;

public class Resize
{
  public static void main(String[] args)
  {
    if ((args == null) || (args.length < 4))
    {
      writeLog(3, "������������������1������(���������������������) ���2������(������������������) ���3������(���������������������) ���4������(������������������������)");
      return;
    }
    String folderin = args[0];
    String folderout = args[1];
    if (!folderout.endsWith("\\")) {
      folderout = folderout + "\\";
    }
    boolean resizeFlg = false;
    if ("true".equals(args[2].toLowerCase())) {
      resizeFlg = true;
    }
    boolean trimmingFlg = false;
    if ("true".equals(args[3].toLowerCase())) {
      trimmingFlg = true;
    }
    if ((!resizeFlg) && (!trimmingFlg))
    {
      writeLog(2, "������������������������������������������������������������������������������������������");
      return;
    }
    List<File> fileList = ImageUtil.fileList(folderin, true);
    writeLog(1, "���������������" + fileList.size());
    if (!fileList.isEmpty())
    {
      File inFolder = new File(folderin);
      File outFolder = new File(folderout);
      for (File f : fileList) {
        try
        {
          writeLog(1, "���������" + f.getName());
          BufferedImage im = ImageIO.read(f);
          int width = im.getWidth();
          int height = im.getHeight();
          if (width != 790)
          {
            height = getSize(height, width, 790);
            width = 790;
          }
          String outPath = getOutFolder(f, inFolder, outFolder);
          String outFile = getJpegPath(outPath + f.getName());
          String srcType = ImageUtil.getType(f.getName());
          boolean deleteFlg = false;
          if (resizeFlg)
          {
            ImageUtil.resize(f.getAbsolutePath(), outFile, srcType, 
              width, height);
            deleteFlg = true;
          }
          else if ((!"jpg".equals(srcType)) || (!"jpeg".equals(srcType)))
          {
            ImageUtil.convert2Jpeg(im, outFile);
            deleteFlg = true;
          }
          else
          {
            outFile = f.getAbsolutePath();
          }
          if (trimmingFlg)
          {
            ImageUtil.trimmingAll(outFile, outPath, f.getName()
              .replaceAll("\\..+$", ""), "jpeg", 790, 1540);
            if (deleteFlg)
            {
              File tempFile = new File(outFile);
              tempFile.delete();
            }
          }
        }
        catch (IOException e)
        {
          e.printStackTrace();
        }
      }
    }
    writeLog(1, "���������������" + fileList.size());
  }
  
  private static String getOutFolder(File inFile, File inFolder, File outFolder)
  {
    String out = outFolder.getAbsolutePath();
    String in = inFolder.getAbsolutePath();
    
    String inPath = inFile.getParent();
    if (!out.endsWith("\\")) {
      out = out + "\\";
    }
    if (!inPath.endsWith("\\")) {
      inPath = inPath + "\\";
    }
    if (!in.endsWith("\\")) {
      in = in + "\\";
    }
    out = inPath.replace(in, out);
    File outF = new File(out);
    outF.mkdirs();
    
    return out;
  }
  
  private static void writeLog(int level, String message)
  {
    StringBuffer log = new StringBuffer();
    if (level == 1) {
      log.append("[INFO] ");
    } else if (level == 2) {
      log.append("[WARN] ");
    } else if (level == 3) {
      log.append("[ERROR] ");
    }
    log.append(new SimpleDateFormat("yyyy/MM/dd HH:mm:ss").format(new Date())).append(" ");
    log.append(message);
    System.out.println(log);
  }
  
  private static String getJpegPath(String inPath)
  {
    String outPath = inPath
      .replace("." + ImageUtil.getType(inPath), ".jpg");
    return outPath;
  }
  
  private static int getSize(int i1, int i2, int i3)
  {
    BigDecimal b1 = new BigDecimal(i1);
    BigDecimal b2 = new BigDecimal(i2);
    BigDecimal b3 = new BigDecimal(i3);
    BigDecimal br = b1.divide(b2, 10, 4)
      .multiply(b3);
    return br.intValue();
  }
}
