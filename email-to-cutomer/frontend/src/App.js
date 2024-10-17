import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [language, setLanguage] = useState('English');
  const [question, setQuestion] = useState('');
  const [subject, setSubject] = useState('');
  const [answer, setAnswer] = useState('');
  const [sentiment, setSentiment] = useState('');
  const [summary, setSummary] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [translateComment, setTranslateComment] = useState(false); 
  const [translateEmail, setTranslateEmail] = useState(false);    

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    const requestBody = {
      comment: question,
      language: language,
      translate_comment: translateComment,  
      translate_email: translateEmail,      
    };

    try {
      const response = await axios.post(`/generate_email`, requestBody, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      setSubject(response.data.subject);
      setAnswer(response.data.email);
      setSentiment(response.data.sentiment);
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error generating email:', error);
      setError('An error occurred while generating the email. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="language-selector">
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="English">English</option>
          <option value="Spanish">Spanish</option>
          <option value="French">French</option>
          <option value="German">German</option>
          <option value="Italian">Italian</option>
          <option value="Portuguese">Portuguese</option>
          <option value="Dutch">Dutch</option>
          <option value="Russian">Russian</option>
          <option value="Chinese">Chinese (Simplified and Traditional)</option>
          <option value="Japanese">Japanese</option>
          <option value="Korean">Korean</option>
          <option value="Arabic">Arabic</option>
          <option value="Hindi">Hindi</option>
          <option value="Bengali">Bengali</option>
          <option value="Urdu">Urdu</option>
          <option value="Turkish">Turkish</option>
          <option value="Vietnamese">Vietnamese</option>
          <option value="Thai">Thai</option>
          <option value="Hebrew">Hebrew</option>
          <option value="Greek">Greek</option>
          <option value="Polish">Polish</option>
          <option value="Czech">Czech</option>
          <option value="Swedish">Swedish</option>
          <option value="Danish">Danish</option>
          <option value="Finnish">Finnish</option>
          <option value="Norwegian">Norwegian</option>
          <option value="Hungarian">Hungarian</option>
          <option value="Romanian">Romanian</option>
          <option value="Ukrainian">Ukrainian</option>
          <option value="Malay">Malay/Indonesian</option>
          <option value="Tagalog">Tagalog</option>
          <option value="Swahili">Swahili</option>
          <option value="Tamil">Tamil</option>
          <option value="Telugu">Telugu</option>
          <option value="Punjabi">Punjabi</option>
          <option value="Marathi">Marathi</option>
          <option value="Gujarati">Gujarati</option>
        </select>
</div>


      <div className="content">
        <div className="question-section">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Enter the customer comment here"
            rows="10"
            cols="50"
          />
        </div>

        <div className="translate-option">
          <label>
            Translate Comment:
            <input
              type="checkbox"
              checked={translateComment}
              onChange={() => setTranslateComment(!translateComment)}
            />
          </label>
        </div>

        <div className="answer-section">
          {subject && <p><strong>Subject:</strong> {subject}</p>}
          <textarea
            value={answer}
            rows="10"
            cols="50"
            readOnly
            placeholder="Generated email content will appear here"
          />
        </div>

        {isLoading ? (
          <p>Loading...</p>
        ) : (
          <button onClick={handleSubmit}>Generate Email</button>
        )}

        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
};

export default App;






// import React, { useState } from 'react';
// import axios from 'axios';
// import './App.css';

// const App = () => {
//   const [language, setLanguage] = useState('English');
//   const [question, setQuestion] = useState('');
//   const [subject, setSubject] = useState('');
//   const [answer, setAnswer] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [error, setError] = useState('');

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setIsLoading(true);
//     setError('');

//     try {
//       const response = await axios.post(`/generate_email`, {
//         comment: question,
//         language: language
//       }, {
//         headers: {
//           'Content-Type': 'application/json',
//         },
//       });

//       setSubject(response.data.subject);
//       setAnswer(response.data.email);
//     } catch (error) {
//       console.error('Error generating email:', error);
//       setError('An error occurred while generating the email. Please try again.');
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <div className="container">
//       <div className="language-selector">
//         <select value={language} onChange={(e) => setLanguage(e.target.value)}>
//           <option value="English">English</option>
//           <option value="Spanish">Spanish</option>
//           <option value="French">French</option>
//         </select>
//       </div>
//       <div className="content">
//         <div className="question-section">
//           <textarea
//             value={question}
//             onChange={(e) => setQuestion(e.target.value)}
//             placeholder="Enter your question here"
//             rows="10"
//             cols="50"
//           />
//         </div>
//         <div className="answer-section">
//           {subject && <p><strong>Subject:</strong> {subject}</p>}
//           <textarea
//             value={error ? error : answer}
//             readOnly
//             placeholder="Answer will appear here"
//             rows="10"
//             cols="50"
//           />
//         </div>
//       </div>
//       <div className="submit-section">
//         <button onClick={handleSubmit} disabled={isLoading}>
//           {isLoading ? 'Generating...' : 'Submit'}
//         </button>
//       </div>
//     </div>
//   );
// };

// export default App;
