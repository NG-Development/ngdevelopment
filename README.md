# NGDevelopment
2D and 3D visualizations of static models

## Running our Official Release v1.0.0

### Support for Windows users only

 1. Download and extract **Source code (zip)** under release v1.0.0

 2. Extract the file anywhere you'd like. 
 
 4. Locate the **CEESIM Visualizer.zip** and extract that folder to your desktop.
 
 3. Locate and double click on **UI.exe** to demo our newest release.
 
### Models and Antennas

 1. We have a few sample models for you to look at. You're also free to download your own models, we currently have support for .obj,        .vtk, .stl, and .ply.
 
 2. After you press **File** > **Import Plane Model** you can choose from a couple sample models under the **models** folder. 
 
 3. You can import Antenna Locations via a CSV file. This can be done by clicking **File** > **Import Antennas**. (Currently we only have     a sample CSV file that matches with the **F16.stl** plane model.) We have added the ability to modify antenna locations through user input. Details on how to do so found below.
 
 ### Add-on features
 
 1. We have added the ability to **Add a new antenna** through user input. 
    
    a. To do so please click the **Antennas** button on the top left and click **Add Antenna**, a popup-dialog will appear for you to            enter the x,y,z values as well as the orientation of the antenna
    
    b. **Please note:** the x,y,z coordinates you input should be in meters based on the specifications of the plane model you have            selected. The orientation should be values >= -360 and <= 360. (You can take a look at our sample CSV file located under the            **Antenna Locations** folder for reference for what the values should look like.)
    
 2. We have added the ability to **Remove Antennas** through user input. 
    
    a. To do so please click the **Antennas** button on the top left and click **Remove Antenna**, a popup-dialog will appear for you to        enter the x,y,z values of the Antenna you want to remove from the model.
    
    b. **Please note:** the x,y,z coordinates you input should be in meters based on the specifications of the plane model you have            selected.
 
 3. We have added the ability to **Edit an existing antenna** through user input. 
    
    a. To do so please click the **Antennas** button on the top left and click **Edit Antenna**, a popup-dialog will appear for you to       enter the x,y,z values as well as the orientation of the original antenna you want to replace. You will then enter the x,y,z and         orientation values you want to change the antenna to.
    
    b. **Please note:** the x,y,z coordinates you input should be in meters based on the specifications of the plane model you have            selected. The orientation should be values >= -360 and <= 360. (You can take a look at our sample CSV file located under the            **Antenna Locations** folder for reference for what the values should look like.)
