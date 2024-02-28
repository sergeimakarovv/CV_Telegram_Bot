// myscript.js
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const filename = process.argv[2]; // Get the input argument

  const browser = await puppeteer.launch({ headless: 'new',  args: ['--no-sandbox', '--disable-setuid-sandbox'] }); // Use the new Headless mode
  const page = await browser.newPage();

  // Get the directory of the script
  const scriptDir = __dirname;

  // Construct the file path for index.html in the same directory
  const filePath = path.join(scriptDir, 'tmp_resume_file.html');
  const fileUrl = `file://${filePath}`;

  await page.goto(fileUrl, { waitUntil: 'networkidle0' });

  // Replace 'output.pdf' with the desired output PDF file path
  await page.pdf({ path: filename, format: 'A4' }); // Use the filename passed as an argument

  await browser.close();
})();
