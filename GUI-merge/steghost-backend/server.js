const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 3000;

// Set up multer for file uploads
const upload = multer({ dest: 'uploads/' });

app.use(express.static('public')); // Serve static files from the 'public' directory

// Route to serve the HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'encode-image.html')); // Specify the HTML file to serve
});

// Route to handle image upload
app.post('/upload-image', upload.single('image'), (req, res) => {
    const imageFilePath = req.file.path;
    const originalImageName = req.file.originalname;
    res.json({ imageFilePath, originalImageName });
});

// Route to handle data upload and embedding
app.post('/upload-data', upload.single('data'), (req, res) => {
    const dataFilePath = req.file.path;
    const imageFilePath = req.body.imageFilePath; // Assume image path is sent in the request body

    // Execute the Python script
    exec(`python embed.py ${imageFilePath} ${dataFilePath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            console.error(`stderr: ${stderr}`);
            return res.status(500).json({ error: 'Failed to embed data in the image', details: stderr });
        }

        console.log(`stdout: ${stdout}`);

        const embeddedImagePath = path.join(__dirname, 'uploads', 'embedded_image.png');
        if (fs.existsSync(embeddedImagePath)) {
            res.json({ embeddedImagePath: `/uploads/embedded_image.png` });
        } else {
            res.status(500).json({ error: 'Embedded image not found' });
        }
    });
});

// Route to serve the embedded image
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
