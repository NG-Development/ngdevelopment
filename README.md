# NGDevelopment
2D and 3D visualizations of static models

## Running our update release with an add-on feature for v0.4.0

### Support for Windows users only

 1. Download and extract **Source code (zip)** under release v0.4.0

 2. Extract the file anywhere you'd like. 
 
 3. Double click on **UI.exe** to demo our newest release.
 
### Models and Antennas

 1. We have a few sample models for you to look at. You're also free to download your own models, we currently have support for .obj,        .vtk, .stl, and .ply.
 
 2. After you press **File** > **Import Plane Model** you can choose from a couple sample models under the **models** folder. 
 
 3. You can import Antenna Locations via a CSV file. This can be done by clicking **File** > **Import Antennas**. (Currently we only have     a sample CSV file that matches with the **F16.stl** plane model.) You are welcome to create your own CSV file to add your own custom       antenna locations. The format follows the x, y, z values and orientation in the first, second, third, and fourth columns respectively. 
 
 ### Add-on features
 
 1. We have added the ability to **Add a new antenna** through user input. 
    
    a. To do so please click the **Add Antenna** button on the top left and 4 Dialogs will appear for you to enter the x,y,z values as            well as the orientation of the antenna
    
    b. **Please note:** the x,y,z coordinates you input should be in meters based on the specifications of the plane model you have              selected. The orientation should be values >= -180 and <= 180. (You can take a look at our sample CSV file located under the              **Antenna Locations** folder for reference for what the values should look like.)
    
 2. We've also added the ability to **Display coordinates** of antennas (via their x,y,z coordinates on the renderer)
