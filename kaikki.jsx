function runPhotoshopActions(inputFolder, actions) {
    if (inputFolder != null) {
        var fileList = inputFolder.getFiles(/\.(jpg|jpeg|tif|tiff|psd|png)$/i); // Adjust file extensions as needed

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
                        try {
                            app.doAction(action.actionName, action.actionSet);
                        } catch (e) {
                            alert("Error playing action: " + action.actionName + " from set: " + action.actionSet + "\n" + e);
                        }
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
}

// Function to execute a shell script that runs Python scripts
function runPythonScriptShell(shellFilePath) {
    try {
        var result = app.system(shellFilePath);
        alert("Shell script executed: " + result);
    } catch (e) {
        alert("Error executing shell script: " + e);
    }
}

// Run the workflow function
function runWorkflow() {
    // Specify the folders and actions
    var outputFolder = new Folder("/Users/joeltikkanen/Documents/lsb/output"); // Adjust output folder as needed

    // Define the Photoshop actions to run after Python scripts
    var photoshopActions1 = [
        { actionSet: "AATK", actionName: "1a" }  // First Photoshop action set after kaantaminen.py
    ];

    var photoshopActions2 = [
        { actionSet: "AATK", actionName: "2" }  // Second Photoshop action set after varikorjaus.py
    ];

    // Run Photoshop actions on processed images
    runPhotoshopActions(outputFolder, photoshopActions1);
    runPhotoshopActions(outputFolder, photoshopActions2);

    alert("Workflow complete.");
}

// Run the workflow function
runWorkflow();
