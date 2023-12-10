console.log("Script run");
let dropArea = document.getElementById("dropzone");
let dropArea_input = document.getElementById("dropzone-file");
let files_loaded = document.getElementById("files-loaded");

const dragEvents = new Array(
  "drag",
  "dragstart",
  "dragend",
  "dragover",
  "dragenter",
  "dragleave",
  "drop",
);

dragEvents.forEach((event) => {
  dropArea.addEventListener(event, (e) => {
    e.preventDefault();
    e.stopPropagation();
  });
});
let globalFiles;
dropArea.addEventListener("drop", function (e) {
  console.log(`Event drop triggered`);
  let dt = e.dataTransfer;
  let files = dt.files;
  globalFiles = files;

  // alert(files[0].name + ": " + files[0].size + " bytes");
  filename.innerText = files[0].name;
  size.innerText = `${Math.round((files[0].size / 1024) * 100) / 100} mb`;
  files_loaded.classList.remove("hidden");
  dropArea.classList.add("hidden");
});
