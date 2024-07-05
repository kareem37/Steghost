const express = require('express');
const multer = require('multer');
const path = require('path');

const app = express();
const port = 3000;

// Set up storage for uploaded files
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + '-' + file.originalname);
    }
});

const upload = multer({ storage: storage });

// Serve static files from the "public" directory
app.use(express.static('public'));

// Serve the upload form at the root URL
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'encode-image.html'));
});

// Endpoint to handle image file upload
app.post('/upload-image', upload.single('image'), (req, res) => {
    if (req.file) {
        res.json({ message: 'Image file uploaded successfully', fileName: req.file.filename });
    } else {
        res.status(400).json({ message: 'No file uploaded' });
    }
});

// Endpoint to handle data file upload
app.post('/upload-data', upload.single('data'), (req, res) => {
    if (req.file) {
        res.json({ message: 'Data file uploaded successfully', fileName: req.file.filename });
    } else {
        res.status(400).json({ message: 'No file uploaded' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
