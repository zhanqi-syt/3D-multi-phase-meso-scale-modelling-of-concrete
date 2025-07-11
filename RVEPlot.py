import numpy as np

def RVEPlt(matidx, tag):
    try:
        from mayavi import mlab
        MayaTag = 1
    except:
        try:
            import matplotlib.pyplot as plt
            MayaTag = 0
        except:
            MayaTag = -1
            print("No plot packages.")
    def RGBColor(colorval):
        """
        From 0-1 to RGB value
        """
        if colorval<=0.00:
            r = 1.0
            g = 0.0
            b = 0.0
        elif colorval > 0.00 and colorval <= 0.25:
            r = 1.0
            g = colorval/0.25
            b = 0.0
        elif colorval > 0.25 and colorval <= 0.50:
            r = 2.0 - colorval/0.25
            g = 1.0
            b = 0.0
        elif colorval > 0.50 and colorval <= 0.75:
            r = 0.0
            g = 1.0
            b = colorval/0.25 - 2.0
        elif colorval > 0.75 and colorval <= 1.00:
            r = 0.0
            g = 4.0 - colorval/0.25
            b = 1.0
        else:
            r = 0.0
            g = 0.0
            b = 1.0
        return (r, g, b)


    def DrawFrame(x_len=50, y_len=50, z_len=50, lw=0.5, c=(0,0,0), op=1.0):
        """
        Plot the frame
        """
        x_0 = np.zeros(2)-0.5-lw
        y_0 = np.zeros(2)-0.5-lw
        z_0 = np.zeros(2)-0.5-lw

        x_1 = x_0+x_len+lw
        y_1 = y_0+y_len+lw
        z_1 = z_0+z_len+lw

        mlab.plot3d([-0.5-lw, x_len-0.5+lw], y_0, z_0, color=c, tube_radius=lw, opacity=op)
        mlab.plot3d([-0.5-lw, x_len-0.5+lw], y_1, z_1, color=c, tube_radius=lw, opacity=op)
        mlab.plot3d([-0.5-lw, x_len-0.5+lw], y_1, z_0, color=c, tube_radius=lw, opacity=op)
        mlab.plot3d([-0.5-lw, x_len-0.5+lw], y_0, z_1, color=c, tube_radius=lw, opacity=op)

        mlab.plot3d(x_0, y_0, [-0.5-lw, z_len-0.5+lw], color=c, tube_radius=lw, opacity=op)
        mlab.plot3d(x_1, y_1, [-0.5-lw, z_len-0.5+lw], color=c, tube_radius=lw, opacity=op)
        mlab.plot3d(x_0, y_1, [-0.5-lw, z_len-0.5+lw], color=c, tube_radius=lw, opacity=op)
        mlab.plot3d(x_1, y_0, [-0.5-lw, z_len-0.5+lw], color=c, tube_radius=lw, opacity=op)

        mlab.plot3d(x_0, [-0.5-lw, y_len-0.5+lw], z_0, color=c, tube_radius=lw, opacity=op)
        mlab.plot3d(x_1, [-0.5-lw, y_len-0.5+lw], z_1, color=c, tube_radius=lw, opacity=op)
        mlab.plot3d(x_1, [-0.5-lw, y_len-0.5+lw], z_0, color=c, tube_radius=lw, opacity=op)
        mlab.plot3d(x_0, [-0.5-lw, y_len-0.5+lw], z_1, color=c, tube_radius=lw, opacity=op)

    if MayaTag == 1:
        if tag == "PoreIdx":
            lx = matidx.shape[0]
            ly = matidx.shape[1]
            lz = matidx.shape[2]
            azm = 40.0
            eleva = 70.0
            dis = lz*3.5
            fcp = np.array([lx/2-0.5, ly/2-0.5, lz/2-0.5])
            fig = mlab.figure(bgcolor=(1, 1, 1))
            DrawFrame(lx, ly, lz, 0.05, (0, 0, 0), 1.0)
            aggrelist = np.setdiff1d(np.unique(matidx), [-1, -2, -3])
            np.random.seed(20221116)
            rc = np.random.random(len(aggrelist))
            for iagg in range(len(aggrelist)):
                xx, yy, zz = np.where(matidx == aggrelist[iagg])
                print(iagg, "/", len(aggrelist))
                mlab.points3d(xx, yy, zz,
                              mode="cube",
                              color=RGBColor(rc[iagg]),
                              line_width=0,
                              opacity=1.0,
                              scale_factor=1.0,
                              scale_mode='none')
            mlab.view(azimuth=azm, elevation=eleva, distance=dis, focalpoint=fcp)
            mlab.show()
        elif tag == "ITZIdx":
            lx = matidx.shape[0]
            ly = matidx.shape[1]
            lz = matidx.shape[2]
            azm = 40.0
            eleva = 70.0
            dis = lz*3.5
            fcp = np.array([lx/2-0.5, ly/2-0.5, lz/2-0.5])
            mlab.figure(bgcolor=(1, 1, 1))
            DrawFrame(lx, ly, lz, 0.05, (0, 0, 0), 1.0)
            xx, yy, zz = np.where(matidx == -2)
            mlab.points3d(xx, yy, zz,
                          mode="cube",
                          color=(0.78, 0.27, 0.28),
                          line_width=0,
                          opacity=0.2,
                          scale_factor=1.0,
                          scale_mode='none')
            aggrelist = np.setdiff1d(np.unique(matidx), [-1, -2, -3])
            np.random.seed(20221116)
            rc = np.random.random(len(aggrelist))
            for iagg in range(len(aggrelist)):
                xx, yy, zz = np.where(matidx == aggrelist[iagg])
                print(iagg, "/", len(aggrelist)-1)
                mlab.points3d(xx, yy, zz,
                              mode="cube",
                              color=RGBColor(rc[iagg]),
                              line_width=0,
                              opacity=1.0,
                              scale_factor=1.0,
                              scale_mode='none')
            mlab.view(azimuth=azm, elevation=eleva, distance=dis, focalpoint=fcp)
            mlab.show()
        elif tag == "MatIdx":
            ops = [0.01, 0.1, 0.2, 1.0]
            lx = matidx.shape[0]
            ly = matidx.shape[1]
            lz = matidx.shape[2]
            azm = 40.0
            eleva = 70.0
            dis = lz*3.5
            fcp = np.array([lx/2-0.5, ly/2-0.5, lz/2-0.5])
            fig = mlab.figure(bgcolor=(1, 1, 1))
            DrawFrame(lx, ly, lz, 0.05, (0, 0, 0), 1.0)
            xx, yy, zz = np.where(matidx == 0)
            mlab.points3d(xx, yy, zz,
                          mode="cube",
                          color=(0.95, 0.95, 0.95),
                          line_width=0,
                          opacity=ops[0],
                          scale_factor=1.0,
                          scale_mode='none')
            xx, yy, zz = np.where(matidx == 1)
            mlab.points3d(xx, yy, zz,
                          mode="cube",
                          color=(0.45, 0.45, 0.45),
                          line_width=0,
                          opacity=ops[1],
                          scale_factor=1.0,
                          scale_mode='none')
            xx, yy, zz = np.where(matidx == 2)
            mlab.points3d(xx, yy, zz,
                          mode="cube",
                          color=(0.78, 0.27, 0.28),
                          line_width=0,
                          opacity=ops[2],
                          scale_factor=0.9,
                          scale_mode='none')
            xx, yy, zz = np.where(matidx == 3)
            mlab.points3d(xx, yy, zz,
                          mode="cube",
                          # color=(0.15, 0.31, 0.26),
                          # color=(0.352941176470588, 0.717647058823529, 0.831372549019608),
                          color=(0.592156862745098, 0.686274509803922, 0.564705882352941),
                          line_width=0,
                          opacity=ops[3],
                          scale_factor=0.9,
                          scale_mode='none')
            mlab.view(azimuth=azm, elevation=eleva, distance=dis, focalpoint=fcp)
            mlab.show()
        elif tag == "Agg&NonAgg":
            ops = [0.01, 0.1, 0.2, 1.0]
            lx = matidx.shape[0]
            ly = matidx.shape[1]
            lz = matidx.shape[2]
            azm = 40.0
            eleva = 70.0
            dis = lz*3.5
            fcp = np.array([lx/2-0.5, ly/2-0.5, lz/2-0.5])
            fig = mlab.figure(bgcolor=(1, 1, 1))
            DrawFrame(lx, ly, lz, 0.05, (0, 0, 0), 1.0)
            xx, yy, zz = np.where(matidx != 3)
            mlab.points3d(xx, yy, zz,
                          mode="cube",
                          color=(0.45, 0.45, 0.45),
                          line_width=0,
                          opacity=ops[1],
                          scale_factor=1.0,
                          scale_mode='none')
            xx, yy, zz = np.where(matidx == 3)
            mlab.points3d(xx, yy, zz,
                          mode="cube",
                          color=(0.592156862745098, 0.686274509803922, 0.564705882352941),
                          line_width=0,
                          opacity=ops[3],
                          scale_factor=0.9,
                          scale_mode='none')
            mlab.view(azimuth=azm, elevation=eleva, distance=dis, focalpoint=fcp)
            mlab.show()
        elif tag == "RandMat":
            lx = matidx.shape[0]
            ly = matidx.shape[1]
            lz = matidx.shape[2]
            azm = 40.0
            eleva = 70.0
            dis = lz*3.5
            fcp = np.array([lx/2-0.5, ly/2-0.5, lz/2-0.5])
            fig = mlab.figure(bgcolor=(1, 1, 1))
            DrawFrame(lx, ly, lz, 0.05, (0, 0, 0), 1.0)
            xx, yy, zz = np.where(matidx != 10000)
            maxval = np.max(matidx[matidx != 10000])
            maxval = max(maxval, -np.min(matidx[matidx != 10000]))
            mlab.points3d(xx, yy, zz, matidx[matidx != 10000],
                          mode="cube",
                          colormap='gist_rainbow',
                          vmin=-maxval,
                          vmax=maxval,
                          line_width=0,
                          opacity=1.0,
                          scale_factor=1.0,
                          scale_mode='none')
            mlab.view(azimuth=azm, elevation=eleva, distance=dis, focalpoint=fcp)
            mlab.show()
        elif tag == "Pore@NonAgg":
            lx = matidx.shape[0]
            ly = matidx.shape[1]
            lz = matidx.shape[2]
            azm = 40.0
            eleva = 70.0
            dis = lz*3.5
            fcp = np.array([lx/2-0.5, ly/2-0.5, lz/2-0.5])
            fig = mlab.figure(bgcolor=(1, 1, 1))
            DrawFrame(lx, ly, lz, 0.05, (0, 0, 0), 1.0)
            xx, yy, zz = np.where(matidx == 0)
            mlab.points3d(xx, yy, zz,
                          mode="cube",
                          color=(0.20, 0.20, 0.20),
                          line_width=0,
                          opacity=0.2,
                          scale_factor=1.0,
                          scale_mode='none')
            xx, yy, zz = np.where(matidx == 1)
            mlab.points3d(xx, yy, zz,
                          mode="cube",
                          color=(0.8, 0.8, 0.8),
                          line_width=0,
                          opacity=1.0,
                          scale_factor=1.0,
                          scale_mode='none')
            xx, yy, zz = np.where(matidx == 2)
            mlab.points3d(xx, yy, zz,
                          mode="cube",
                          color=(0.8, 0.8, 0.8),
                          line_width=0,
                          opacity=1.0,
                          scale_factor=1.0,
                          scale_mode='none')
            mlab.view(azimuth=azm, elevation=eleva, distance=dis, focalpoint=fcp)
            mlab.show()
    print("-----------------", tag, "Plot Finish-----------------")
    return 1

