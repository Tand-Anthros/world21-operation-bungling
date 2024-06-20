"use client";
import { useState } from "react";
import { Box, Button, Heading, Text, Spinner } from "@chakra-ui/react";

// const App = () => {
//   const [elementHtml, setElementHtml] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const fetchElementHtml = async () => {
//     try {
//       console.log("Fetching element HTML...");
//       setLoading(true);
//       const response = await fetch("http://localhost:5000/get-element-html");
//       console.log("Response status:", response.status);
//       const data = await response.json();
//       console.log("Data:", data);
//       setElementHtml(data.element_html);
//     } catch (error) {
//       console.error("Error fetching element HTML:", error);
//       setError("Error fetching element HTML");
//     } finally {
//       setLoading(false);
//     }
//   };
  

//   return (
//     <Box p={4}>
//       <Heading>Element HTML</Heading>
//       <Button onClick={fetchElementHtml} mt={4} colorScheme="blue">
//         Fetch Element HTML
//       </Button>
//       {loading ? (
//         <Spinner size="xl" mt={4} />
//       ) : error ? (
//         <Text color="red.500" mt={4}>
//           {error}
//         </Text>
//       ) : (
//         <Box id="element-html" mt={4} dangerouslySetInnerHTML={{ __html: elementHtml }} />
//       )}
//     </Box>
//   );
// };


const App = () => {
  const [elementHtml, setElementHtml] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchElementHtml = async () => {
    try {
      console.log("Fetching element HTML...");
      setLoading(true);
      const response = await fetch("http://localhost:5000/haechi");
      console.log("Response status:", response.status);
      const data = await response.text();
      console.log("Data:", data);
      setElementHtml(data);
    } catch (error) {
      console.error("Error fetching element HTML:", error);
      setError("Error fetching element HTML");
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <Box p={4}>
      <Heading>Element HTML</Heading>
      <Button onClick={fetchElementHtml} mt={4} colorScheme="blue">
        Fetch Element HTML
      </Button>
      {loading ? (
        <Spinner size="xl" mt={4} />
      ) : error ? (
        <Text color="red.500" mt={4}>
          {error}
        </Text>
      ) : (
        <Box id="element-html" mt={4} dangerouslySetInnerHTML={{ __html: elementHtml }} />
      )}
    </Box>
  );
};


export default App;