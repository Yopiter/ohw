# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
import numpy as np
import pathlib
import moviepy.editor as mpy
from moviepy.video.io.bindings import mplfig_to_npimage

from libraries import helpfunctions


def plot_Kinetics(timeindex, mean_absMotions, Peaks=None, mark_peaks=False, file_name=None):
    """
        plots graph for beating kinetics "EKG"
    """
    fig_kinetics, ax_kinetics = plt.subplots(1,1)
    fig_kinetics.set_size_inches(11, 7) #16,12  
    
    ax_kinetics.plot(timeindex, mean_absMotions, '-', linewidth = 2) #self.fig_kinetics
    ax_kinetics.set_xlim(left = 0, right = timeindex[-1])
    ax_kinetics.set_ylim(bottom = 0)
    #fig_kinetics.subplots_adjust(bottom = 0.2)
    
    #self.ax.set_title('Beating kinetics', fontsize = 26)
    ax_kinetics.set_xlabel('t [s]', fontsize = 22)
    ax_kinetics.set_ylabel(u'Mean Absolute Motion [\xb5m/s]', fontsize = 22)
    ax_kinetics.tick_params(labelsize = 20)
    
    for side in ['top','right','bottom','left']:
        ax_kinetics.spines[side].set_linewidth(2)              
    
    if (mark_peaks == True): #Peaks["t_peaks_low_sorted"] != None
        # plot peaks, low peaks are marked as triangles , high peaks are marked as circles         
        ax_kinetics.plot(Peaks["t_peaks_low_sorted"], Peaks["peaks_low_sorted"], marker='o', ls="", ms=5, color='r' )
        ax_kinetics.plot(Peaks["t_peaks_high_sorted"], Peaks["peaks_high_sorted"], marker='^', ls="", ms=5, color='r' )  #easier plotting without for loop          
    
    if file_name != None:
        fig_kinetics.savefig(str(file_name), dpi = 300, bbox_inches = 'tight') #, bbox_inches = 'tight', pad_inches = 0.4)
    return fig_kinetics, ax_kinetics

def plot_TimeAveragedMotions(avg_absMotion, avg_MotionX, avg_MotionY, max_avgMotion, savefolder, file_ext):
    colormap_for_all = "jet"    #"inferno"
    
    ###### abs-motion
    fig_avgAmp, ax_avg_Amp = plt.subplots(1,1)
#    w,h = get_figure_size(avg_absMotion, 12)
 #   fig_avgAmp.set_size_inches(w,h)
    fig_avgAmp.set_size_inches(16,12)  
    imshow_Amp_avg = ax_avg_Amp.imshow(avg_absMotion, vmin = 0, vmax = max_avgMotion, cmap=colormap_for_all, interpolation="bilinear")
    cbar = fig_avgAmp.colorbar(imshow_Amp_avg)
    cbar.ax.tick_params(labelsize=16)     

    for l in cbar.ax.yaxis.get_ticklabels():
        l.set_weight("bold")    
      
    ax_avg_Amp.set_title('Average Motion [µm/s]', fontsize = 16, fontweight = 'bold')
    ax_avg_Amp.axis('off')

    outputpath = str(savefolder / ('TimeAveraged_totalMotion' + file_ext))
    fig_avgAmp.savefig(outputpath, dpi = 100, bbox_inches = 'tight', pad_inches = 0.4)

    ##### x-motion
    fig_avgMotionX, ax_avgMotionX = plt.subplots(1,1)
    fig_avgMotionX.set_size_inches(16, 12)
    imshow_Amp_avg = ax_avgMotionX.imshow(avg_MotionX, vmin = 0, vmax = max_avgMotion, cmap=colormap_for_all, interpolation="bilinear")
    cbar = fig_avgMotionX.colorbar(imshow_Amp_avg)
    cbar.ax.tick_params(labelsize=16)     

    for l in cbar.ax.yaxis.get_ticklabels():
        l.set_weight("bold")    
      
    ax_avgMotionX.set_title('Average x-Motion [µm/s]', fontsize = 16, fontweight = 'bold')
    ax_avgMotionX.axis('off')

    outputpath = str(savefolder / ('TimeAveraged_xMotion' + file_ext))
    fig_avgMotionX.savefig(outputpath, dpi = 100, bbox_inches = 'tight', pad_inches = 0.4)
    
    
    ##### y-motion
    fig_avgMotionY, ax_avgMotionY = plt.subplots(1,1)
    fig_avgMotionY.set_size_inches(16, 12)
    imshow_Amp_avg = ax_avgMotionY.imshow(avg_MotionY, vmin = 0, vmax = max_avgMotion, cmap=colormap_for_all, interpolation="bilinear")
    cbar = fig_avgMotionY.colorbar(imshow_Amp_avg)
    cbar.ax.tick_params(labelsize=16)     

    for l in cbar.ax.yaxis.get_ticklabels():
        l.set_weight("bold")    
      
    ax_avgMotionY.set_title('Average y-Motion [µm/s]', fontsize = 16, fontweight = 'bold')
    ax_avgMotionY.axis('off')

    outputpath = str(savefolder / ('TimeAveraged_yMotion' + file_ext))
    fig_avgMotionY.savefig(outputpath, dpi = 100, bbox_inches = 'tight', pad_inches = 0.4)
    
