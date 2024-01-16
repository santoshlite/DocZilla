const { app, BrowserWindow, ipcMain } = require("electron");
const fs = require("fs");
const path = require("path");

function createWindow() {
  // Create the browser window.
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      enableRemoteModule: true,
      nodeIntegration: true,
      preload: path.join(__dirname, "preload.js"), // Add this line
    },
  });

  //load the index.html from a url
  win.loadURL("http://localhost:3000");

  // Open the DevTools.
  win.webContents.openDevTools();
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(createWindow);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.

  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// IPC event for reading markdown files
ipcMain.on("read-markdown-files", (event) => {
  console.log("IPC event 'read-markdown-files' triggered");
  const sharedDirPath = path.join(
    require("os").homedir(),
    "Documents",
    "GrimoireOutput"
  );
  console.log("Reading from directory:", sharedDirPath);

  fs.readdir(sharedDirPath, (err, files) => {
    if (err) {
      console.error("Error reading directory:", err);
      event.reply("markdown-files-response", { error: err.message });
      return;
    }

    console.log("Found files:", files);
    const markdownFiles = files.filter((file) => file.endsWith(".md"));
    console.log("Filtered markdown files:", markdownFiles);

    const fileContents = markdownFiles.map((file) => {
      const filePath = path.join(sharedDirPath, file);
      console.log("Reading file:", filePath);
      return {
        title: file,
        content: fs.readFileSync(filePath, "utf-8"),
      };
    });

    console.log("Sending file contents back to renderer");
    event.reply("markdown-files-response", fileContents);
  });
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
