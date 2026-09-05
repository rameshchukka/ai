// install the pdf parsing library: npm install pdf-parse
import { PDFLoader } from '@langchain/community/document_loaders/fs/pdf';

const loader = new PDFLoader('./test.pdf');
const docs = await loader.load();

console.log(docs);