def save_heatmap(ohw_dataset, savepath, singleframe = False, *args, **kwargs):
    """
        saves either the selected frame (singleframe = framenumber) or the whole heatmap video (=False)
    """
    absMotions = ohw_dataset.absMotions
    
    savefig_heatmaps, saveax_heatmaps = plt.subplots(1,1)
    savefig_heatmaps.set_size_inches(16,12) 
    saveax_heatmaps.axis('off')
    
    scale_max = helpfunctions.get_scale_maxMotion2(absMotions)
    imshow_heatmaps = saveax_heatmaps.imshow(absMotions[0], vmin = 0, vmax = scale_max, cmap = "jet", interpolation="bilinear")#  cmap="inferno"
    
    cbar_heatmaps = savefig_heatmaps.colorbar(imshow_heatmaps)
    cbar_heatmaps.ax.tick_params(labelsize=20)
    for l in cbar_heatmaps.ax.yaxis.get_ticklabels():
        l.set_weight("bold")
    saveax_heatmaps.set_title('Motion [µm/s]', fontsize = 16, fontweight = 'bold')
    
    '''
    if keyword == None:
        path_heatmaps = self.analysis_meta["results_folder"]/ "heatmap_results"
    elif keyword == 'batch':
        path_heatmaps = subfolder / "heatmap_results"
    '''
    savepath.mkdir(parents = True, exist_ok = True) #create folder for results if it doesn't exist
    
    if singleframe != False:
    # save only specified frame
        imshow_heatmaps.set_data(absMotions[singleframe])
        
        heatmap_filename = str(savepath / ('heatmap_frame' + str(singleframe) + '.png'))
        savefig_heatmaps.savefig(heatmap_filename, bbox_inches = "tight", pad_inches = 0)
    
    else:
    # save video
        fps = ohw_dataset.videometa["fps"]
        
        def make_frame_mpl(t):

            frame = int(round(t*fps))
            imshow_heatmaps.set_data(absMotions[frame])

            return mplfig_to_npimage(savefig_heatmaps) # RGB image of the figure
        
        heatmap_filename = str(savepath / 'heatmapvideo.mp4')
        duration = 1/fps * absMotions.shape[0]
        animation = mpy.VideoClip(make_frame_mpl, duration=duration)
        # animation.resize((1500,800))
        animation.write_videofile(heatmap_filename, fps=fps)
        
        

