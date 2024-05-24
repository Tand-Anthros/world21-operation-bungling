import { ChakraProvider, Button, Text } from "@chakra-ui/react";

// export default function Home() {
//   return (
//     <ChakraProvider>
//       <Text>мир 21: "операция головопятсятво"</Text>
//       <Button>Батон</Button>
//     </ChakraProvider>
//   );
// }


import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import './index.css';

const App: React.FC = () => {
  const [url, setUrl] = useState<string>('');
  const [response, setResponse] = useState<string>('');

  const handleButtonClick = async () => {
    try {
      const res = await fetch(`http://localhost:3001/open?url=${encodeURIComponent(url)}`);
      const text = await res.text();
      setResponse(text);
    } catch (error) {
      // @ts-ignore
      setResponse(`Error: ${error.message}`);
    }
  };

  return (
    <div>
      <h1>Open URL in Puppeteer</h1>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter URL"
      />
      <button onClick={handleButtonClick}>Open URL</button>
      <p>{response}</p>
    </div>
  );
};

ReactDOM.render(<App />, document.getElementById('root'));
