#!/usr/bin/env python
import roslib,rospy,sys
roslib.load_manifest('ratslam_python')
from cv_bridge import CvBridge,CvBridgeError
import ratslam
import sys
import time
import os, os.path
from numpy import *
from matplotlib.pylab import *
#import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cPickle as pkl
import cv2
from sensor_msgs.msg import Image

def draw_position(x, y):
    scatter(x,y)

def draw_x_y_z(pcmax, xcoord, ycoord, thcoord, subplot):
    ax3 = Axes3D(gcf(), rect=subplot.get_position())
    ax3.scatter(xcoord, ycoord, thcoord, 'z')
    ax3.set_xlim3d([0, 30])
    ax3.set_ylim3d([0, 30])
    ax3.set_zlim3d([0, 36])

def callback(data):
    global i
    global driver
    #rval,image_source=video.read()
    image_source=array(bridge.imgmsg_to_cv(data,"bgr8"))
    image_source=cv2.cvtColor(image_source,cv2.COLOR_BGR2GRAY)
    #print image_source.shape
      
    #driver = ratslam.RatSLAM(image_source)
    #cv2.imshow('Video Feed',image_source)
    #cv2.waitKey(1)
    #print 'hello'
    
    xcoord = []
    ycoord = []
    thcoord = []
    
    last_time = time.time()
    
    n_steps = 21000
    #n_steps = 500
    
    ########################################################################
    #for i in xrange(n_steps):
	
	# option to quit/break cleanly
    
    #cv2.imshow('hello',image_source)
    #cv2.waitKey(1)
    # do a time step of the simulation
    ion()
    cv2.imshow('Video Feed',image_source)
    cv2.waitKey(1)
    driver.evolve(image_source)
    
    # query some values for plotting
    im = driver.current_image
    #cv2.imshow('hello',im)
    
    #cv2.waitKey(1)
    emap = driver.experience_map
    pcmax = driver.current_pose_cell # this is where we are getting the pose cell x,y and theta
    pcall=driver.all_pose_cell # 3d pose cell
    pvall=driver.args_visual_posecells
    odo = driver.current_odo
    current_exp = emap.current_exp
    #match_scores=drriver.match_scores
    #print 'experience',current_exp.x_m
    #print 'odometry',odo[0],odo[1]
    
    xcoord.append(pcmax[0])
    ycoord.append(pcmax[1])
    thcoord.append(pcmax[2])
    
  
	    
    
    #if i % 5 == 0:
    #ion()  
    figure(1)
    print "Plotting..."
    subplot(2,2,1)
    imshow(im, cmap=cm.gray)
    a=gca()
    a.axis('off')
    title('Raw Image')

    subplot(2,2,2)
    draw_position(odo[0], odo[1])
    b = gca()
    title('Raw Odometry')
    #b.set_xlim([-50, 100])
    #b.set_ylim([0, 125])

    pcdata = subplot(2,2,3)
    
    draw_x_y_z(pcmax, xcoord, ycoord, thcoord, pcdata)
    
    title('Pose Cell Activity')
    pcdata.axis('off')

    subplot(2,2,4)
    draw_position(current_exp.x_m, current_exp.y_m)
    title('Experience Map')
    d = gca()
    #draw()
    now = time.time()
    fps = 1.0 / (now - last_time)
    last_time = now
    print "Using frames %i and %i (%f fps ; %f spf)" % (i, i+1, fps, 1.0/fps)
    global drive_all_pose_cell
    hold(1)
    figure(2)
    total_dist=[]
    global total_dist_sum
    #print 'no of cells activated', driver.all_pose_cell.shape[0]
    for j in range(driver.all_pose_cell.shape[0]):
      #inital_pose_cell=driver.all_pose_cell[j]
      z_dist=np.minimum(np.abs(driver.all_pose_cell[j][0]-driver.all_pose_cell[0][0]),36-np.abs(driver.all_pose_cell[j][0]-driver.all_pose_cell[0][0]))
      x_dist=np.minimum(np.abs(driver.all_pose_cell[j][1]-driver.all_pose_cell[0][1]),36-np.abs(driver.all_pose_cell[j][0]-driver.all_pose_cell[0][0]))
      y_dist=np.minimum(np.abs(driver.all_pose_cell[j][2]-driver.all_pose_cell[0][2]),36-np.abs(driver.all_pose_cell[j][2]-driver.all_pose_cell[0][2]))
      total_dist.append(np.sqrt(np.power(x_dist,2)+np.power(y_dist,2)+np.power(z_dist,2)))
    total_dist_sum.append(sum(total_dist)/driver.all_pose_cell.shape[0])
    #print driver.all_pose_cell
    #print 'next'
    drive_all_pose_cell.append(driver.all_pose_cell.shape[0])
   # print 'all the pose cells are',drive_all_pose_cell
    
    global match
    global total_y
    global difference_pose_cells
    '''
    if pvall[0]==0 and pvall[1]==0 and pvall[2]==0:
      match.append(0)
    else:
      match.append(1)
    '''
    y=2
    match.append(min(driver.match_scores)*10)
    total_y.append(y)
    plot(match)
    difference_pose_cells.append(driver.all_pose_cell.shape[0])
    if len(difference_pose_cells)==1:
      diff=0
    else:
      diff=abs(difference_pose_cells[len(difference_pose_cells)-1]-driver.all_pose_cell.shape[0])
    plot(diff)
    #y=2
    plot(total_y)
    figure(3)
    plot(total_dist_sum)
    
    #draw()
    #i=i+1
    #print i
    '''
    hold(1)
    figure(2)
    ax=subplot(111,projection='3d')
    driver.posecells_1=sum(driver.posecells_1,2)
    print driver.posecells_1.shape
    for j in range(pcall.shape[0]):
	    k=pcall[j]
	    ax.scatter(k[0],k[1],driver.posecells_1[k[0]][k[1]])
	    
	    #ax.set_zlim3d([0, 36])
	    #print driver.posecells_1[abs(pcmax[0])][abs(pcmax[1])]
	    ax.scatter(pcmax[0],pcmax[1],driver.posecells_1[pcmax[0]][pcmax[1]],'r')
	    ax.set_xlim3d([0, 30])
	    ax.set_ylim3d([0, 30])
	    ax.set_xlabel('X label')
	    ax.set_ylabel('Y Label')
	    ax.set_zlabel('Z label')
    
    figure(4)
    ax=subplot(111,projection='3d')
    for j in range(pcall.shape[0]):
	    k=pcall[j]
	    ax.scatter(k[0],k[1],k[2])
	    
	    #ax.set_zlim3d([0, 36])
	    #print driver.posecells_1[abs(pcmax[0])][abs(pcmax[1])]
	    ax.scatter(pcmax[0],pcmax[1],pcmax[2],'r')
	    ax.set_xlim3d([0, 30])
	    ax.set_ylim3d([0, 30])
	    ax.set_zlim3d([0,36])
	    ax.set_xlabel('X label')
	    ax.set_ylabel('Y Label')
	    ax.set_zlabel('Z label')	
    figure(3)
    ad=subplot(111,projection='3d')
    ad.scatter(pvall[0],pvall[1],pvall[2])
    ad.set_xlim3d([0, 30])
    ad.set_ylim3d([0, 30])
    ad.set_zlim3d([0, 36])

    ad.set_xlabel('X label')
    ad.set_ylabel('Y Label')
    ad.set_xlabel('Z label')
    '''
    draw()
      
    
    #plt.figure(2)
    #ax=plt.subplot(111,projection='3d')
    #ax.scatter(pcall,pcall,pcall)
    
    #plt.draw()
    
    
   # print i
            #savefig(os.path.join(output_path, 'output%06i.png' % i))
            #d.set_xlim([-50, 100])
            #d.set_ylim([0, 120])
'''  

def main(): 
    # TODO use argparse
    #video_path = sys.argv[1]
    
    #image_source = ratslam.VideoSource(video_path, grayscale=True)
    #video=cv2.VideoCapture('/home/rohan/Downloads/video002.mp4')
'''    

    

############################################################################

if __name__ == "__main__":
    #output_path = sys.argv[1]
    i=0
    drive_all_pose_cell=[]
    pkl_state = False
    wait_for_key = False
    total_dist_sum=[]
    difference_pose_cells=[]
    match=[]
    total_y=[]
    bridge=CvBridge()
    
    driver = ratslam.RatSLAM(np.ones((480,640),'uint8'))
    topic_camera='usb_cam/image_raw'#'image_raw/image_decompressed'
    #image_source=cv2.imread('/home/rohan/camera.jpg',0)
    #driver=ratslam.RatSLAM(image_source)
    print 'done'
    image_sub=rospy.Subscriber(topic_camera,Image,callback)
    rospy.init_node('ratslam-python')
    print "about to spin"
    
    rospy.spin()
    #main()