def save_quivervid3(ohw_dataset, savepath, singleframe = False, skipquivers = 1, t_cut = 0, *args, **kwargs):
    """
        saves a video with the normal beating, beating + quivers and velocity trace
        or a single frame with the same three views
    """
    
    absMotions, unitMVs = ohw_dataset.absMotions, ohw_dataset.unitMvs   
    timeindex = ohw_dataset.timeindex
    scale_max = helpfunctions.get_scale_maxMotion2(absMotions)   
    MV_zerofiltered = Filters.zeromotion_to_nan(unitMVs, copy=True)
    MV_cutoff = Filters.cutoffMVs(MV_zerofiltered, max_length = scale_max, copy=True)
    
    MotionX = self.MV_cutoff[:,0,:,:]
    MotionY = self.MV_cutoff[:,1,:,:]

    blockwidth = ohw_dataset.analysis_meta["MV_parameters"]["blockwidth"]
    self.MotionCoordinatesX, self.MotionCoordinatesY = np.meshgrid(
            np.arange(blockwidth/2, self.scaledImageStack.shape[2], blockwidth), 
            np.arange(blockwidth/2, self.scaledImageStack.shape[1], blockwidth))        
       
    #prepare figure
    outputfigure = plt.figure(figsize=(14,10), dpi = 150)#figsize=(6.5,12)

    gs = gridspec.GridSpec(3,2, figure=outputfigure)
    gs.tight_layout(outputfigure)
    #plt.tight_layout()
    
    saveax_video = outputfigure.add_subplot(gs[0:2, 0])
    saveax_video.axis('off')        
    
    saveax_quivers = outputfigure.add_subplot(gs[0:2, 1])
    saveax_quivers.axis('off')

    saveax_trace = outputfigure.add_subplot(gs[2,:])
    saveax_trace.plot(timeindex, ohw_dataset.mean_absMotions, '-', linewidth = 2)
    
    saveax_trace.set_xlim(left = 0, right = timeindex[-1])
    saveax_trace.set_ylim(bottom = 0)
    saveax_trace.set_xlabel('t [s]', fontsize = 22)
    saveax_trace.set_ylabel(u'$\mathrm{\overline {v}}$ [\xb5m/s]', fontsize = 22)
    saveax_trace.tick_params(labelsize = 20)

    for side in ['top','right','bottom','left']:
        saveax_trace.spines[side].set_linewidth(2) 
    
    self.marker, = saveax_trace.plot(timeindex[0],self.mean_absMotions[0],'ro')
    
    #savefig_quivers, saveax_quivers = plt.subplots(1,1)
    #savefig_quivers.set_size_inches(8, 10)
    #saveax_quivers.axis('off')   

    ###### prepare video axis
    imshow_video = saveax_video.imshow(self.scaledImageStack[0], vmin = self.videometa["Blackval"], vmax = self.videometa["Whiteval"], cmap = "gray")
    
    qslice=(slice(None,None,skipquivers),slice(None,None,skipquivers))
    distance_between_arrows = blockwidth * skipquivers
    arrowscale = 1 / (distance_between_arrows / scale_max)
           
    imshow_quivers = saveax_quivers.imshow(self.scaledImageStack[0], vmin = self.videometa["Blackval"], vmax = self.videometa["Whiteval"], cmap = "gray")
    # adjust desired quiver plotstyles here!
    quiver_quivers = saveax_quivers.quiver(self.MotionCoordinatesX[qslice], self.MotionCoordinatesY[qslice], self.MotionX[0][qslice], self.MotionY[0][qslice], pivot='mid', color='r', units ="xy", scale_units = "xy", angles = "xy", scale = arrowscale,  width = 4, headwidth = 3, headlength = 5, headaxislength = 5, minshaft =1.5) #width = 4, headwidth = 2, headlength = 3
    #saveax_quivers.set_title('Motion [µm/s]', fontsize = 16, fontweight = 'bold')

    path_quivers = self.analysis_meta["results_folder"] / "quiver_results"
    path_quivers.mkdir(parents = True, exist_ok = True) #create folder for results

    # parameters for cropping white border in output video
    sizex, sizey = outputfigure.get_size_inches()*outputfigure.dpi
    bbox = outputfigure.get_tightbbox(outputfigure.canvas.get_renderer())
    bbox_bounds_px = np.round(np.asarray(bbox.extents*outputfigure.dpi)).astype(int)

    # to do: introduce min/max to be on the safe side!
    # reverse for np indexing
    bbox_bounds_px[3] = sizey - bbox_bounds_px[1]#y1
    bbox_bounds_px[1] = sizey - bbox_bounds_px[3]#y0

    bbox_bounds_px[2] = sizex - bbox_bounds_px[0]#x1
    bbox_bounds_px[0] = sizex - bbox_bounds_px[2]#x0

    # save only specified frame       
    if not isinstance(singleframe, bool):
        imshow_quivers.set_data(self.scaledImageStack[singleframe])
        imshow_video.set_data(self.scaledImageStack[singleframe])
        quiver_quivers.set_UVC(self.MotionX[singleframe][qslice], self.MotionY[singleframe][qslice])
        
        self.marker.remove()
        self.marker, = saveax_trace.plot(self.timeindex[singleframe],self.mean_absMotions[singleframe],'ro')
        self.marker.set_clip_on(False)
            
        outputfigure.savefig(str(path_quivers / ('quiver3_frame' + str(singleframe) + '.png')))
              
    else:
        # save video
        def make_frame_mpl(t):
            #calculate the current frame number:
            frame = int(round(t*self.videometa["fps"]))
            
    #               if len(self.timeindex) > frame:
    #                   print('Frame: {}, Timeindex: {}'.format(frame, self.timeindex[frame]))
            imshow_quivers.set_data(self.scaledImageStack[frame])
            imshow_video.set_data(self.scaledImageStack[frame])
            
            try:
                quiver_quivers.set_UVC(self.MotionX[frame][qslice], self.MotionY[frame][qslice])
                
                self.marker.remove()
                self.marker, = saveax_trace.plot(self.timeindex[frame],self.mean_absMotions[frame],'ro')
                self.marker.set_clip_on(False)
            except Exception:
                pass
            
            return mplfig_to_npimage(outputfigure)[bbox_bounds_px[1]:bbox_bounds_px[3],bbox_bounds_px[0]:bbox_bounds_px[2]] # RGB image of the figure  #150:1450,100:1950
            
    #               else:
    #                   return
            # slicing here really hacky! find better solution!
            # find equivalent to bbox_inches='tight' in savefig
            # mplfig_to_npimage just uses barer canvas.tostring_rgb()
            # -> check how bbox_inches works under the hood
            # -> in print_figure:
            # if bbox_inches:
            # call adjust_bbox to save only the given area
        
        quivers_filename = str(path_quivers / 'quivervideo3.mp4')
        duration = 1/self.videometa["fps"] * self.MotionX.shape[0]
        animation = mpy.VideoClip(make_frame_mpl, duration=duration)
        
        #cut clip if desired by user
        animation_to_save = self.cut_clip(clip_full=animation, t_cut=t_cut)
       
        animation_to_save.write_videofile(quivers_filename, fps=self.videometa["fps"])