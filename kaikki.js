// Function to run Photoshop actions on a folder of images
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
}

// Function to execute a batch file that runs Python scripts
function runPythonScriptBatch(batchFilePath) {
    var cmdFile = new File(batchFilePath);
    cmdFile.execute();
}

// Run the workflow function
function runWorkflow() {
    // Specify the folders and actions
    var inputFolder = Folder.selectDialog("Select the folder with images to process");
    var outputFolder = new Folder("Z:/lsb-scripts/output"); // Adjust output folder as needed

    // Run Python script batch file
    var pythonBatchFilePath = "Z:/lsb-scripts/run_python_script.bat";
    runPythonScriptBatch(pythonBatchFilePath);

    // Define the Photoshop actions to run after Python scripts
    var photoshopActions1 = [
        { actionSet: "AATK 4-väri", actionName: "1a" }  // First Photoshop action set after kaantaminen.py
    ];

    var photoshopActions2 = [
        { actionSet: "AATK 4-väri", actionName: "2" }  // Second Photoshop action set after varikorjaus.py
    ];

    // Run Photoshop actions on processed images
    runPhotoshopActions(outputFolder, photoshopActions1);
    runPhotoshopActions(outputFolder, photoshopActions2);

    alert("Workflow complete.");
}

// Run the workflow function
runWorkflow();
