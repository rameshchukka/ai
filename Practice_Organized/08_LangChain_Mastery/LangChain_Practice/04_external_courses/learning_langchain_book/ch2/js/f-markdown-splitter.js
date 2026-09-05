import { RecursiveCharacterTextSplitter } from '@langchain/textsplitters';

const markdownText = ` # 🦜🔗 LangChain ⚡ Building applications with LLMs through composability ⚡ ## Quick Install \`\`\`bash pip install langchain \`\`\` As an open source project in a rapidly developing field, we are extremely open to contributions. `;

const mdSplitter = RecursiveCharacterTextSplitter.fromLanguage('markdown', {
  chunkSize: 60,
  chunkOverlap: 0,
});

const mdDocs = await mdSplitter.createDocuments(
  [markdownText],
  [{ source: 'https://www.langchain.com' }]
);

console.log(mdDocs);
