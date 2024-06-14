// Specify the folder containing the files
var inputFolder = Folder.selectDialog("Select the folder with images to process");
if (inputFolder != null) {
    var fileList = inputFolder.getFiles(/\.(jpg|jpeg|tif|tiff|psd|png)$/i); // Adjust file extensions as needed

    // Define an array of actions to run
    var actions = [
        { actionSet: "AATK 4-väri", actionName: "1a" }, // Replace with your first Action Set name and Action name
        { actionSet: "AATK 4-väri", actionName: "2"}  // Replace with your second Action Set name and Action name
        // Add more actions here as needed
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

                // Save and close the document
                var saveOptions = new PhotoshopSaveOptions();
                saveOptions.embedColorProfile = true;
                saveOptions.alphaChannels = true;
                saveOptions.layers = true;

                doc.saveAs(file, saveOptions, true, Extension.LOWERCASE);
                doc.close(SaveOptions.DONOTSAVECHANGES);
            }
        }
    }
}
