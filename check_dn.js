const XLSX = require('xlsx');

const filePath = '/Users/database-zuma/.openclaw/media/inbound/59084663-0706-486e-a250-c3e93a939611.xlsx';
const workbook = XLSX.readFile(filePath);

console.log('=== SHEET NAMES ===');
console.log(workbook.SheetNames);

workbook.SheetNames.forEach(sheetName => {
  console.log(`\n=== SHEET: ${sheetName} ===`);
  const sheet = workbook.Sheets[sheetName];
  const data = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: '' });
  
  console.log(`Total rows: ${data.length}`);
  console.log('\nFirst 15 rows:');
  data.slice(0, 15).forEach((row, i) => {
    console.log(`Row ${i}:`, row);
  });
});
