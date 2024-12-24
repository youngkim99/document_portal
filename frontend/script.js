// Select elements from the DOM
const fileListElement = document.getElementById('file-list');
const uploadForm = document.getElementById('upload-form');
const fileUpload = document.getElementById('file-upload');
const pdfContainer = document.getElementById('pdf-container');

const UPLOAD_URL = 'http://localhost:8000/api/documents/upload/';
const DOCUMENT_DETAIL_URL = 'http://localhost:8000/api/documents/';

// Handle file upload form submission
uploadForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('file', fileUpload.files[0]);

    // Send the file to the backend for processing
    fetch(UPLOAD_URL, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Add the uploaded PDF to the list
        
        console.log(data);
        console.log(data.file);
        const listItem = document.createElement('li');
        listItem.className = 'uploaded-file';
        listItem.textContent = data.file.split('/').pop();  // Show the filename
        listItem.addEventListener('click', () => viewDocument(data.id));
        fileListElement.appendChild(listItem);
    })
    .catch(error => {
        console.error('Error uploading file:', error);
    });
});

// Function to view a specific document with its extracted data
function viewDocument(documentId) {
    fetch(`http://localhost:8000/api/documents/${documentId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Display the PDF with highlights and extracted data
            pdfContainer.innerHTML = `<iframe src="http://localhost:8000/media/${data.file}" width="600" height="400"></iframe>`;
            const extractedData = JSON.stringify(data.extracted_data, null, 2);
            pdfContainer.innerHTML += `<pre>${extractedData}</pre>`;
        })
        .catch(error => {
            // Log the error message and response for debugging
            console.error('Error fetching document:', error);
            alert('An error occurred while fetching the document. Please check the console for details.');
        });
}

