document
  .getElementById("Upload")
  .addEventListener("click", function(event){
      event.preventDefault()
      makeRequest()
  });

async function makeRequest() {
    let formData = new FormData();
    formData.append("file", fileUpload.files[0]);
    await fetch('/api/upload', {
      method: "POST",
      body: formData
    });
    alert('The file has been uploaded successfully.');
}