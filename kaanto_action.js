// Script 1: Apply first set of actions (Edit existing files)

// Specify the folder containing the files
var inputFolder = Folder.selectDialog("Select the folder with images to process");
if (inputFolder != null) {
    var fileList = inputFolder.getFiles(/\.(jpg|jpeg|tif|tiff|psd|png)$/i); // Adjust file extensions as needed

    // Define the first set of actions to run
    var actions = [
        { actionSet: "AATK 4-väri", actionName: "1a" },  // Replace with your first Action Set name and Action name
       
        // Add more actions here if needed for the first set
    ];

    for (var i = 0; i < fileList.length; i++) {
        var file = fileList[i];
        if (file instanceof File) {
            open(file);

            // Ensure the document is open
            if (app.documents.length > 0) {
                var doc = app.activeDocument;

                // Run each action in the actions array
                for (var j = 0; j < actions.length; j++) {
                    var action = actions[j];
                    app.doAction(action.actionName, action.actionSet);
                }

                // Save the file (overwrite existing file)
                var saveOptions = new TiffSaveOptions();
                saveOptions.embedColorProfile = true;
                saveOptions.alphaChannels = true;
                saveOptions.layers = true;
                saveOptions.imageCompression = TIFFEncoding.NONE; // No compression, adjust as needed

                doc.saveAs(file, saveOptions, true, Extension.LOWERCASE);

                // Close the document without saving changes again
                doc.close(SaveOptions.DONOTSAVECHANGES);
            }
        }
    }
}
